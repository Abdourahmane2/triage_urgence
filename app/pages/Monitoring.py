import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ajouter le chemin src au PYTHONPATH
root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_path))

from src.monitoring.metrics_tracker import get_tracker
from src.monitoring.cost_calculator import get_calculator

# Configuration
st.set_page_config(page_title="Monitoring", page_icon="📊", layout="wide")

# Header
st.title("📊 Monitoring et Analytics")
st.caption("Suivi des performances et des coûts du système")

st.divider()

# Initialisation
tracker = get_tracker()
calculator = get_calculator()

# Sidebar
with st.sidebar:
    st.header("⚙️ Actions")

    if st.button("🔄 Rafraîchir", use_container_width=True, type="primary"):
        st.rerun()

    if st.button("📥 Export CSV", use_container_width=True):
        export_path = tracker.export_csv()
        st.success("✅ Exporté!")

    st.divider()

    if st.button("🗑️ Reset", use_container_width=True, type="secondary"):
        if st.session_state.get("confirm_reset"):
            tracker.reset()
            st.success("✅ Reset OK")
            st.session_state.confirm_reset = False
            st.rerun()
        else:
            st.session_state.confirm_reset = True
            st.warning("⚠️ Confirmer?")

# Calculs
api_stats = tracker.get_api_stats()
cost_data = calculator.calculate_total_cost(tracker.api_calls)
pred_stats = tracker.get_prediction_stats()

if tracker.api_calls:
    first_call = datetime.fromisoformat(tracker.api_calls[0]["timestamp"])
    days_elapsed = max(1, (datetime.now() - first_call).days)
else:
    days_elapsed = 1

monthly_estimate = calculator.estimate_monthly_cost(cost_data["total_cost"], days_elapsed)

# ============================================================================
# 1. INDICATEURS CLÉS (KPI)
# ============================================================================
st.subheader("📈 Indicateurs Clés")
st.caption("Vue d'ensemble des performances du système")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Coût Total",
        calculator.format_cost(cost_data["total_cost"]),
        delta=f"~{calculator.format_cost(monthly_estimate)}/mois",
        help="Coût total des appels API Mistral"
    )

with col2:
    st.metric(
        "📞 Appels API",
        f"{api_stats['total_calls']}",
        help="Nombre total d'appels à l'API Mistral"
    )

with col3:
    latency_value = f"{api_stats['avg_latency']:.2f}s" if api_stats["avg_latency"] > 0 else "N/A"
    st.metric(
        "⚡ Latence Moyenne",
        latency_value,
        help="Temps moyen de réponse de l'API"
    )

with col4:
    st.metric(
        "🎯 Prédictions ML",
        f"{pred_stats['total']}",
        help="Nombre de prédictions de gravité effectuées"
    )

st.divider()

# ============================================================================
# 2. ÉVOLUTION DES COÛTS (GRAPHIQUE PRINCIPAL)
# ============================================================================
st.subheader("💰 Évolution des Coûts dans le Temps")
st.caption("Permet de suivre la consommation budgétaire et détecter les pics d'utilisation")

if tracker.api_calls:
    costs_over_time = []
    cumulative_cost = 0
    
    for call in tracker.api_calls:
        if call.get("service") == "mistral":
            cost = calculator.calculate_mistral_cost(
                call.get("model", "mistral-small-latest"),
                call["tokens_input"],
                call["tokens_output"],
            )
            cumulative_cost += cost["cost_total"]
        
        costs_over_time.append({
            "Date": datetime.fromisoformat(call["timestamp"]),
            "Coût Cumulé (€)": cumulative_cost
        })
    
    if costs_over_time:
        df_cost = pd.DataFrame(costs_over_time)
        
        fig_cost = px.area(
            df_cost,
            x="Date",
            y="Coût Cumulé (€)",
            labels={"Date": "Date et Heure", "Coût Cumulé (€)": "Coût Cumulé (€)"}
        )
        
        fig_cost.update_traces(
            line_color='#0066cc',
            fillcolor='rgba(0, 102, 204, 0.2)'
        )
        
        fig_cost.update_layout(
            height=400,
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # Insights automatiques
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"📊 **{len(tracker.api_calls)} appels** enregistrés depuis {first_call.strftime('%d/%m/%Y')}")
        with col_b:
            avg_cost_per_call = cost_data["total_cost"] / max(1, api_stats['total_calls'])
            st.info(f"💵 Coût moyen par appel: **{calculator.format_cost(avg_cost_per_call)}**")
else:
    st.info("💡 Aucune donnée disponible. Générez des conversations pour voir les statistiques.")

st.divider()

# ============================================================================
# 3. DISTRIBUTION DES PRÉDICTIONS ML
# ============================================================================
st.subheader("🎯 Distribution des Niveaux de Gravité")
st.caption("Montre la répartition des cas par niveau d'urgence - utile pour évaluer la cohérence du modèle")

if pred_stats["total"] > 0:
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # Graphique en barres horizontal (plus lisible)
        severity_data = []
        for severity, count in pred_stats["by_severity"].items():
            percentage = (count / pred_stats['total']) * 100
            severity_data.append({
                "Niveau": severity,
                "Nombre": count,
                "Pourcentage": percentage
            })
        
        df_sev = pd.DataFrame(severity_data)
        
        # Trier par ordre de gravité
        order = {"ROUGE": 0, "JAUNE": 1, "VERT": 2, "GRIS": 3}
        df_sev['order'] = df_sev['Niveau'].map(order)
        df_sev = df_sev.sort_values('order')
        
        fig_bar = px.bar(
            df_sev,
            y="Niveau",
            x="Nombre",
            orientation='h',
            text="Nombre",
            color="Niveau",
            color_discrete_map={
                "ROUGE": "#dc3545",
                "JAUNE": "#ffc107",
                "VERT": "#28a745",
                "GRIS": "#6c757d"
            }
        )
        
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(
            height=300,
            showlegend=False,
            xaxis_title="Nombre de cas",
            yaxis_title=""
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.write("**Statistiques détaillées**")
        
        for idx, row in df_sev.iterrows():
            severity = row['Niveau']
            count = row['Nombre']
            pct = row['Pourcentage']
            
            # Emoji selon gravité
            emoji_map = {"ROUGE": "🔴", "JAUNE": "🟡", "VERT": "🟢", "GRIS": "⚪"}
            emoji = emoji_map.get(severity, "")
            
            st.metric(
                f"{emoji} {severity}",
                f"{count} cas",
                delta=f"{pct:.1f}%"
            )
    
    # Insight
    most_common = df_sev.iloc[0]
    st.success(f"✅ **Niveau le plus fréquent:** {most_common['Niveau']} avec {most_common['Nombre']} cas ({most_common['Pourcentage']:.1f}%)")
    
else:
    st.info("💡 Aucune prédiction disponible. Utilisez l'onglet 'Génération' pour créer des conversations et prédire leur gravité.")

st.divider()

# ============================================================================
# 4. TABLEAU RÉCAPITULATIF
# ============================================================================
st.subheader("📋 Résumé des Métriques")
st.caption("Vue synthétique de toutes les métriques importantes")

if tracker.api_calls or pred_stats["total"] > 0:
    
    # Créer un DataFrame récapitulatif
    summary_data = {
        "Métrique": [
            "Coût total",
            "Estimation mensuelle",
            "Nombre d'appels API",
            "Latence moyenne",
            "Nombre de prédictions",
            "Tokens consommés (input)",
            "Tokens consommés (output)"
        ],
        "Valeur": [
            calculator.format_cost(cost_data["total_cost"]),
            calculator.format_cost(monthly_estimate),
            f"{api_stats['total_calls']}",
            f"{api_stats['avg_latency']:.2f}s" if api_stats["avg_latency"] > 0 else "N/A",
            f"{pred_stats['total']}",
            f"{cost_data['mistral']['tokens_input']:,}",
            f"{cost_data['mistral']['tokens_output']:,}"
        ]
    }
    
    df_summary = pd.DataFrame(summary_data)
    
    st.dataframe(
        df_summary,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
else:
    st.info("💡 Aucune donnée disponible")

# Footer
st.divider()

col_foot1, col_foot2 = st.columns(2)

with col_foot1:
    st.caption("📊 **Utilité du Monitoring:**")
    st.caption("• Contrôler les coûts API en temps réel")
    st.caption("• Détecter les anomalies de performance")
    st.caption("• Valider la cohérence des prédictions ML")

with col_foot2:
    st.caption("💡 **Comment l'interpréter:**")
    st.caption("• Coûts: surveiller la tendance et le budget")
    st.caption("• Latence: détecter les ralentissements")
    st.caption("• Prédictions: vérifier la distribution est réaliste")   