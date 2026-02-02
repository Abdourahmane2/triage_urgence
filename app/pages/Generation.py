# Standard library imports
import json
import sys
from pathlib import Path

# Third-party imports
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Ajouter le chemin src au PYTHONPATH
root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_path))

# Local imports
from src.llm.llm_factory import LLMFactory
from src.workflows.simulation_workflow import SimulationWorkflow

# Configuration
st.set_page_config(page_title="Génération", page_icon="🎲", layout="wide")

# Header
st.title("🎲 Génération de Conversations IA")
st.caption("Créez des datasets • Prédiction ML • Analytics")
# Session State
if "conversations" not in st.session_state:
    st.session_state.conversations = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "current_prediction" not in st.session_state:
    st.session_state.current_prediction = None


        
    if st.session_state.conversations:
        st.metric("Total conversations", len(st.session_state.conversations))
    
    st.info("💡 **Astuce**\n\nLaissez vide pour génération aléatoire")

# Configuration
st.subheader("📝 Configuration")

pathology_input = st.text_input(
    "Pathologie (optionnel)",
    placeholder="Ex: Homme de 65 ans avec suspicion d'infarctus",
    help="Laissez vide pour aléatoire"
)


# Boutons d'action
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    generate_one = st.button("🎲 Générer 1", type="primary", use_container_width=True)

clear_dataset = False

with col_btn3:
    if st.session_state.conversations:
        clear_dataset = st.button("🗑️ Effacer", use_container_width=True)

# Génération 1 conversation
if generate_one:
    with st.spinner("Génération en cours..."):
        try:
            llm = LLMFactory.create("mistral", "mistral-large-latest")
            workflow = SimulationWorkflow(llm, max_turns=20)  
            
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
            st.session_state.current_prediction = None
            
            st.success(f"✅ Générée en {duration:.2f}s!")
            st.balloons()
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")

# Effacer
if st.session_state.conversations and clear_dataset:
    st.session_state.conversations = []
    st.session_state.current_result = None
    st.session_state.current_prediction = None
    st.success("✅ Effacé")
    st.rerun()

st.divider()

# ============================================================================
# AFFICHAGE EN 2 COLONNES : Conversation + Prédiction côte à côte
# ============================================================================
if st.session_state.current_result:
    result = st.session_state.current_result
    
    st.header("📋 Résultat")
    
    # Layout 2 colonnes principales
    col_left, col_right = st.columns([1.5, 1])
    
    # ========== COLONNE GAUCHE : Conversation & Infos ==========
    with col_left:
        st.info(f"**Pathologie:** {result['pathology']}")
        
        extr = result["extracted_patient"]
        orig = result["original_patient"]
        
        # Constantes vitales compactes
        st.subheader("🩺 Constantes Vitales")
        
        if orig.constantes:
            c = orig.constantes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                temp = c.temperature
                #temp_status = "🟢" if 36.1 <= temp <= 37.8 else "🟡" if temp <= 38.5 else "🔴"
                st.metric("Temp", f"{temp}°C")
                
                fc = c.fc
                #fc_status = "🟢" if 60 <= fc <= 100 else "🟡" if (50 <= fc < 60 or 100 < fc <= 120) else "🔴"
                st.metric("FC", f"{fc} bpm")
            
            with col2:
                spo2 = c.spo2
                #spo2_status = "🟢" if spo2 >= 95 else "🟡" if 90 <= spo2 < 95 else "🔴"
                st.metric("SpO2", f"{spo2}%")
                
                fr = c.fr
                #fr_status = "🟢" if 12 <= fr <= 20 else "🟡" if (10 <= fr < 12 or 20 < fr <= 25) else "🔴"
                st.metric("FR", f"{fr}/min")
            
            with col3:
                ta_sys = c.ta_systolique
                ta_dia = c.ta_diastolique
                #ta_status = "🟢" if 90 <= ta_sys <= 140 else "🟡" if (80 <= ta_sys < 90 or 140 < ta_sys <= 160) else "🔴" 
                st.metric("TA", f"{ta_sys}/{ta_dia}")
        
        st.divider()
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["💬 Conversation", "👤 Patient", "💾 ML Data"])
        
        with tab1:
            conversation = result["conversation"]
            
            for msg in conversation.messages:
                if msg.role.value == "user":
                    with st.chat_message("assistant"):
                        st.write(f"**Infirmier:** {msg.content}")
                else:
                    with st.chat_message("user"):
                        st.write(f"**Patient:** {msg.content}")
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Identité**")
                st.write(f"• {orig.prenom} {orig.nom}")
                st.write(f"• {orig.age} ans")
                st.write(f"• {'Homme' if orig.sexe == 'M' else 'Femme'}")
            
            with col2:
                st.write("**Médical**")
                
                if orig.symptomes_exprimes:
                    st.write("**Symptômes:**")
                    for s in orig.symptomes_exprimes[:5]:
                        st.write(f"• {s}")
                
                if orig.antecedents:
                    st.write("**Antécédents:**")
                    for a in orig.antecedents[:3]:
                        st.write(f"• {a}")
        
        with tab3:
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
                "📥 Télécharger JSON",
                json_str,
                "conversation.json",
                "application/json",
                use_container_width=True,
                type="primary"
            )
    
    # ========== COLONNE DROITE : Prédiction ML (TOUJOURS VISIBLE) ==========
    with col_right:
        st.subheader("🤖 Prédiction ML")
        
        # Bouton prédire
        if not st.session_state.current_prediction:
            predict_button = st.button("🔮 Prédire", type="primary", use_container_width=True)
        else:
            predict_button = False
        
        if predict_button:
            import pickle
            import numpy as np
            import time
            
            model_path = root_path / "src" / "models" / "random_forest_simple.pkl"
            
            if not model_path.exists():
                st.error("❌ Modèle ML non trouvé")
            else:
                with st.spinner("Analyse..."):
                    start_time = time.time()
                    
                    with open(model_path, "rb") as f:
                        clf = pickle.load(f)
                    
                    llm = LLMFactory.create("mistral", "mistral-large-latest")
                    workflow = SimulationWorkflow(llm)
                    workflow.original_patient = result["original_patient"]
                    workflow.extracted_patient = result["extracted_patient"]
                    workflow.pathology = result["pathology"]
                    workflow.conversation = result["conversation"]
                    
                    ml_data = workflow.export_for_ml()
                    
                    fc = ml_data.get("fc", 80)
                    fr = ml_data.get("fr", 16)
                    spo2 = ml_data.get("spo2", 98)
                    ta_sys = ml_data.get("ta_systolique", 120)
                    ta_dia = ml_data.get("ta_diastolique", 80)
                    temp = ml_data.get("temperature", 37.0)
                    age = ml_data.get("age", 50)
                    sexe = ml_data.get("sexe", "M")
                    
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
                    
                    prediction = clf.predict(features)[0]
                    probas = clf.predict_proba(features)[0]
                    proba_dict = dict(zip(clf.classes_, probas))
                    
                    duration = time.time() - start_time
                    
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
                    
                    st.success(f"✅ {duration*1000:.0f}ms")
                    st.balloons()
                    st.rerun()
        
        # Affichage prédiction
        if st.session_state.current_prediction:
            pred = st.session_state.current_prediction
            
            colors_emoji = {
                "ROUGE": "🔴",
                "JAUNE": "🟡",
                "VERT": "🟢",
                "GRIS": "⚪"
            }
            
            descriptions = {
                "ROUGE": "Urgence vitale",
                "JAUNE": "Urgent",
                "VERT": "Non urgent",
                "GRIS": "Consultation"
            }
            
            severity = pred['severity']
            severity_emoji = colors_emoji[severity]
            
            st.success(f"{severity_emoji} **{severity}**\n\n{descriptions[severity]}")
            st.metric("Confiance", f"{pred['confidence']*100:.1f}%")
            
            st.divider()
            
            # Probabilités
            st.write("**Probabilités**")
            
            for sev in ["ROUGE", "JAUNE", "VERT", "GRIS"]:
                prob = pred['probabilities'].get(sev, 0)
                st.progress(prob, text=f"{sev}: {prob*100:.0f}%")
            
            # Détails
            with st.expander("📋 Détails"):
                feat = pred['features']
                st.write(f"• FC: {feat['fc']} bpm")
                st.write(f"• FR: {feat['fr']}/min")
                st.write(f"• SpO2: {feat['spo2']}%")
                st.write(f"• TA: {feat['ta_sys']}/{feat['ta_dia']}")
                st.write(f"• Temp: {feat['temp']}°C")
                st.write(f"• Âge: {feat['age']} ans")
                st.caption(f"Temps: {pred['duration']*1000:.0f}ms")

st.divider()

# Dataset complet
st.header("📊 Dataset Complet")

if st.session_state.conversations:
    st.success(f"📚 **{len(st.session_state.conversations)} conversations**")
    
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
    st.info("Aucune conversation générée. Cliquez sur **'Générer'** pour commencer!")

# Footer
st.divider()
st.caption("🎲 Génération IA + 🤖 Prédiction ML • Mistral AI • Random Forest")