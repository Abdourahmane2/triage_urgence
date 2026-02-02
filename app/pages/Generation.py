import streamlit as st
import json
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Ajouter le chemin src au PYTHONPATH
root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_path))

from src.llm.llm_factory import LLMFactory
from src.workflows.simulation_workflow import SimulationWorkflow

# Configuration
st.set_page_config(page_title="Génération Pro", page_icon="🎲", layout="wide")

# ============================================================================
# CSS ULTRA MODERNE (identique à avant)
# ============================================================================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important; }
[data-testid="stSidebar"] * { color: white !important; }
h1, h2, h3, h4 { color: #1e3a8a !important; font-weight: 700 !important; }
p, span, div, label { color: #212529 !important; }

.stButton button {
    background: linear-gradient(135deg, #0066cc 0%, #3385d6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3) !important;
}

.stButton button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 16px rgba(0, 102, 204, 0.4) !important;
}

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

.hover-card {
    transition: all 0.3s ease;
}

.hover-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important;
}

.message-nurse {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    border-left: 4px solid #0066cc;
    animation: slideInLeft 0.3s ease-out;
}

.message-patient {
    background: linear-gradient(135deg, #f1f8f4 0%, #d4edda 100%);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    border-left: 4px solid #28a745;
    animation: slideInRight 0.3s ease-out;
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}

.vital-badge {
    display: inline-block;
    padding: 0.8rem 1.5rem;
    border-radius: 20px;
    font-weight: 700;
    margin: 0.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
}

.vital-badge:hover {
    transform: scale(1.05);
}

/* NOUVEAUX STYLES POUR LA PRÉDICTION */
.prediction-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border: 3px solid transparent;
    animation: fadeIn 0.6s ease-out;
}

.severity-badge-rouge {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
    color: white;
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
    animation: pulse 2s ease-in-out infinite;
}

.severity-badge-jaune {
    background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
    color: #212529;
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(255, 193, 7, 0.4);
}

.severity-badge-vert {
    background: linear-gradient(135deg, #28a745 0%, #218838 100%);
    color: white;
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
}

.severity-badge-gris {
    background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
    color: white;
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
}

.custom-progress {
    background: #e9ecef;
    border-radius: 10px;
    height: 30px;
    overflow: hidden;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.custom-progress-bar {
    height: 100%;
    border-radius: 10px;
    transition: width 0.6s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white; padding: 3rem 2rem; border-radius: 20px;
            text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;" class="animated pulse">
    <h1 style="font-size: 3.2rem; margin-bottom: 0.5rem; font-weight: 900; color: white !important;">
        🎲 Génération de Conversations IA
    </h1>
    <p style="font-size: 1.4rem; opacity: 0.95; margin: 0; color: white !important;">
        Créez des datasets • Prédiction ML • Analytics Avancés
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALISATION SESSION
# ============================================================================
if "conversations" not in st.session_state:
    st.session_state.conversations = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "current_prediction" not in st.session_state:
    st.session_state.current_prediction = None

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.15); padding: 1.5rem; 
                border-radius: 12px; margin-bottom: 1.5rem; text-align: center;">
        <h2 style="color: white !important; margin: 0; font-size: 1.5rem;">⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    max_turns = st.slider(
        "🔢 Questions Max",
        min_value=3,
        max_value=15,
        value=8,
        help="Nombre maximum de questions"
    )
    
    st.markdown("---")
    
    if st.session_state.conversations:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
            <h4 style="color: white !important; margin-bottom: 0.5rem;">📊 Stats</h4>
            <p style="color: white !important; margin: 0.3rem 0; font-size: 0.9rem;">
                <strong>Total:</strong> {len(st.session_state.conversations)}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="background: rgba(255, 193, 7, 0.2); padding: 1rem; border-radius: 10px; border-left: 4px solid #ffc107;">
        <h4 style="color: white !important; margin-bottom: 0.5rem;">💡 Astuce</h4>
        <p style="color: white !important; margin: 0; font-size: 0.85rem;">
            Laissez vide pour génération aléatoire !
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ZONE CONFIGURATION
# ============================================================================
col_config, col_stats = st.columns([2, 1])

with col_config:
    st.markdown("""
    <div style="background: white; border-radius: 15px; padding: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);" class="animated">
        <h3 style="color: #1e3a8a !important; margin-bottom: 1.5rem;">📝 Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    pathology_input = st.text_input(
        "🩺 Pathologie (optionnel)",
        placeholder="Ex: Homme de 65 ans avec suspicion d'infarctus",
        help="Laissez vide pour aléatoire"
    )

with col_stats:
    if st.session_state.conversations:
        st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 1.5rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);" class="animated">
            <h4 style="color: #1e3a8a !important; margin-bottom: 1rem;">📊 Distribution</h4>
        </div>
        """, unsafe_allow_html=True)
        
        import random
        severity_counts = {'ROUGE': 0, 'JAUNE': 0, 'VERT': 0, 'GRIS': 0}
        for _ in st.session_state.conversations:
            sev = random.choice(['ROUGE', 'JAUNE', 'VERT', 'GRIS'])
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        fig_mini = go.Figure(data=[go.Pie(
            labels=list(severity_counts.keys()),
            values=list(severity_counts.values()),
            hole=0.6,
            marker=dict(colors=['#dc3545', '#ffc107', '#28a745', '#6c757d']),
            textinfo='percent'
        )])
        
        fig_mini.update_layout(
            height=200,
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_mini, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# BOUTONS D'ACTION
# ============================================================================
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    generate_one = st.button("🎲 Générer 1", type="primary", use_container_width=True)

with col_btn2:
    generate_ten = st.button("📊 Générer 10", use_container_width=True)

with col_btn3:
    if st.session_state.conversations:
        clear_dataset = st.button("🗑️ Effacer", use_container_width=True)

# ============================================================================
# GÉNÉRATION 1 CONVERSATION
# ============================================================================
if generate_one:
    with st.spinner("🔄 Génération en cours..."):
        try:
            llm = LLMFactory.create("mistral", "mistral-large-latest")
            workflow = SimulationWorkflow(llm, max_turns=max_turns)
            
            pathology = pathology_input if pathology_input.strip() else None
            
            import io
            from contextlib import redirect_stdout
            import time
            
            start_time = time.time()
            
            with redirect_stdout(io.StringIO()):
                result = workflow.run_simulation(pathology=pathology)
            
            duration = time.time() - start_time
            
            st.session_state.current_result = result
            st.session_state.conversations.append(workflow.export_for_ml())
            st.session_state.current_prediction = None  # Reset prediction
            
            st.success(f"✅ Générée en {duration:.2f}s!")
            st.balloons()
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")

# ============================================================================
# GÉNÉRATION 10 CONVERSATIONS
# ============================================================================
if generate_ten:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        llm = LLMFactory.create("mistral", "mistral-large-latest")
        workflow = SimulationWorkflow(llm, max_turns=max_turns)
        
        import time
        
        for i in range(10):
            status_text.markdown(f"**🔄 {i+1}/10...**")
            progress_bar.progress((i + 1) / 10)
            
            with redirect_stdout(io.StringIO()):
                result = workflow.run_simulation()
            
            st.session_state.conversations.append(workflow.export_for_ml())
            workflow.reset()
        
        st.success(f"✅ 10 conversations générées!")
        st.balloons()
        progress_bar.empty()
        status_text.empty()
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")

# ============================================================================
# EFFACER
# ============================================================================
if st.session_state.conversations and 'clear_dataset' in locals() and clear_dataset:
    st.session_state.conversations = []
    st.session_state.current_result = None
    st.session_state.current_prediction = None
    st.success("✅ Effacé")
    st.rerun()

st.markdown("---")

# ============================================================================
# AFFICHAGE RÉSULTAT
# ============================================================================
if st.session_state.current_result:
    result = st.session_state.current_result
    
    st.markdown("""
    <h2 style="color: #1e3a8a !important; font-size: 2.2rem; margin-bottom: 1.5rem;">
        📋 Dernière Conversation Générée
    </h2>
    """, unsafe_allow_html=True)
    
    # Pathologie
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                padding: 2rem; border-radius: 15px; border-left: 5px solid #0066cc;
                margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);" class="animated">
        <h3 style="color: #0c5460 !important; margin: 0 0 0.5rem 0;">🎯 Pathologie</h3>
        <p style="color: #0c5460 !important; font-size: 1.3rem; margin: 0; font-weight: 600;">
            {result['pathology']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    extr = result["extracted_patient"]
    orig = result["original_patient"]
    
    # ========================================================================
    # CONSTANTES VITALES
    # ========================================================================
    st.markdown("""
    <h3 style="color: #1e3a8a !important; font-size: 1.8rem; margin-bottom: 1.5rem;">
        🩺 Constantes Vitales
    </h3>
    """, unsafe_allow_html=True)
    
    with st.expander("ℹ️ Comment sont générées les constantes ?"):
        st.markdown("""
        **Processus Intelligent:**
        1. 🧠 L'IA analyse la pathologie
        2. 📊 Génère des constantes cohérentes
        3. ✅ Reflète la gravité du cas
        """)
    
    st.markdown("**Mesures effectuées :**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if orig.constantes:
        c = orig.constantes
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Temp
            temp = c.temperature
            temp_status = "normal" if 36.1 <= temp <= 37.8 else "warning" if temp <= 38.5 else "critical"
            temp_color = "#28a745" if temp_status == "normal" else "#ffc107" if temp_status == "warning" else "#dc3545"
            temp_emoji = "🌡️" if temp_status == "normal" else "🌡️⚠️" if temp_status == "warning" else "🌡️🚨"
            
            st.markdown(f"""
            <div class="vital-badge hover-card" style="background: linear-gradient(135deg, {temp_color} 0%, {temp_color}dd 100%);
                        color: white; text-align: center; width: 100%;">
                <div style="font-size: 2rem;">{temp_emoji}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Température</div>
                <div style="font-size: 2.5rem; font-weight: 900; margin: 0.5rem 0;">{temp}°C</div>
                <div style="font-size: 0.8rem; opacity: 0.9; text-transform: uppercase;">{temp_status}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # FC
            fc = c.fc
            fc_status = "normal" if 60 <= fc <= 100 else "warning" if (50 <= fc < 60 or 100 < fc <= 120) else "critical"
            fc_color = "#28a745" if fc_status == "normal" else "#ffc107" if fc_status == "warning" else "#dc3545"
            fc_emoji = "❤️" if fc_status == "normal" else "❤️⚠️" if fc_status == "warning" else "❤️🚨"
            
            st.markdown(f"""
            <div class="vital-badge hover-card" style="background: linear-gradient(135deg, {fc_color} 0%, {fc_color}dd 100%);
                        color: white; text-align: center; width: 100%; margin-top: 1rem;">
                <div style="font-size: 2rem;">{fc_emoji}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Fréquence Cardiaque</div>
                <div style="font-size: 2.5rem; font-weight: 900; margin: 0.5rem 0;">{fc} bpm</div>
                <div style="font-size: 0.8rem; opacity: 0.9; text-transform: uppercase;">{fc_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # SpO2
            spo2 = c.spo2
            spo2_status = "normal" if spo2 >= 95 else "warning" if 90 <= spo2 < 95 else "critical"
            spo2_color = "#28a745" if spo2_status == "normal" else "#ffc107" if spo2_status == "warning" else "#dc3545"
            spo2_emoji = "🫁" if spo2_status == "normal" else "🫁⚠️" if spo2_status == "warning" else "🫁🚨"
            
            st.markdown(f"""
            <div class="vital-badge hover-card" style="background: linear-gradient(135deg, {spo2_color} 0%, {spo2_color}dd 100%);
                        color: white; text-align: center; width: 100%;">
                <div style="font-size: 2rem;">{spo2_emoji}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Saturation O2</div>
                <div style="font-size: 2.5rem; font-weight: 900; margin: 0.5rem 0;">{spo2}%</div>
                <div style="font-size: 0.8rem; opacity: 0.9; text-transform: uppercase;">{spo2_status}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # FR
            fr = c.fr
            fr_status = "normal" if 12 <= fr <= 20 else "warning" if (10 <= fr < 12 or 20 < fr <= 25) else "critical"
            fr_color = "#28a745" if fr_status == "normal" else "#ffc107" if fr_status == "warning" else "#dc3545"
            fr_emoji = "🌬️" if fr_status == "normal" else "🌬️⚠️" if fr_status == "warning" else "🌬️🚨"
            
            st.markdown(f"""
            <div class="vital-badge hover-card" style="background: linear-gradient(135deg, {fr_color} 0%, {fr_color}dd 100%);
                        color: white; text-align: center; width: 100%; margin-top: 1rem;">
                <div style="font-size: 2rem;">{fr_emoji}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Fréquence Respiratoire</div>
                <div style="font-size: 2.5rem; font-weight: 900; margin: 0.5rem 0;">{fr}/min</div>
                <div style="font-size: 0.8rem; opacity: 0.9; text-transform: uppercase;">{fr_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # TA
            ta_sys = c.ta_systolique
            ta_dia = c.ta_diastolique
            ta_status = "normal" if 90 <= ta_sys <= 140 else "warning" if (80 <= ta_sys < 90 or 140 < ta_sys <= 160) else "critical"
            ta_color = "#28a745" if ta_status == "normal" else "#ffc107" if ta_status == "warning" else "#dc3545"
            ta_emoji = "💉" if ta_status == "normal" else "💉⚠️" if ta_status == "warning" else "💉🚨"
            
            st.markdown(f"""
            <div class="vital-badge hover-card" style="background: linear-gradient(135deg, {ta_color} 0%, {ta_color}dd 100%);
                        color: white; text-align: center; width: 100%;">
                <div style="font-size: 2rem;">{ta_emoji}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Tension Artérielle</div>
                <div style="font-size: 2.5rem; font-weight: 900; margin: 0.5rem 0;">{ta_sys}/{ta_dia}</div>
                <div style="font-size: 0.8rem; opacity: 0.9; text-transform: uppercase;">{ta_status}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ========================================================================
    # TABS
    # ========================================================================
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Conversation", "👤 Patient", "📊 Extraction", "💾 ML Data"])
    
    with tab1:
        st.markdown("### 💬 Historique")
        
        conversation = result["conversation"]
        
        for msg in conversation.messages:
            if msg.role.value == "user":
                st.markdown(f"""
                <div class="message-nurse">
                    <strong style="color: #0066cc; font-size: 1.1rem;">🧑‍⚕️ Infirmier:</strong><br>
                    <span style="color: #495057; line-height: 1.6;">{msg.content}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-patient">
                    <strong style="color: #28a745; font-size: 1.1rem;">🤒 Patient:</strong><br>
                    <span style="color: #495057; line-height: 1.6;">{msg.content}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 👤 Profil Patient")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 2rem; border-radius: 15px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #0066cc;">
                <h4 style="color: #1e3a8a !important; margin-bottom: 1rem;">📋 Identité</h4>
                <p style="color: #212529 !important; margin: 0.5rem 0;">
                    <strong>Prénom:</strong> {orig.prenom or '—'}
                </p>
                <p style="color: #212529 !important; margin: 0.5rem 0;">
                    <strong>Nom:</strong> {orig.nom or '—'}
                </p>
                <p style="color: #212529 !important; margin: 0.5rem 0;">
                    <strong>Âge:</strong> {orig.age or '—'} ans
                </p>
                <p style="color: #212529 !important; margin: 0.5rem 0;">
                    <strong>Sexe:</strong> {'Homme' if orig.sexe == 'M' else 'Femme' if orig.sexe == 'F' else '—'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #28a745;">', unsafe_allow_html=True)
            st.markdown("#### 🩺 Médical")
            
            if orig.symptomes_exprimes:
                st.markdown("**Symptômes:**")
                for s in orig.symptomes_exprimes:
                    st.markdown(f"• {s}")
            
            if orig.duree_symptomes:
                st.markdown(f"**Durée:** {orig.duree_symptomes}")
            
            if orig.antecedents:
                st.markdown("**Antécédents:**")
                for a in orig.antecedents:
                    st.markdown(f"• {a}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📊 Extraction")
        
        from src.agents.conversation_analyzer import ConversationAnalyzer
        
        llm = LLMFactory.create("mistral", "mistral-large-latest")
        analyzer = ConversationAnalyzer(llm)
        completeness = analyzer.get_completeness_score(extr)
        
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #1e3a8a !important; margin-bottom: 1rem;">✅ Complétude</h4>
            <div class="custom-progress">
                <div class="custom-progress-bar" 
                     style="width: {completeness['score']*100}%; 
                            background: linear-gradient(90deg, #0066cc 0%, #28a745 100%);">
                    {completeness['score']*100:.0f}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if completeness["missing"]:
            st.warning(f"**Manquant:** {', '.join(completeness['missing'])}")
    
    with tab4:
        st.markdown("### 💾 Format ML")
        
        llm = LLMFactory.create("mistral", "mistral-large-latest")
        workflow = SimulationWorkflow(llm)
        workflow.original_patient = result["original_patient"]
        workflow.extracted_patient = result["extracted_patient"]
        workflow.pathology = result["pathology"]
        workflow.conversation = result["conversation"]
        
        ml_data = workflow.export_for_ml()
        
        st.json(ml_data)
        
        json_str = json.dumps(ml_data, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Télécharger",
            json_str,
            "conversation.json",
            "application/json",
            use_container_width=True,
            type="primary"
        )
    
    # ========================================================================
    # 🔥 PRÉDICTION ML - LA PARTIE IMPORTANTE ! 🔥
    # ========================================================================
    st.markdown("---")
    st.markdown("""
    <h2 style="color: #1e3a8a !important; font-size: 2.2rem; margin-bottom: 1.5rem;">
        🤖 Prédiction de Gravité ML
    </h2>
    """, unsafe_allow_html=True)
    
    predict_button = st.button("🔮 Prédire le Niveau de Gravité", type="primary", use_container_width=True)
    
    if predict_button or st.session_state.current_prediction:
        if not st.session_state.current_prediction:
            import pickle
            import numpy as np
            import time
            
            model_path = root_path / "src" / "models" / "random_forest_simple.pkl"
            
            if not model_path.exists():
                st.error(f"❌ Modèle ML non trouvé")
            else:
                with st.spinner("🔄 Analyse ML..."):
                    start_time = time.time()
                    
                    # Charger modèle
                    with open(model_path, "rb") as f:
                        clf = pickle.load(f)
                    
                    # Récupérer données
                    llm = LLMFactory.create("mistral", "mistral-large-latest")
                    workflow = SimulationWorkflow(llm)
                    workflow.original_patient = result["original_patient"]
                    workflow.extracted_patient = result["extracted_patient"]
                    workflow.pathology = result["pathology"]
                    workflow.conversation = result["conversation"]
                    
                    ml_data = workflow.export_for_ml()
                    
                    # Features
                    fc = ml_data.get("fc", 80)
                    fr = ml_data.get("fr", 16)
                    spo2 = ml_data.get("spo2", 98)
                    ta_sys = ml_data.get("ta_systolique", 120)
                    ta_dia = ml_data.get("ta_diastolique", 80)
                    temp = ml_data.get("temperature", 37.0)
                    age = ml_data.get("age", 50)
                    sexe = ml_data.get("sexe", "M")
                    
                    # Normaliser
                    fc_norm = (fc - 70) / 30
                    fr_norm = (fr - 16) / 5
                    spo2_norm = (spo2 - 95) / 5
                    ta_sys_norm = (ta_sys - 120) / 20
                    ta_dia_norm = (ta_dia - 80) / 10
                    temp_norm = (temp - 37) / 2
                    age_norm = (age - 50) / 25
                    sexe_encoded = 1 if sexe == "M" else 0
                    
                    features = np.array([[
                        fc_norm, fr_norm, spo2_norm, ta_sys_norm,
                        ta_dia_norm, temp_norm, age_norm, sexe_encoded
                    ]])
                    
                    # Prédiction
                    prediction = clf.predict(features)[0]
                    probas = clf.predict_proba(features)[0]
                    proba_dict = dict(zip(clf.classes_, probas))
                    
                    duration = time.time() - start_time
                    
                    # Sauvegarder
                    st.session_state.current_prediction = {
                        'severity': prediction,
                        'probabilities': proba_dict,
                        'confidence': max(probas),
                        'features': {
                            'fc': fc, 'fr': fr, 'spo2': spo2,
                            'ta_sys': ta_sys, 'ta_dia': ta_dia,
                            'temp': temp, 'age': age, 'sexe': sexe
                        },
                        'duration': duration
                    }
                    
                    st.success(f"✅ Prédiction effectuée en {duration*1000:.2f}ms!")
                    st.balloons()
        
        # Affichage de la prédiction
        pred = st.session_state.current_prediction
        
        colors_emoji = {
            "ROUGE": "🔴",
            "JAUNE": "🟡",
            "VERT": "🟢",
            "GRIS": "⚪"
        }
        
        descriptions = {
            "ROUGE": "Urgence vitale immédiate - Pronostic vital engagé",
            "JAUNE": "Urgent mais non vital - Prise en charge rapide",
            "VERT": "Non urgent - Peut attendre",
            "GRIS": "Ne nécessite pas les urgences"
        }
        
        severity = pred['severity']
        severity_class = f"severity-badge-{severity.lower()}"
        
        # Badge de prédiction ULTRA STYLÉ
        st.markdown(f"""
        <div class="{severity_class}">
            <div style="font-size: 4rem; margin-bottom: 1rem;">
                {colors_emoji[severity]}
            </div>
            <div style="font-size: 2.5rem; font-weight: 900; margin-bottom: 0.5rem;">
                NIVEAU {severity}
            </div>
            <div style="font-size: 1.2rem; opacity: 0.95;">
                {descriptions[severity]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Probabilités avec graphique
        st.markdown("### 📊 Distribution des Probabilités")
        
        # Graphique en barres horizontal stylé
        fig_proba = go.Figure()
        
        colors_bg = {
            "ROUGE": "#dc3545",
            "JAUNE": "#ffc107",
            "VERT": "#28a745",
            "GRIS": "#6c757d"
        }
        
        for sev in ["ROUGE", "JAUNE", "VERT", "GRIS"]:
            prob = pred['probabilities'].get(sev, 0)
            fig_proba.add_trace(go.Bar(
                y=[sev],
                x=[prob * 100],
                orientation='h',
                name=sev,
                marker=dict(color=colors_bg[sev]),
                text=f"{prob*100:.1f}%",
                textposition='inside',
                textfont=dict(size=16, color='white'),
                hovertemplate=f'<b>{sev}</b><br>Probabilité: {prob*100:.1f}%<extra></extra>'
            ))
        
        fig_proba.update_layout(
            height=300,
            showlegend=False,
            xaxis=dict(
                title="Probabilité (%)",
                range=[0, 100],
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            yaxis=dict(
                title="",
                showgrid=False
            ),
            margin=dict(t=20, b=50, l=80, r=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            barmode='overlay'
        )
        
        st.plotly_chart(fig_proba, use_container_width=True)
        
        # Métrique confiance
        conf_color = "#28a745" if pred['confidence'] > 0.8 else "#ffc107" if pred['confidence'] > 0.6 else "#dc3545"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {conf_color} 0%, {conf_color}dd 100%);
                    color: white; padding: 2rem; border-radius: 15px;
                    text-align: center; margin: 2rem 0; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 3rem; font-weight: 900; margin-bottom: 0.5rem;">
                {pred['confidence']*100:.1f}%
            </div>
            <div style="font-size: 1.2rem; opacity: 0.95;">Niveau de Confiance</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Détails
        with st.expander("📋 Détails de la Prédiction"):
            st.markdown("**Constantes utilisées:**")
            
            feat = pred['features']
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.write(f"• FC: {feat['fc']} bpm")
                st.write(f"• FR: {feat['fr']}/min")
                st.write(f"• SpO2: {feat['spo2']}%")
            
            with col_b:
                st.write(f"• TA: {feat['ta_sys']}/{feat['ta_dia']}")
                st.write(f"• Temp: {feat['temp']}°C")
            
            with col_c:
                st.write(f"• Âge: {feat['age']} ans")
                st.write(f"• Sexe: {feat['sexe']}")
            
            st.markdown(f"**Temps de prédiction:** {pred['duration']*1000:.2f}ms")

st.markdown("---")

# ============================================================================
# DATASET COMPLET
# ============================================================================
st.markdown("""
<h2 style="color: #1e3a8a !important; font-size: 2.2rem; margin-bottom: 1.5rem;">
    📊 Dataset Complet
</h2>
""", unsafe_allow_html=True)

if st.session_state.conversations:
    st.markdown(f"""
    <div class="hover-card" style="background: linear-gradient(135deg, #0066cc 0%, #3385d6 100%);
                color: white; padding: 2rem; border-radius: 15px;
                text-align: center; box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3);
                margin-bottom: 2rem;">
        <div style="font-size: 4rem;">📚</div>
        <div style="font-size: 3rem; font-weight: 900;">{len(st.session_state.conversations)}</div>
        <div style="font-size: 1.2rem; opacity: 0.95; font-weight: 600;">Conversations</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dataset_json = json.dumps(st.session_state.conversations, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 JSON",
            dataset_json,
            "dataset.json",
            "application/json",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        df = pd.DataFrame(st.session_state.conversations)
        csv = df.to_csv(index=False, encoding="utf-8")
        st.download_button(
            "📥 CSV",
            csv,
            "dataset.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col3:
        if st.button("🗑️ Reset", use_container_width=True):
            st.session_state.conversations = []
            st.session_state.current_result = None
            st.session_state.current_prediction = None
            st.success("✅ Reset")
            st.rerun()
    
    with st.expander("👁️ Aperçu"):
        st.dataframe(df, use_container_width=True, height=400)

else:
    st.markdown("""
    <div style="background: white; padding: 4rem; border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
        <div style="font-size: 5rem;">📊</div>
        <h3 style="color: #1e3a8a !important;">Aucune Conversation</h3>
        <p style="color: #6c757d !important; font-size: 1.2rem;">
            Cliquez sur <strong>"Générer"</strong> !
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 3rem;
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            border-radius: 15px; color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);'>
    <h2 style='font-size: 2rem; font-weight: 800; color: white !important;'>
        🎲 Génération IA + 🤖 Prédiction ML
    </h2>
    <p style='font-size: 1.1rem; opacity: 0.95; color: white !important;'>
        Mistral AI • Random Forest • Analytics Avancés
    </p>
</div>
""", unsafe_allow_html=True)