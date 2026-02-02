import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Ajouter le chemin src au PYTHONPATH
root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_path))

from src.monitoring.metrics_tracker import get_tracker
from src.monitoring.cost_calculator import get_calculator

# Configuration
st.set_page_config(page_title="Monitoring Pro", page_icon="📊", layout="wide")

# ============================================================================
# CSS ULTRA MODERNE
# ============================================================================
st.markdown("""
<style>
/* Fond avec animation */
.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Titres */
h1, h2, h3, h4 { color: #1e3a8a !important; font-weight: 700 !important; }
p, span, div, label { color: #212529 !important; }

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

.animated { animation: fadeIn 0.5s ease-out; }
.pulse { animation: pulse 2s ease-in-out infinite; }

/* Cartes avec effet hover */
.hover-card {
    transition: all 0.3s ease;
    cursor: pointer;
}

.hover-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important;
}

/* Graphiques avec bordure animée */
.chart-container {
    border: 2px solid transparent;
    border-radius: 15px;
    background: white;
    padding: 1rem;
    position: relative;
    overflow: hidden;
}

.chart-container::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #0066cc, #28a745, #ffc107, #dc3545);
    border-radius: 15px;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.chart-container:hover::before {
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER AVEC ANIMATION
# ============================================================================
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white; padding: 2.5rem; border-radius: 15px;
            text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;" class="animated pulse">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem; font-weight: 800; color: white !important;">
        📊 Monitoring Ultra Pro
    </h1>
    <p style="font-size: 1.3rem; opacity: 0.95; margin: 0; color: white !important;">
        Analytics Avancés • Visualisations Spectaculaires • Dashboard Interactif
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALISATION
# ============================================================================
tracker = get_tracker()
calculator = get_calculator()

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.15); padding: 1.5rem; 
                border-radius: 12px; margin-bottom: 1.5rem; text-align: center;">
        <h2 style="color: white !important; margin: 0; font-size: 1.5rem;">⚙️ Actions</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Rafraîchir", use_container_width=True, type="primary"):
        st.rerun()

    if st.button("📥 Export CSV", use_container_width=True):
        export_path = tracker.export_csv()
        st.success(f"✅ Exporté!")

    st.markdown("---")

    if st.button("🗑️ Reset", use_container_width=True, type="secondary"):
        if st.session_state.get("confirm_reset"):
            tracker.reset()
            st.success("✅ Reset OK")
            st.session_state.confirm_reset = False
            st.rerun()
        else:
            st.session_state.confirm_reset = True
            st.warning("⚠️ Confirmer?")

# ============================================================================
# CALCULS
# ============================================================================
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
# KPI CARDS MODERNES
# ============================================================================
st.markdown("### 📈 Indicateurs Temps Réel")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="hover-card" style="background: linear-gradient(135deg, #28a745 0%, #48c774 100%);
                color: white; padding: 2rem; border-radius: 15px;
                text-align: center; box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">💰</div>
        <div style="font-size: 2.8rem; font-weight: 900; margin-bottom: 0.5rem;">
            {calculator.format_cost(cost_data["total_cost"])}
        </div>
        <div style="font-size: 1.1rem; opacity: 0.95; font-weight: 600;">COÛT TOTAL</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="hover-card" style="background: linear-gradient(135deg, #0066cc 0%, #3385d6 100%);
                color: white; padding: 2rem; border-radius: 15px;
                text-align: center; box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3);">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">📞</div>
        <div style="font-size: 2.8rem; font-weight: 900; margin-bottom: 0.5rem;">
            {api_stats['total_calls']}
        </div>
        <div style="font-size: 1.1rem; opacity: 0.95; font-weight: 600;">APPELS API</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    latency_value = f"{api_stats['avg_latency']:.2f}s" if api_stats["avg_latency"] > 0 else "N/A"
    st.markdown(f"""
    <div class="hover-card" style="background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
                color: white; padding: 2rem; border-radius: 15px;
                text-align: center; box-shadow: 0 6px 20px rgba(23, 162, 184, 0.3);">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">⚡</div>
        <div style="font-size: 2.8rem; font-weight: 900; margin-bottom: 0.5rem;">
            {latency_value}
        </div>
        <div style="font-size: 1.1rem; opacity: 0.95; font-weight: 600;">LATENCE</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="hover-card" style="background: linear-gradient(135deg, #ffc107 0%, #ffab00 100%);
                color: #212529; padding: 2rem; border-radius: 15px;
                text-align: center; box-shadow: 0 6px 20px rgba(255, 193, 7, 0.3);">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-size: 2.8rem; font-weight: 900; margin-bottom: 0.5rem; color: #212529 !important;">
            {pred_stats['total']}
        </div>
        <div style="font-size: 1.1rem; opacity: 0.95; font-weight: 600; color: #212529 !important;">PRÉDICTIONS</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# GRAPHIQUE 1: ÉVOLUTION TEMPORELLE DES COÛTS (AREA CHART STYLÉ)
# ============================================================================
st.markdown("## 💰 Évolution des Coûts en Temps Réel")

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
            "timestamp": datetime.fromisoformat(call["timestamp"]),
            "cost": cumulative_cost,
            "incremental": cost["cost_total"] if call.get("service") == "mistral" else 0
        })
    
    if costs_over_time:
        df_cost = pd.DataFrame(costs_over_time)
        
        # Graphique avec double axe
        fig_cost = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Ligne de coût cumulé
        fig_cost.add_trace(
            go.Scatter(
                x=df_cost["timestamp"],
                y=df_cost["cost"],
                name="Coût Cumulé",
                mode='lines',
                line=dict(color='#0066cc', width=4),
                fill='tozeroy',
                fillcolor='rgba(0, 102, 204, 0.2)',
                hovertemplate='<b>%{x}</b><br>Cumulé: %{y:.4f}€<extra></extra>'
            ),
            secondary_y=False
        )
        
        # Barres de coût incrémental
        fig_cost.add_trace(
            go.Bar(
                x=df_cost["timestamp"],
                y=df_cost["incremental"],
                name="Coût par appel",
                marker=dict(color='#28a745', opacity=0.6),
                hovertemplate='<b>%{x}</b><br>Appel: %{y:.4f}€<extra></extra>'
            ),
            secondary_y=True
        )
        
        fig_cost.update_layout(
            height=450,
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255,255,255,0.8)'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        fig_cost.update_xaxes(
            title_text="Date & Heure",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            showline=True,
            linecolor='rgba(0,0,0,0.2)'
        )
        
        fig_cost.update_yaxes(
            title_text="<b>Coût Cumulé (€)</b>",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            secondary_y=False
        )
        
        fig_cost.update_yaxes(
            title_text="<b>Coût par Appel (€)</b>",
            showgrid=False,
            secondary_y=True
        )
        
        st.plotly_chart(fig_cost, use_container_width=True)
else:
    st.info("💡 Aucune donnée disponible")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# GRAPHIQUE 2: DASHBOARD MULTI-MÉTRIQUES (3D SUNBURST)
# ============================================================================
st.markdown("## 🎨 Distribution des Ressources")

col1, col2 = st.columns(2)

with col1:
    # Sunburst Chart - Répartition hiérarchique
    st.markdown("### 🌟 Répartition Hiérarchique")
    
    if cost_data["total_cost"] > 0:
        # Créer données hiérarchiques
        sunburst_data = {
            'labels': ['Total', 'Mistral API', 'Embeddings', 
                      f'Input Tokens\n{cost_data["mistral"]["tokens_input"]:,}',
                      f'Output Tokens\n{cost_data["mistral"]["tokens_output"]:,}',
                      f'Embed Calls\n{cost_data["embeddings"]["calls"]}'],
            'parents': ['', 'Total', 'Total', 'Mistral API', 'Mistral API', 'Embeddings'],
            'values': [
                cost_data["total_cost"],
                cost_data["mistral"]["cost"],
                cost_data["embeddings"]["cost"],
                cost_data["mistral"]["cost"] * 0.6,  # Approximation
                cost_data["mistral"]["cost"] * 0.4,
                cost_data["embeddings"]["cost"]
            ]
        }
        
        fig_sunburst = go.Figure(go.Sunburst(
            labels=sunburst_data['labels'],
            parents=sunburst_data['parents'],
            values=sunburst_data['values'],
            branchvalues="total",
            marker=dict(
                colors=['#1e3a8a', '#0066cc', '#28a745', '#3385d6', '#5599ff', '#48c774'],
                line=dict(color='white', width=2)
            ),
            hovertemplate='<b>%{label}</b><br>Valeur: %{value:.4f}€<br>%{percentParent}<extra></extra>'
        ))
        
        fig_sunburst.update_layout(
            height=400,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.info("💡 Pas encore de données")

with col2:
    # Gauge Chart - Indicateur de budget
    st.markdown("### 🎯 Indicateur de Budget")
    
    if cost_data["total_cost"] > 0:
        budget_limit = 10.0
        usage_pct = min((cost_data["total_cost"] / budget_limit) * 100, 100)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=usage_pct,
            title={'text': "Utilisation Budget (%)", 'font': {'size': 20}},
            delta={'reference': 50, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "darkblue"},
                'bar': {'color': "#0066cc", 'thickness': 0.75},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#d4edda'},
                    {'range': [50, 80], 'color': '#fff3cd'},
                    {'range': [80, 100], 'color': '#f8d7da'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'size': 16}
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Budget info
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    padding: 1rem; border-radius: 10px; text-align: center;
                    border-left: 4px solid #0066cc;">
            <p style="margin: 0; color: #212529 !important; font-size: 1.1rem;">
                <strong>{cost_data["total_cost"]:.4f}€</strong> / {budget_limit}€
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 Pas encore de données")

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# GRAPHIQUE 3: PERFORMANCES (RADAR CHART + HEATMAP)
# ============================================================================
st.markdown("## ⚡ Analyse des Performances")

latency_stats = tracker.get_latency_stats()

if latency_stats and len(latency_stats) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📡 Radar des Performances")
        
        # Radar Chart
        categories = list(latency_stats.keys())
        values = [latency_stats[cat]['avg'] for cat in categories]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(0, 102, 204, 0.3)',
            line=dict(color='#0066cc', width=3),
            marker=dict(size=8, color='#0066cc'),
            name='Latence Moyenne',
            hovertemplate='<b>%{theta}</b><br>Latence: %{r:.3f}s<extra></extra>'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.2] if values else [0, 1],
                    showline=False,
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                angularaxis=dict(
                    showline=True,
                    linecolor='rgba(0,0,0,0.2)',
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                bgcolor='rgba(0,0,0,0.02)'
            ),
            showlegend=False,
            height=400,
            margin=dict(t=50, b=50, l=80, r=80),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("### 🔥 Heatmap Temporelle")
        
        # Heatmap des latences par heure
        if tracker.latencies:
            df_lat = pd.DataFrame(tracker.latencies)
            df_lat['timestamp'] = pd.to_datetime(df_lat['timestamp'])
            df_lat['hour'] = df_lat['timestamp'].dt.hour
            df_lat['day'] = df_lat['timestamp'].dt.day_name()
            
            # Créer matrice pour heatmap
            pivot_table = df_lat.pivot_table(
                values='duration',
                index='component',
                columns='hour',
                aggfunc='mean',
                fill_value=0
            )
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=pivot_table.values,
                x=[f"{h}h" for h in pivot_table.columns],
                y=pivot_table.index,
                colorscale=[
                    [0, '#d4edda'],
                    [0.5, '#fff3cd'],
                    [1, '#f8d7da']
                ],
                hovertemplate='<b>%{y}</b><br>Heure: %{x}<br>Latence: %{z:.3f}s<extra></extra>',
                colorbar=dict(title="Latence (s)")
            ))
            
            fig_heatmap.update_layout(
                height=400,
                xaxis_title="Heure de la journée",
                yaxis_title="Composant",
                margin=dict(t=50, b=50, l=100, r=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("💡 Pas encore assez de données")
else:
    st.info("💡 Aucune donnée de latence disponible")

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# GRAPHIQUE 4: PRÉDICTIONS (TREEMAP + FUNNEL)
# ============================================================================
st.markdown("## 🎯 Analytics des Prédictions ML")

if pred_stats["total"] > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🗺️ Treemap des Gravités")
        
        # Treemap
        severity_data = []
        for severity, count in pred_stats["by_severity"].items():
            severity_data.append({
                'severity': severity,
                'count': count,
                'percentage': (count / pred_stats['total']) * 100
            })
        
        df_sev = pd.DataFrame(severity_data)
        
        fig_treemap = go.Figure(go.Treemap(
            labels=df_sev['severity'],
            parents=[''] * len(df_sev),
            values=df_sev['count'],
            marker=dict(
                colors=['#dc3545', '#ffc107', '#28a745', '#6c757d'],
                line=dict(width=3, color='white')
            ),
            text=[f"{row['severity']}<br>{row['count']} cas<br>{row['percentage']:.1f}%" 
                  for _, row in df_sev.iterrows()],
            textfont=dict(size=16, color='white'),
            hovertemplate='<b>%{label}</b><br>Nombre: %{value}<br>%{text}<extra></extra>'
        ))
        
        fig_treemap.update_layout(
            height=400,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Distribution 3D")
        
        # 3D Pie Chart
        fig_3d = go.Figure(data=[go.Pie(
            labels=list(pred_stats["by_severity"].keys()),
            values=list(pred_stats["by_severity"].values()),
            hole=0.4,
            marker=dict(
                colors=['#dc3545', '#ffc107', '#28a745', '#6c757d'],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, color='white'),
            pull=[0.1, 0.05, 0.05, 0.05],  # Pull out premier segment
            hovertemplate='<b>%{label}</b><br>%{value} cas<br>%{percent}<extra></extra>'
        )])
        
        fig_3d.update_layout(
            height=400,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            margin=dict(t=20, b=20, l=20, r=100),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)
else:
    st.info("💡 Aucune prédiction disponible")

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# GRAPHIQUE 5: TIMELINE INTERACTIVE
# ============================================================================
st.markdown("## 📅 Timeline Interactive des Événements")

if tracker.api_calls or tracker.predictions:
    # Combiner tous les événements
    events = []
    
    for call in tracker.api_calls[-20:]:  # Derniers 20
        events.append({
            'timestamp': datetime.fromisoformat(call['timestamp']),
            'type': 'API Call',
            'service': call.get('service', 'unknown'),
            'duration': call.get('latency', 0)
        })
    
    for pred in tracker.predictions[-20:]:  # Dernières 20
        events.append({
            'timestamp': datetime.fromisoformat(pred['timestamp']),
            'type': 'Prediction',
            'service': pred['severity'],
            'duration': 0
        })
    
    df_events = pd.DataFrame(events).sort_values('timestamp')
    
    # Timeline scatter
    fig_timeline = go.Figure()
    
    # API Calls
    api_events = df_events[df_events['type'] == 'API Call']
    if len(api_events) > 0:
        fig_timeline.add_trace(go.Scatter(
            x=api_events['timestamp'],
            y=[1] * len(api_events),
            mode='markers',
            name='API Calls',
            marker=dict(size=15, color='#0066cc', symbol='circle', line=dict(width=2, color='white')),
            hovertemplate='<b>API Call</b><br>%{x}<br>Service: %{text}<extra></extra>',
            text=api_events['service']
        ))
    
    # Predictions
    pred_events = df_events[df_events['type'] == 'Prediction']
    if len(pred_events) > 0:
        color_map = {'ROUGE': '#dc3545', 'JAUNE': '#ffc107', 'VERT': '#28a745', 'GRIS': '#6c757d'}
        colors = [color_map.get(s, '#6c757d') for s in pred_events['service']]
        
        fig_timeline.add_trace(go.Scatter(
            x=pred_events['timestamp'],
            y=[2] * len(pred_events),
            mode='markers',
            name='Prédictions',
            marker=dict(size=15, color=colors, symbol='diamond', line=dict(width=2, color='white')),
            hovertemplate='<b>Prédiction</b><br>%{x}<br>Gravité: %{text}<extra></extra>',
            text=pred_events['service']
        ))
    
    fig_timeline.update_layout(
        height=300,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2],
            ticktext=['API', 'Predictions'],
            showgrid=False
        ),
        xaxis=dict(
            title="Timeline",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        margin=dict(t=50, b=50, l=50, r=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("💡 Aucun événement à afficher")

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# FOOTER STYLÉ
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 3rem;
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            border-radius: 15px; color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);'>
    <h2 style='font-size: 2rem; font-weight: 800; margin-bottom: 1rem; color: white !important;'>
        📊 Monitoring Ultra Pro
    </h2>
    <p style='font-size: 1.1rem; opacity: 0.95; margin: 0.5rem 0; color: white !important;'>
        Visualisations Avancées • Analytics Temps Réel • Dashboard Interactif
    </p>
    <p style='font-size: 0.9rem; opacity: 0.8; margin-top: 1.5rem; color: white !important;'>
        🚀 Propulsé par Plotly • Streamlit • Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)