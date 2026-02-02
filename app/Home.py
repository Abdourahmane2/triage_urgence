"""
Page d'accueil - Application de triage des urgences.
Design moderne et professionnel - VERSION CORRIGÉE
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Triage Urgences - IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS COMPLET - Tout en un
st.markdown("""
<style>
/* ===== FOND GLOBAL ===== */
.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

/* ===== SIDEBAR MODERNE ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Navigation items */
[data-testid="stSidebar"] .css-1v0mbdj a,
[data-testid="stSidebar"] button {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    margin: 0.3rem 0 !important;
    transition: all 0.3s ease !important;
    border: none !important;
}

[data-testid="stSidebar"] .css-1v0mbdj a:hover,
[data-testid="stSidebar"] button:hover {
    background: rgba(255, 255, 255, 0.2) !important;
    transform: translateX(5px) !important;
}

/* Headers dans sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ===== BOUTONS STREAMLIT ===== */
.stButton button {
    background: linear-gradient(135deg, #0066cc 0%, #3385d6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3) !important;
}

.stButton button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 16px rgba(0, 102, 204, 0.4) !important;
}

/* ===== ANIMATIONS ===== */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animated {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.03);
    }
}

/* ===== CACHE LE CODE ===== */
code {
    display: none !important;
}

pre {
    display: none !important;
}

/* ===== TITRES ===== */
h1 {
    color: #1e3a8a !important;
    font-weight: 800 !important;
}

h2 {
    color: #1e40af !important;
    font-weight: 700 !important;
}

h3 {
    color: #2563eb !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER PRINCIPAL =====
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;"
            class="animated">
    <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem; color: white !important;">
        🏥 Système de Triage Intelligent aux Urgences
    </h1>
    <p style="font-size: 1.3rem; margin: 0; opacity: 0.95;">
        Propulsé par l'Intelligence Artificielle pour optimiser la prise en charge des patients
    </p>
</div>
""", unsafe_allow_html=True)

# ===== STATS RAPIDES =====
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0066cc 0%, #3385d6 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3);"
                class="animated">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">⚡</div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">Temps Réel</div>
        <div style="font-size: 0.95rem; opacity: 0.9;">Analyse instantanée</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #28a745 0%, #48c774 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);"
                class="animated">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">IA Avancée</div>
        <div style="font-size: 0.95rem; opacity: 0.9;">Mistral AI</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffc107 0%, #ffab00 100%);
                color: #212529;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 6px 20px rgba(255, 193, 7, 0.3);"
                class="animated">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">ML Intégré</div>
        <div style="font-size: 0.95rem; opacity: 0.9;">Random Forest</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 6px 20px rgba(220, 53, 69, 0.3);"
                class="animated">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔒</div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">Sécurisé</div>
        <div style="font-size: 0.95rem; opacity: 0.9;">Données protégées</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)


st.markdown("""
<h2 style="text-align: center; color: #1e3a8a; font-size: 2.5rem; margin-bottom: 2rem;">
    🎯 Fonctionnalités Principales
</h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white;
                border-radius: 15px;
                padding: 2.5rem;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border: 2px solid transparent;
                height: 100%;"
                class="animated">
        <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">🎲</div>
        <h3 style="color: #1e3a8a; text-align: center; margin-bottom: 1.5rem; font-size: 1.5rem;">
            Génération Automatique
        </h3>
        <p style="color: #6c757d; line-height: 1.8; text-align: center; font-size: 1rem;">
            Générez des conversations réalistes entre infirmier et patient. 
            Extraction automatique des constantes vitales et symptômes.
        </p>
        <ul style="text-align: left; color: #495057; margin-top: 1.5rem; line-height: 2;">
            <li><strong>✨ Patients IA réalistes</strong></li>
            <li><strong>📋 Extraction automatique</strong></li>
            <li><strong>💾 Export ML-ready</strong></li>
            <li><strong>⚡ Génération rapide</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white;
                border-radius: 15px;
                padding: 2.5rem;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border: 2px solid transparent;
                height: 100%;"
                class="animated">
        <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">💬</div>
        <h3 style="color: #1e3a8a; text-align: center; margin-bottom: 1.5rem; font-size: 1.5rem;">
            Chat Interactif
        </h3>
        <p style="color: #6c757d; line-height: 1.8; text-align: center; font-size: 1rem;">
            Menez vos propres conversations de triage. L'IA patient répond 
            en temps réel à vos questions médicales.
        </p>
        <ul style="text-align: left; color: #495057; margin-top: 1.5rem; line-height: 2;">
            <li><strong>🤖 IA conversationnelle</strong></li>
            <li><strong>🩺 Suivi des constantes</strong></li>
            <li><strong>🎯 Prédiction ML</strong></li>
            <li><strong>📄 Export de rapport</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white;
                border-radius: 15px;
                padding: 2.5rem;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border: 2px solid transparent;
                height: 100%;"
                class="animated">
        <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">📊</div>
        <h3 style="color: #1e3a8a; text-align: center; margin-bottom: 1.5rem; font-size: 1.5rem;">
            Monitoring Avancé
        </h3>
        <p style="color: #6c757d; line-height: 1.8; text-align: center; font-size: 1rem;">
            Suivez les performances, coûts API et analytics en temps réel. 
            Tableaux de bord interactifs.
        </p>
        <ul style="text-align: left; color: #495057; margin-top: 1.5rem; line-height: 2;">
            <li><strong>💰 Suivi des coûts</strong></li>
            <li><strong>⚡ Métriques performances</strong></li>
            <li><strong>📈 Analytics détaillés</strong></li>
            <li><strong>💾 Export CSV/JSON</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ===== COMMENT ÇA FONCTIONNE =====
st.markdown("""
<h2 style="text-align: center; color: #1e3a8a; font-size: 2.5rem; margin-bottom: 2rem;">
    🔄 Comment ça fonctionne ?
</h2>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);"
                class="animated">
        <div style="font-size: 4rem; margin-bottom: 1rem;">1️⃣</div>
        <h4 style="color: #1e3a8a; margin-bottom: 1rem; font-size: 1.3rem;">Génération Patient</h4>
        <p style="color: #6c757d; font-size: 0.95rem; line-height: 1.6;">
            L'IA crée un patient réaliste avec symptômes et constantes cohérentes
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);"
                class="animated">
        <div style="font-size: 4rem; margin-bottom: 1rem;">2️⃣</div>
        <h4 style="color: #1e3a8a; margin-bottom: 1rem; font-size: 1.3rem;">Conversation</h4>
        <p style="color: #6c757d; font-size: 0.95rem; line-height: 1.6;">
            Dialogue naturel pour collecter informations médicales essentielles
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);"
                class="animated">
        <div style="font-size: 4rem; margin-bottom: 1rem;">3️⃣</div>
        <h4 style="color: #1e3a8a; margin-bottom: 1rem; font-size: 1.3rem;">Extraction</h4>
        <p style="color: #6c757d; font-size: 0.95rem; line-height: 1.6;">
            Analyse automatique et structuration des données médicales
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);"
                class="animated">
        <div style="font-size: 4rem; margin-bottom: 1rem;">4️⃣</div>
        <h4 style="color: #1e3a8a; margin-bottom: 1rem; font-size: 1.3rem;">Prédiction ML</h4>
        <p style="color: #6c757d; font-size: 0.95rem; line-height: 1.6;">
            Classification automatique du niveau de gravité
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ===== TECHNOLOGIES =====
st.markdown("""
<h2 style="text-align: center; color: #1e3a8a; font-size: 2.5rem; margin-bottom: 2rem;">
    🛠️ Technologies Utilisées
</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: white;
                padding: 2.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                height: 100%;"
                class="animated">
        <h3 style="color: #1e3a8a; margin-bottom: 2rem; font-size: 1.8rem;">🤖 Intelligence Artificielle</h3>
        
        <div style="margin-bottom: 1.5rem;">
            <h4 style="color: #0066cc; margin-bottom: 0.5rem; font-size: 1.2rem;">🧠 Mistral AI</h4>
            <p style="color: #6c757d; margin: 0; line-height: 1.6;">
                Modèle de langage pour conversations naturelles et extraction d'informations
            </p>
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <h4 style="color: #0066cc; margin-bottom: 0.5rem; font-size: 1.2rem;">🌲 Random Forest</h4>
            <p style="color: #6c757d; margin: 0; line-height: 1.6;">
                Algorithme ML pour classification du niveau de gravité
            </p>
        </div>
        
        <div>
            <h4 style="color: #0066cc; margin-bottom: 0.5rem; font-size: 1.2rem;">📚 RAG System</h4>
            <p style="color: #6c757d; margin: 0; line-height: 1.6;">
                Retrieval Augmented Generation avec ChromaDB pour réponses médicales précises
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white;
                padding: 2.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                height: 100%;"
                class="animated">
        <h3 style="color: #1e3a8a; margin-bottom: 2rem; font-size: 1.8rem;">⚙️ Infrastructure</h3>
        
        <div style="margin-bottom: 1.5rem;">
            <h4 style="color: #0066cc; margin-bottom: 0.5rem; font-size: 1.2rem;">🎨 Streamlit</h4>
            <p style="color: #6c757d; margin: 0; line-height: 1.6;">
                Framework web pour interface utilisateur moderne et réactive
            </p>
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <h4 style="color: #0066cc; margin-bottom: 0.5rem; font-size: 1.2rem;">🐍 Python</h4>
            <p style="color: #6c757d; margin: 0; line-height: 1.6;">
                Langage principal avec libraries scientifiques (pandas, numpy, scikit-learn)
            </p>
        </div>
        
        <div>
            <h4 style="color: #0066cc; margin-bottom: 0.5rem; font-size: 1.2rem;">📊 Plotly</h4>
            <p style="color: #6c757d; margin: 0; line-height: 1.6;">
                Visualisations interactives pour analytics et monitoring
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ===== CTA =====
st.markdown("""
<div style="background: linear-gradient(135deg, #28a745 0%, #48c774 100%);
            color: white;
            padding: 3.5rem 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(40, 167, 69, 0.3);"
            class="animated">
    <h2 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 1.5rem; color: white !important;">
        🚀 Prêt à commencer ?
    </h2>
    <p style="font-size: 1.3rem; margin-bottom: 2rem; opacity: 0.95;">
        Sélectionnez une fonctionnalité dans la barre latérale pour démarrer
    </p>
    <div style="background: white;
                color: #28a745;
                display: inline-block;
                padding: 1rem 2.5rem;
                border-radius: 12px;
                font-weight: 700;
                font-size: 1.2rem;">
        👈 Utilisez le menu à gauche
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.15);
                padding: 1.5rem;
                border-radius: 12px;
                margin: 1rem 0;">
        <h3 style="color: white !important; margin-bottom: 1rem; font-size: 1.3rem;">📱 Navigation</h3>
        <div style="background: rgba(255,255,255,0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;">
            <p style="margin: 0.5rem 0; color: white !important;">
                <strong style="font-size: 1.1rem;">🎲 Génération</strong><br>
                <small style="opacity: 0.9;">Créez des conversations automatiques</small>
            </p>
        </div>
        
        <div style="background: rgba(255,255,255,0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;">
            <p style="margin: 0.5rem 0; color: white !important;">
                <strong style="font-size: 1.1rem;">💬 Chat Interactif</strong><br>
                <small style="opacity: 0.9;">Mode conversation manuelle</small>
            </p>
        </div>
        
        <div style="background: rgba(255,255,255,0.1);
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;">
            <p style="margin: 0.5rem 0; color: white !important;">
                <strong style="font-size: 1.1rem;">📊 Monitoring</strong><br>
                <small style="opacity: 0.9;">Analytics et performances</small>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem;">
        <h4 style="color: white !important; margin-bottom: 1rem;">ℹ️ À propos</h4>
        <p style="font-size: 0.9rem; line-height: 1.6; opacity: 0.9; color: white !important;">
            Application développée pour optimiser le triage médical aux urgences 
            grâce à l'intelligence artificielle.
        </p>
        <div style="margin-top: 1.5rem; font-size: 0.85rem; opacity: 0.85; color: white !important;">
            <strong>Version:</strong> 1.0.0<br>
            <strong>Framework:</strong> Streamlit<br>
            <strong>IA:</strong> Mistral AI
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center;
            padding: 2.5rem;
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            border-radius: 15px;
            color: white;'>
    <p style='font-size: 1.2rem; font-weight: 700; margin-bottom: 0.8rem;'>
        🏥 Système de Triage Intelligent - 2025
    </p>
    <p style='font-size: 1rem; opacity: 0.95; margin: 0.5rem 0;'>
        Propulsé par Mistral AI • Streamlit • Machine Learning
    </p>
    <p style='font-size: 0.85rem; opacity: 0.8; margin-top: 1.5rem;'>
        ⚠️ Outil d'aide à la décision - Ne remplace pas un avis médical professionnel
    </p>
</div>
""", unsafe_allow_html=True)
