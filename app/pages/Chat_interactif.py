import streamlit as st
from pathlib import Path
import sys
import warnings

# Supprimer les warnings sklearn
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.rag.chatbot import TriageChatbotLLM
from src.rag.predictor import MLTriagePredictor

# Configuration
st.set_page_config(
    page_title="Chat Triage Pro", 
    page_icon="💬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("💬 Assistant IA de Triage Médical")
st.caption("Analyse Intelligente • Prédiction ML • Aide à la Décision en Temps Réel")

st.divider()

# Session State
if "chatbot" not in st.session_state:
    retriever = None
    with st.spinner("Initialisation du système..."):
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
            #st.success("Système RAG activé")
        except Exception as e:
            st.info("Mode sans RAG")
            st.session_state.predictor = MLTriagePredictor()

    st.session_state.chatbot = TriageChatbotLLM(retriever=retriever)
    st.session_state.messages = []
    st.session_state.started = False
    st.session_state.prediction = None

bot = st.session_state.chatbot
predictor = st.session_state.predictor
data = bot.data

# Sidebar - Dossier Patient
with st.sidebar:
    st.header("📋 Dossier Patient")
    
    # Identité
    with st.expander("👤 Identité", expanded=True):
        st.write(f"**Prénom:** {data.get('name') or '—'}")
        st.write(f"**Âge:** {data.get('age') or '—'} ans")
        sex = "Homme" if data.get("sex") == "H" else "Femme" if data.get("sex") == "F" else "—"
        st.write(f"**Sexe:** {sex}")

    # Symptômes
    with st.expander("🩺 Symptômes", expanded=True):
        if data["symptoms"]:
            for s in data["symptoms"]:
                st.write(f"• {s}")
        else:
            st.caption("Aucun symptôme signalé")

    # Constantes vitales
    with st.expander("📊 Constantes Vitales", expanded=True):
        v = data["vitals"]
        count = len([k for k in ["Temperature", "FC", "TA_systolique", "SpO2", "FR"] if k in v])
        
        st.progress(count / 5, text=f"Progression: {count}/5")
        
        if v:
            if "Temperature" in v:
                temp = v['Temperature']
                temp_status = "🟢" if 36.1 <= temp <= 37.8 else "🟡" if temp <= 38.5 else "🔴"
                st.write(f"{temp_status} Température: {temp}°C")
            
            if "FC" in v:
                fc = v['FC']
                fc_status = "🟢" if 60 <= fc <= 100 else "🟡" if (50 <= fc < 60 or 100 < fc <= 120) else "🔴"
                st.write(f"{fc_status} Fréquence cardiaque: {fc} bpm")
            
            if "TA_systolique" in v:
                ta_sys = v['TA_systolique']
                ta_dia = v.get('TA_diastolique', '?')
                ta_status = "🟢" if 90 <= ta_sys <= 140 else "🟡" if (80 <= ta_sys < 90 or 140 < ta_sys <= 160) else "🔴"
                st.write(f"{ta_status} Tension: {ta_sys}/{ta_dia} mmHg")
            
            if "SpO2" in v:
                spo2 = v['SpO2']
                spo2_status = "🟢" if spo2 >= 95 else "🟡" if 90 <= spo2 < 95 else "🔴"
                st.write(f"{spo2_status} SpO2: {spo2}%")
            
            if "FR" in v:
                fr = v['FR']
                fr_status = "🟢" if 12 <= fr <= 20 else "🟡" if (10 <= fr < 12 or 20 < fr <= 25) else "🔴"
                st.write(f"{fr_status} Fréquence respiratoire: {fr}/min")
        else:
            st.caption("En attente de mesures...")

    st.divider()

    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Nouveau", use_container_width=True):
            bot.reset()
            st.session_state.messages = []
            st.session_state.started = False
            st.session_state.prediction = None
            st.rerun()

    ready = bot.is_ready_for_prediction()

    with col2:
        if st.button(
            "🎯 Prédire",
            use_container_width=True,
            disabled=not ready,
            type="primary" if ready else "secondary"
        ):
            with st.spinner("Analyse ML en cours..."):
                summary = bot.get_summary()
                st.session_state.prediction = predictor.predict(summary)
            st.balloons()
            st.success("Analyse terminée!")
            st.rerun()

    if not ready:
        st.caption("⚠️ Collectez les 5 constantes vitales")

# Layout principal - 2 colonnes
col_chat, col_prediction = st.columns([2.5, 1.5])

# Colonne gauche - Conversation
with col_chat:
    st.subheader("💬 Conversation de Triage")
    
    if not st.session_state.started:
        st.info("Cliquez sur le bouton ci-dessous pour démarrer l'entretien de triage")
        
        if st.button("🚀 Démarrer l'Entretien", use_container_width=True, type="primary"):
            msg = bot.start()
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.session_state.started = True
            st.rerun()
    else:
        # Zone messages
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.write(m["content"])

# Colonne droite - Prédiction
with col_prediction:
    st.subheader("🎯 Analyse ML")

    if st.session_state.prediction:
        r = st.session_state.prediction

        # Badge niveau de gravité
        severity_colors = {
            "ROUGE": "🔴",
            "JAUNE": "🟡",
            "VERT": "🟢",
            "GRIS": "⚪"
        }
        
        severity_emoji = severity_colors.get(r['severity_level'], "⚪")
        
        st.success(f"{severity_emoji} **Niveau: {r['label']}**")
        st.metric("Confiance", f"{r['confidence']*100:.1f}%")

        st.divider()

        # Action recommandée
        st.write("**📋 Action Recommandée**")
        st.info(r['action'])

        # Drapeaux rouges
        if r.get("red_flags"):
            st.write("**⚠️ Signes de Gravité**")
            for flag in r["red_flags"]:
                st.warning(f"• {flag}")

        st.divider()

        # Probabilités
        st.write("**📊 Probabilités**")
        for lvl in ["ROUGE", "JAUNE", "VERT", "GRIS"]:
            p = r["probabilities"].get(lvl, 0)
            st.progress(p, text=f"{lvl}: {p*100:.1f}%")

        st.divider()

        # Détails techniques
        with st.expander("🔬 Détails Techniques"):
            if r.get("features_used"):
                st.json(r["features_used"])

        with st.expander("📚 Sources RAG"):
            if r.get("rag_sources"):
                for source in r["rag_sources"]:
                    st.write(f"• {source}")
            else:
                st.caption("Aucune source RAG disponible")

        with st.expander("📋 Justification Médicale", expanded=True):
            st.write(r["justification"])

        st.divider()

        # Export rapport
        if st.button("💾 Exporter le Rapport", use_container_width=True, type="primary"):
            export = f"# RAPPORT DE TRIAGE MÉDICAL\n\n"
            export += f"## {r['label']}\n\n"
            export += f"**Action:** {r['action']}\n"
            export += f"**Confiance:** {r['confidence']*100:.1f}%\n\n"

            export += "### Patient\n\n"
            export += f"- Prénom: {data.get('name') or '—'}\n"
            export += f"- Âge: {data.get('age') or '—'} ans\n"
            export += f"- Sexe: {sex}\n\n"

            if data["symptoms"]:
                export += "### Symptômes\n\n"
                for s in data["symptoms"]:
                    export += f"- {s}\n"
                export += "\n"

            if v:
                export += "### Constantes Vitales\n\n"
                for k, val in v.items():
                    export += f"- {k}: {val}\n"
                export += "\n"

            if r.get("red_flags"):
                export += "### Drapeaux Rouges\n\n"
                for flag in r["red_flags"]:
                    export += f"- {flag}\n"
                export += "\n"

            export += "### Historique\n\n"
            for m in st.session_state.messages:
                role = "Infirmier" if m["role"] == "user" else "Assistant IA"
                export += f"**{role}:** {m['content']}\n\n"

            export += f"\n### Probabilités ML\n\n"
            for lvl, prob in r["probabilities"].items():
                export += f"- {lvl}: {prob*100:.1f}%\n"

            st.download_button(
                "📥 Télécharger (Markdown)",
                export,
                "rapport_triage.md",
                "text/markdown",
                use_container_width=True,
            )
    else:
        st.info("**En Attente de Données**\n\nComplétez la conversation en collectant les 5 constantes vitales puis cliquez sur 'Prédire Gravité'")

        with st.expander("❓ Guide d'Utilisation"):
            st.write("**Constantes Vitales Requises (5/5)**")
            st.write("1. Température corporelle")
            st.write("2. Fréquence cardiaque (FC)")
            st.write("3. Tension artérielle (TA)")
            st.write("4. Saturation en oxygène (SpO2)")
            st.write("5. Fréquence respiratoire (FR)")

# Chat input
if st.session_state.started and not st.session_state.prediction:
    user_input = st.chat_input("Tapez votre message ici...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("L'assistant IA analyse votre réponse..."):
            response = bot.chat(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Footer