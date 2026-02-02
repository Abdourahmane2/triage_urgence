import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Triage Urgences - IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Header
st.title("🏥 Système de Triage Intelligent aux Urgences")
st.caption("Propulsé par l'Intelligence Artificielle pour optimiser la prise en charge des patients")

st.divider()

# Stats rapides
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Temps Réel",
        value="Instantané",
        delta="Analyse rapide"
    )

with col2:
    st.metric(
        label="IA Avancée",
        value="Mistral AI",
        delta="Modèle LLM"
    )

with col3:
    st.metric(
        label="ML Intégré",
        value="Random Forest",
        delta="Classification"
    )

with col4:
    st.metric(
        label="Sécurisé",
        value="100%",
        delta="Protection données"
    )

st.divider()

# Fonctionnalités principales
st.header("Fonctionnalités Principales")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎲 Génération Automatique")
    st.write("Générez des conversations réalistes entre infirmier et patient.")
    with st.expander("Voir les détails"):
        st.write("• Patients IA réalistes")
        st.write("• Extraction automatique")
        st.write("• Export ML-ready")
        st.write("• Génération rapide")

with col2:
    st.subheader("💬 Chat Interactif")
    st.write("Menez vos propres conversations de triage en temps réel.")
    with st.expander("Voir les détails"):
        st.write("• IA conversationnelle")
        st.write("• Suivi des constantes")
        st.write("• Prédiction ML")
        st.write("• Export de rapport")

with col3:
    st.subheader("📊 Monitoring Avancé")
    st.write("Suivez les performances et analytics en temps réel.")
    with st.expander("Voir les détails"):
        st.write("• Suivi des coûts")
        st.write("• Métriques performances")
        st.write("• Analytics détaillés")
        st.write("• Export CSV/JSON")

st.divider()

# Comment ça fonctionne
st.header("Comment ça fonctionne")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1️⃣ Génération Patient")
    st.write("L'IA crée un patient réaliste avec symptômes et constantes cohérentes")

with col2:
    st.subheader("2️⃣ Conversation")
    st.write("Dialogue naturel pour collecter informations médicales essentielles")

with col3:
    st.subheader("3️⃣ Extraction")
    st.write("Analyse automatique et structuration des données médicales")

with col4:
    st.subheader("4️⃣ Prédiction ML")
    st.write("Classification automatique du niveau de gravité")

st.divider()

# Technologies
st.header("Technologies Utilisées")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 Intelligence Artificielle")
    st.write("**Mistral AI** - Modèle de langage pour conversations naturelles")
    st.write("**Random Forest** - Algorithme ML pour classification")
    st.write("**RAG System** - ChromaDB pour réponses médicales précises")

with col2:
    st.subheader("⚙️ Infrastructure")
    st.write("**Streamlit** - Interface utilisateur moderne")
    st.write("**Python** - Langage principal avec libraries scientifiques")
    st.write("**Plotly** - Visualisations interactives")

st.divider()

# Call to action
st.success("🚀 Prêt à commencer ? Sélectionnez une fonctionnalité dans la barre latérale pour démarrer")

# Sidebar
with st.sidebar:
    st.header("📱 Navigation")
    
    st.info("**🎲 Génération**\n\nCréez des conversations automatiques")
    st.info("**💬 Chat Interactif**\n\nMode conversation manuelle")
    st.info("**📊 Monitoring**\n\nAnalytics et performances")
    
    st.divider()
    
    st.subheader("ℹ️ À propos")
    st.caption("Application développée pour optimiser le triage médical aux urgences grâce à l'intelligence artificielle.")
    st.caption("**Version:** 1.0.0")
    st.caption("**Framework:** Streamlit")
    st.caption("**IA:** Mistral AI")

# Footer
st.divider()
st.info("⚠️ **Important:** Outil d'aide à la décision - Ne remplace pas un avis médical professionnel")
st.caption("🏥 Système de Triage Intelligent - 2025 • Propulsé par Mistral AI, Streamlit & Machine Learning")