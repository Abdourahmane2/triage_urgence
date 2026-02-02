
import streamlit as st
from pathlib import Path
import sys
import warnings

# Supprimer les warnings sklearn
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.rag.chatbot import TriageChatbotAPI
from src.rag.predictor import MLTriagePredictor

# Config
st.set_page_config(
    page_title="Chat Triage Pro", 
    page_icon="💬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS ULTRA PROFESSIONNEL - DESIGN DE FOU
# ============================================================================
st.markdown("""
<style>
/* ===== FOND PREMIUM ===== */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* ===== SIDEBAR MODERNE ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== TITRES PROFESSIONNELS ===== */
h1, h2, h3, h4 { 
    color: #1a1a2e !important; 
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}

p, span, div, label { 
    color: #2d3436 !important; 
}

/* ===== BOUTONS PREMIUM ===== */
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.stButton button:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6) !important;
}

.stButton button:active {
    transform: translateY(-2px) scale(0.98) !important;
}

/* ===== ANIMATIONS PROFESSIONNELLES ===== */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.03);
    }
}

@keyframes glow {
    0%, 100% {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.4);
    }
    50% {
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.8);
    }
}

.animated {
    animation: fadeInUp 0.6s ease-out;
}

.slide-left {
    animation: slideInLeft 0.4s ease-out;
}

.slide-right {
    animation: slideInRight 0.4s ease-out;
}

.pulse {
    animation: pulse 2s ease-in-out infinite;
}

.glow {
    animation: glow 2s ease-in-out infinite;
}

/* ===== CARTES PREMIUM ===== */
.premium-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.premium-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
}

/* ===== BADGES CONSTANTES VITALES ULTRA STYLÉS ===== */
.vital-badge-pro {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.8rem 1.5rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: 1rem;
    margin: 0.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
    cursor: pointer;
}

.vital-badge-pro:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
}

.vital-normal {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
}

.vital-warning {
    background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
    color: white;
}

.vital-critical {
    background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    color: white;
}

/* ===== PROGRESS BAR PREMIUM ===== */
.progress-premium {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50px;
    height: 35px;
    overflow: hidden;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
}

.progress-premium-bar {
    height: 100%;
    border-radius: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 800;
    font-size: 1rem;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

/* ===== MESSAGES CHAT ULTRA STYLÉS ===== */
.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

.message-user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.2rem 1.8rem;
    border-radius: 25px 25px 5px 25px;
    margin: 1rem 0 1rem auto;
    max-width: 70%;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    animation: slideInRight 0.4s ease-out;
    position: relative;
}

.message-user::before {
    content: "🧑‍⚕️";
    position: absolute;
    right: -45px;
    top: 0;
    font-size: 2rem;
}

.message-assistant {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1.2rem 1.8rem;
    border-radius: 25px 25px 25px 5px;
    margin: 1rem auto 1rem 0;
    max-width: 70%;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    animation: slideInLeft 0.4s ease-out;
    position: relative;
}

.message-assistant::before {
    content: "🤖";
    position: absolute;
    left: -45px;
    top: 0;
    font-size: 2rem;
}

/* ===== PREDICTION BADGE SPECTACULAIRE ===== */
.prediction-spectacle {
    padding: 3rem;
    border-radius: 30px;
    text-align: center;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}

.prediction-spectacle::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: rotate(45deg);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.pred-rouge {
    background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    color: white;
    animation: pulse 2s ease-in-out infinite;
}

.pred-jaune {
    background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
    color: white;
}

.pred-vert {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
}

.pred-gris {
    background: linear-gradient(135deg, #757f9a 0%, #d7dde8 100%);
    color: white;
}

/* ===== SCROLLBAR CUSTOM ===== */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* ===== TIMELINE INTERACTIVE ===== */
.timeline-item {
    position: relative;
    padding-left: 3rem;
    padding-bottom: 2rem;
    border-left: 3px solid #667eea;
    margin-left: 1rem;
}

.timeline-item::before {
    content: "";
    position: absolute;
    left: -8px;
    top: 0;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 0 15px rgba(102, 126, 234, 0.6);
}

.timeline-item:hover::before {
    transform: scale(1.3);
    transition: transform 0.3s ease;
}

/* ===== CONFIDENCE METER ===== */
.confidence-meter {
    position: relative;
    height: 40px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50px;
    overflow: hidden;
    backdrop-filter: blur(5px);
}

.confidence-fill {
    height: 100%;
    border-radius: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 800;
    font-size: 1.1rem;
    transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.confidence-fill::after {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 200%; }
}

/* ===== REMOVE STREAMLIT BRANDING ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER SPECTACULAIRE
# ============================================================================
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 3rem 2rem; border-radius: 30px;
            text-align: center; box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem; position: relative; overflow: hidden;"
            class="animated glow">
    <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; 
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: rotate 20s linear infinite;"></div>
    <h1 style="font-size: 3.5rem; margin-bottom: 1rem; font-weight: 900; 
               color: white !important; text-shadow: 0 4px 10px rgba(0,0,0,0.3);
               letter-spacing: -1px;">
        💬 Assistant IA de Triage Médical
    </h1>
    <p style="font-size: 1.4rem; opacity: 0.95; margin: 0; color: white !important;
              text-shadow: 0 2px 5px rgba(0,0,0,0.2);">
        Analyse Intelligente • Prédiction ML • Aide à la Décision en Temps Réel
    </p>
</div>

<style>
@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if "chatbot" not in st.session_state:
    retriever = None
    with st.spinner("🔄 Initialisation du système..."):
        try:
            project_root = Path(__file__).resolve().parents[2]
            vector_db_path = project_root / "data" / "vector_db"

            from src.rag.vector_store import VectorStore, RAGRetriever

            vector_store = VectorStore(
                persist_directory=str(vector_db_path), 
                collection_name="triage_medical"
            )
            retriever = RAGRetriever(vector_store=vector_store)

            st.session_state.predictor = MLTriagePredictor(rag_retriever=retriever)
            st.success("✅ Système RAG activé", icon="✅")
        except Exception as e:
            st.info("ℹ️ Mode sans RAG", icon="ℹ️")
            st.session_state.predictor = MLTriagePredictor()

    st.session_state.chatbot = TriageChatbotAPI(retriever=retriever)
    st.session_state.messages = []
    st.session_state.started = False
    st.session_state.prediction = None
    st.session_state.timeline = []

bot = st.session_state.chatbot
predictor = st.session_state.predictor
data = bot.data

# ============================================================================
# SIDEBAR ULTRA PRO
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 2rem; 
                border-radius: 20px; margin-bottom: 2rem; text-align: center;
                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
        <h2 style="color: white !important; margin: 0; font-size: 1.8rem; font-weight: 800;">
            📋 Dossier Patient
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Identité
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; 
                border-radius: 15px; margin-bottom: 1rem; backdrop-filter: blur(10px);
                border-left: 5px solid #667eea;">
        <h3 style="color: white !important; margin-bottom: 1rem; font-size: 1.3rem;">👤 Identité</h3>
    """, unsafe_allow_html=True)
    st.markdown(f"**Prénom:** {data.get('name') or '—'}")
    st.markdown(f"**Âge:** {data.get('age') or '—'} ans")
    sex = "Homme" if data.get("sex") == "H" else "Femme" if data.get("sex") == "F" else "—"
    st.markdown(f"**Sexe:** {sex}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Symptômes
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; 
                border-radius: 15px; margin-bottom: 1rem; backdrop-filter: blur(10px);
                border-left: 5px solid #f093fb;">
        <h3 style="color: white !important; margin-bottom: 1rem; font-size: 1.3rem;">🩺 Symptômes</h3>
    """, unsafe_allow_html=True)
    if data["symptoms"]:
        for s in data["symptoms"]:
            st.markdown(f"• {s}")
    else:
        st.markdown("*Aucun symptôme signalé*")
    st.markdown('</div>', unsafe_allow_html=True)

    # Constantes vitales
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; 
                border-radius: 15px; margin-bottom: 1rem; backdrop-filter: blur(10px);
                border-left: 5px solid #38ef7d;">
        <h3 style="color: white !important; margin-bottom: 1rem; font-size: 1.3rem;">📊 Constantes Vitales</h3>
    """, unsafe_allow_html=True)
    
    v = data["vitals"]
    count = len([k for k in ["Temperature", "FC", "TA_systolique", "SpO2", "FR"] if k in v])
    
    # Barre de progression premium
    progress_pct = (count / 5) * 100
    st.markdown(f"""
    <div style="margin: 1.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.8rem;">
            <span style="font-weight: 800; color: white !important; font-size: 1.1rem;">Progression</span>
            <span style="font-weight: 800; color: white !important; font-size: 1.1rem;">{count}/5</span>
        </div>
        <div class="progress-premium">
            <div class="progress-premium-bar" style="width: {progress_pct}%;">
                {progress_pct:.0f}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if v:
        if "Temperature" in v:
            temp = v['Temperature']
            temp_class = "vital-normal" if 36.1 <= temp <= 37.8 else "vital-warning" if temp <= 38.5 else "vital-critical"
            st.markdown(f'<div class="vital-badge-pro {temp_class}"><span>🌡️</span><span>{temp}°C</span></div>', unsafe_allow_html=True)
        
        if "FC" in v:
            fc = v['FC']
            fc_class = "vital-normal" if 60 <= fc <= 100 else "vital-warning" if (50 <= fc < 60 or 100 < fc <= 120) else "vital-critical"
            st.markdown(f'<div class="vital-badge-pro {fc_class}"><span>❤️</span><span>{fc} bpm</span></div>', unsafe_allow_html=True)
        
        if "TA_systolique" in v:
            ta_sys = v['TA_systolique']
            ta_dia = v.get('TA_diastolique', '?')
            ta_class = "vital-normal" if 90 <= ta_sys <= 140 else "vital-warning" if (80 <= ta_sys < 90 or 140 < ta_sys <= 160) else "vital-critical"
            st.markdown(f'<div class="vital-badge-pro {ta_class}"><span>💉</span><span>{ta_sys}/{ta_dia}</span></div>', unsafe_allow_html=True)
        
        if "SpO2" in v:
            spo2 = v['SpO2']
            spo2_class = "vital-normal" if spo2 >= 95 else "vital-warning" if 90 <= spo2 < 95 else "vital-critical"
            st.markdown(f'<div class="vital-badge-pro {spo2_class}"><span>🫁</span><span>{spo2}%</span></div>', unsafe_allow_html=True)
        
        if "FR" in v:
            fr = v['FR']
            fr_class = "vital-normal" if 12 <= fr <= 20 else "vital-warning" if (10 <= fr < 12 or 20 < fr <= 25) else "vital-critical"
            st.markdown(f'<div class="vital-badge-pro {fr_class}"><span>🌬️</span><span>{fr}/min</span></div>', unsafe_allow_html=True)
    else:
        st.info("*En attente de mesures...*")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Nouveau Patient", use_container_width=True):
            bot.reset()
            st.session_state.messages = []
            st.session_state.started = False
            st.session_state.prediction = None
            st.session_state.timeline = []
            st.rerun()

    ready = bot.is_ready_for_prediction()

    with col2:
        if st.button(
            "🎯 Prédire Gravité",
            use_container_width=True,
            disabled=not ready,
            type="primary" if ready else "secondary"
        ):
            with st.spinner("🔮 Analyse ML en cours..."):
                summary = bot.get_summary()
                st.session_state.prediction = predictor.predict(summary)
            st.balloons()
            st.success("✅ Analyse terminée!", icon="✅")
            st.rerun()

    if not ready:
        st.caption("⚠️ Collectez les 5 constantes vitales")

# ============================================================================
# LAYOUT PRINCIPAL - 2 COLONNES
# ============================================================================
col_chat, col_prediction = st.columns([2.5, 1.5])

# ============================================================================
# COLONNE GAUCHE - CONVERSATION
# ============================================================================
with col_chat:
    st.markdown('<div class="premium-card animated">', unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style="color: #1a1a2e !important; margin-bottom: 1.5rem; font-size: 1.8rem; font-weight: 800;">
        💬 Conversation de Triage
    </h3>
    """, unsafe_allow_html=True)
    
    if not st.session_state.started:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 3rem; border-radius: 25px; text-align: center;
                    box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
                    color: white; margin: 2rem 0;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🚀</div>
            <h4 style="color: white !important; margin-bottom: 1rem; font-size: 1.8rem; font-weight: 800;">
                Prêt à Commencer ?
            </h4>
            <p style="color: white !important; font-size: 1.1rem; opacity: 0.95;">
                Cliquez sur le bouton ci-dessous pour démarrer l'entretien de triage
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Démarrer l'Entretien", use_container_width=True, type="primary"):
            msg = bot.start()
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.session_state.started = True
            st.session_state.timeline.append({"type": "start", "time": "now"})
            st.rerun()
    else:
        # Zone messages avec style premium
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for idx, m in enumerate(st.session_state.messages):
            if m["role"] == "user":
                st.markdown(f"""
                <div class="message-user">
                    {m["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-assistant">
                    {m["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# COLONNE DROITE - PRÉDICTION
# ============================================================================
with col_prediction:
    st.markdown("""
    <h3 style="color: #1a1a2e !important; margin-bottom: 1.5rem; font-size: 1.8rem; font-weight: 800;">
        🎯 Analyse ML
    </h3>
    """, unsafe_allow_html=True)

    if st.session_state.prediction:
        r = st.session_state.prediction

        # Badge niveau spectaculaire
        pred_class = f"pred-{r['severity_level'].lower()}"
        
        st.markdown(f"""
        <div class="prediction-spectacle {pred_class}">
            <div style="font-size: 4.5rem; margin-bottom: 1rem; position: relative; z-index: 1;">
                {'🔴' if r['severity_level']=='ROUGE' else '🟡' if r['severity_level']=='JAUNE' else '🟢' if r['severity_level']=='VERT' else '⚪'}
            </div>
            <div style="font-size: 2.5rem; font-weight: 900; margin-bottom: 0.5rem; position: relative; z-index: 1;">
                {r['label']}
            </div>
            <div style="font-size: 1.1rem; opacity: 0.95; position: relative; z-index: 1;">
                {r['action'][:50]}...
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Action complète
        st.markdown(f"""
        <div class="premium-card" style="border-left: 5px solid {r['color']}; margin-bottom: 1.5rem;">
            <h4 style="color: #1a1a2e !important; margin-bottom: 1rem; font-size: 1.3rem; font-weight: 700;">
                📋 Action Recommandée
            </h4>
            <p style="margin: 0; color: #2d3436 !important; font-size: 1.05rem; line-height: 1.6;">
                {r['action']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Drapeaux rouges
        if r.get("red_flags"):
            st.markdown("""
            <div class="premium-card" style="background: linear-gradient(135deg, rgba(235, 51, 73, 0.1) 0%, rgba(244, 92, 67, 0.1) 100%);
                        border-left: 5px solid #eb3349; margin-bottom: 1.5rem;">
                <h4 style="color: #eb3349 !important; margin-bottom: 1rem; font-size: 1.3rem; font-weight: 700;">
                    ⚠️ Signes de Gravité
                </h4>
            """, unsafe_allow_html=True)
            for flag in r["red_flags"]:
                st.markdown(f"🚨 {flag}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Probabilités avec animation
        st.markdown("#### 📊 Distribution des Probabilités")
        
        severity_colors_map = {
            "ROUGE": "#eb3349",
            "JAUNE": "#f2994a",
            "VERT": "#11998e",
            "GRIS": "#757f9a"
        }
        
        for lvl in ["ROUGE", "JAUNE", "VERT", "GRIS"]:
            p = r["probabilities"].get(lvl, 0)
            color = severity_colors_map.get(lvl, '#757f9a')
            
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-weight: 700; color: #1a1a2e !important; font-size: 1.05rem;">
                        {lvl}
                    </span>
                    <span style="font-weight: 800; color: {color} !important; font-size: 1.1rem;">
                        {p*100:.1f}%
                    </span>
                </div>
                <div class="confidence-meter">
                    <div class="confidence-fill" style="width: {p*100}%; background: linear-gradient(90deg, {color} 0%, {color}dd 100%);">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Confiance spectaculaire
        conf_color = "#11998e" if r['confidence'] > 0.8 else "#f2994a" if r['confidence'] > 0.6 else "#eb3349"
        
        st.markdown(f"""
        <div class="prediction-spectacle" style="background: linear-gradient(135deg, {conf_color} 0%, {conf_color}dd 100%);
                    margin-top: 2rem; animation: none;">
            <div style="font-size: 3.5rem; font-weight: 900; margin-bottom: 0.5rem; position: relative; z-index: 1;">
                {r['confidence']*100:.1f}%
            </div>
            <div style="font-size: 1.2rem; opacity: 0.95; font-weight: 600; position: relative; z-index: 1;">
                Niveau de Confiance
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Détails techniques
        with st.expander("🔬 Détails Techniques ML", expanded=False):
            if r.get("features_used"):
                st.json(r["features_used"])

        with st.expander("📚 Sources RAG", expanded=False):
            if r.get("rag_sources"):
                for source in r["rag_sources"]:
                    st.markdown(f"• {source}")
            else:
                st.info("Aucune source RAG disponible")

        with st.expander("📋 Justification Médicale", expanded=True):
            st.markdown(r["justification"])

        # Export rapport
        st.markdown("---")
        if st.button("💾 Exporter le Rapport Complet", use_container_width=True, type="primary"):
            export = f"# 📋 RAPPORT DE TRIAGE MÉDICAL\n\n"
            export += f"## {r['label']}\n\n"
            export += f"**Action Recommandée:** {r['action']}\n"
            export += f"**Niveau de Confiance:** {r['confidence']*100:.1f}%\n\n"

            export += "### 👤 Patient\n\n"
            export += f"- Prénom: {data.get('name') or '—'}\n"
            export += f"- Âge: {data.get('age') or '—'} ans\n"
            export += f"- Sexe: {sex}\n\n"

            if data["symptoms"]:
                export += "### 🩺 Symptômes\n\n"
                for s in data["symptoms"]:
                    export += f"- {s}\n"
                export += "\n"

            if v:
                export += "### 📊 Constantes Vitales\n\n"
                for k, val in v.items():
                    export += f"- {k}: {val}\n"
                export += "\n"

            if r.get("red_flags"):
                export += "### ⚠️ Drapeaux Rouges\n\n"
                for flag in r["red_flags"]:
                    export += f"- {flag}\n"
                export += "\n"

            export += "### 💬 Historique de Conversation\n\n"
            for m in st.session_state.messages:
                role = "Infirmier" if m["role"] == "user" else "Assistant IA"
                export += f"**{role}:** {m['content']}\n\n"

            export += f"\n### 📊 Probabilités ML\n\n"
            for lvl, prob in r["probabilities"].items():
                export += f"- {lvl}: {prob*100:.1f}%\n"

            st.download_button(
                "📥 Télécharger le Rapport (Markdown)",
                export,
                "rapport_triage.md",
                "text/markdown",
                use_container_width=True,
            )
    else:
        st.markdown("""
        <div class="premium-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🤖</div>
            <h4 style="color: #1a1a2e !important; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 700;">
                En Attente de Données
            </h4>
            <p style="color: #636e72 !important; line-height: 1.8; font-size: 1.05rem;">
                Complétez la conversation en collectant les <strong>5 constantes vitales</strong> 
                puis cliquez sur <strong>"Prédire Gravité"</strong> dans le panneau latéral.
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("❓ Guide d'Utilisation", expanded=False):
            st.markdown("""
            ### 📋 Constantes Vitales Requises (5/5)
            
            1. 🌡️ **Température** corporelle
            2. ❤️ **Fréquence cardiaque** (FC)
            3. 💉 **Tension artérielle** (TA)
            4. 🫁 **Saturation en oxygène** (SpO2)
            5. 🌬️ **Fréquence respiratoire** (FR)
            
            ### 💡 Conseils
            
            - L'assistant IA vous guidera étape par étape
            - Répondez aux questions de manière précise
            - Les constantes seront extraites automatiquement
            - La prédiction ML sera instantanée une fois les 5/5 collectées
            """)

# ============================================================================
# CHAT INPUT - EN DEHORS DES COLONNES (CRITIQUE!)
# ============================================================================
if st.session_state.started and not st.session_state.prediction:
    user_input = st.chat_input("💭 Tapez votre message ici...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.timeline.append({"type": "user_message", "time": "now"})
        
        with st.spinner("🤔 L'assistant IA analyse votre réponse..."):
            response = bot.chat(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.timeline.append({"type": "assistant_message", "time": "now"})
        
        st.rerun()

# ============================================================================
# FOOTER PROFESSIONNEL
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 25px; color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);'>
    <p style='font-size: 1.3rem; font-weight: 800; margin-bottom: 0.8rem; color: white !important;
              text-shadow: 0 2px 5px rgba(0,0,0,0.2);'>
        🤖 Intelligence Artificielle • 📊 Machine Learning • 📚 RAG System
    </p>
    <p style='font-size: 1rem; opacity: 0.95; margin: 0; color: white !important;'>
        Propulsé par <strong>Mistral AI</strong> • <strong>Random Forest</strong> • <strong>ChromaDB</strong>
    </p>
    <p style='font-size: 0.85rem; opacity: 0.8; margin-top: 1rem; color: white !important;'>
        ⚠️ Outil d'aide à la décision médicale - Ne remplace pas l'avis d'un professionnel de santé
    </p>
</div>
""", unsafe_allow_html=True)