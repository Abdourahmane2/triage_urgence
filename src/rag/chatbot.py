"""
Chatbot LLM Professionnel pour Triage Médical
"""

import json
import time
import os
from typing import Dict, Optional, List
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()


class TriageChatbotLLM:
    """Chatbot professionnel piloté par LLM."""

    def __init__(self, api_key: str = None, retriever=None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.retriever = retriever
        
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY manquante")
        
        self.client = Mistral(api_key=self.api_key)
        print("✅ Mistral API activée")
        
        self.reset()

    def reset(self):
        """Réinitialise le chatbot."""
        self.data = {
            "name": None,
            "age": None,
            "sex": None,
            "symptoms": [],
            "symptom_duration": None,
            "antecedents": [],
            "allergies": [],
            "vitals": {},
            "messages": [],
        }
        self.conversation_history = []
        self.collected_identity = False
        self.collected_symptoms = False
        self.collected_antecedents = False

    def start(self) -> str:
        """Message de bienvenue professionnel."""
        return """**Assistant de Triage Médical**

Bonjour, je vais collecter les informations du patient.

**Pour commencer, donnez-moi :**
• Prénom et nom
• Âge
• Sexe (H/F)

Ex: Marie Dubois, 45 ans, femme"""

    def chat(self, user_message: str) -> str:
        """
        Traite le message de l'infirmier.
        
        Flow:
        1. Identité (prénom, âge, sexe)
        2. Symptômes (principal + autres)
        3. Antécédents médicaux
        4. Constantes vitales (5)
        """
        start_time = time.time()
        
        # Ajouter à l'historique
        self.conversation_history.append({"role": "user", "content": user_message})
        self.data["messages"].append({"role": "user", "content": user_message})
        
        # Extraire les données avec LLM + TRACKING
        self._extract_with_llm(user_message)
        
        # Déterminer prochaine étape
        next_step = self._get_next_step()
        
        # Générer question suivante avec LLM + TRACKING
        if next_step == "done":
            response = "✅ **Collecte terminée**\n\nVous pouvez maintenant cliquer sur **'Prédire'** pour l'analyse ML."
        else:
            response = self._generate_next_question_llm(next_step, user_message)
        
        # Ajouter à l'historique
        self.conversation_history.append({"role": "assistant", "content": response})
        self.data["messages"].append({"role": "assistant", "content": response})
        
        # Track latence totale
        self._track_latency(time.time() - start_time)
        
        return response

    def _extract_with_llm(self, user_message: str):
        """
        Extrait les données du message avec le LLM + TRACKING API.
        """
        # Construire le contexte de conversation
        conversation_text = "\n".join([
            f"{'Infirmier' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in self.conversation_history[-6:]
        ])
        
        prompt = f"""Tu es un système d'extraction pour triage médical.

CONVERSATION:
{conversation_text}

EXTRAIT LES INFORMATIONS (mets null si NON mentionné):

**IDENTITÉ:**
- Prénom: texte ou null
- Nom: texte ou null
- Âge: nombre (0-120) ou null
- Sexe: "H" ou "F" ou null

**SYMPTÔMES:**
- Symptômes: liste des symptômes (utilise le langage du patient)
- Durée: "depuis X heures/jours" ou null
- Localisation: où se situe la douleur ou null

**ANTÉCÉDENTS:**
- Antécédents médicaux: liste (diabète, hypertension, etc.)
- Allergies: liste ou []
- Traitements en cours: liste ou []

**CONSTANTES VITALES** (UNIQUEMENT si CLAIREMENT mentionnées avec contexte):
- Température: nombre (35-42) ou null - SI "température", "temp", "fièvre" mentionné
- FC: nombre (30-250) ou null - SI "fréquence cardiaque", "pouls", "FC", "battements" mentionné
- TA_systolique: nombre (50-250) ou null - SI format X/Y ou "tension" mentionné
- TA_diastolique: nombre (30-150) ou null
- SpO2: nombre (50-100) ou null - SI "SpO2", "saturation", "oxygène" mentionné
- FR: nombre (5-60) ou null - SI "fréquence respiratoire", "respiration", "FR" mentionné

**RÈGLES STRICTES:**
- Extrais UNIQUEMENT ce qui est dit explicitement
- Pour constantes: DOIT avoir contexte médical clair
- Ne confonds PAS âge avec température/FC
- Si "35 ans" → âge=35, température=null
- Si "température 35" → température=35

RÉPONDS EN JSON SEULEMENT:

{{
  "identity": {{
    "prenom": null,
    "nom": null,
    "age": null,
    "sex": null
  }},
  "symptoms": {{
    "list": [],
    "duration": null,
    "location": null
  }},
  "antecedents": {{
    "medical": [],
    "allergies": [],
    "treatments": []
  }},
  "vitals": {{
    "Temperature": null,
    "FC": null,
    "TA_systolique": null,
    "TA_diastolique": null,
    "SpO2": null,
    "FR": null
  }}
}}"""

        try:
            # APPEL API AVEC TRACKING
            api_start = time.time()
            
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )
            
            api_duration = time.time() - api_start
            
            # TRACKING API
            self._track_api_call(
                model="mistral-large-latest",
                tokens_input=len(prompt.split()) * 1.3,  # Approximation
                tokens_output=len(response.choices[0].message.content.split()) * 1.3,
                duration=api_duration
            )
            
            llm_response = response.choices[0].message.content
            
            # Parser JSON
            data = self._parse_json(llm_response)
            
            # Mettre à jour IDENTITÉ
            identity = data.get("identity", {})
            if identity.get("prenom") and not self.data["name"]:
                nom_complet = identity.get("prenom", "")
                if identity.get("nom"):
                    nom_complet += " " + identity["nom"]
                self.data["name"] = nom_complet
                print(f"✅ Nom: {nom_complet}")
            
            if identity.get("age"):
                self.data["age"] = identity["age"]
                print(f"✅ Âge: {identity['age']}")
            
            if identity.get("sex"):
                self.data["sex"] = identity["sex"]
                print(f"✅ Sexe: {identity['sex']}")
            
            # Mettre à jour SYMPTÔMES
            symptoms_data = data.get("symptoms", {})
            if symptoms_data.get("list"):
                for s in symptoms_data["list"]:
                    if s and s not in self.data["symptoms"]:
                        self.data["symptoms"].append(s)
                        print(f"✅ Symptôme: {s}")
            
            if symptoms_data.get("duration"):
                self.data["symptom_duration"] = symptoms_data["duration"]
            
            # Mettre à jour ANTÉCÉDENTS
            antecedents_data = data.get("antecedents", {})
            if antecedents_data.get("medical"):
                for a in antecedents_data["medical"]:
                    if a and a not in self.data["antecedents"]:
                        self.data["antecedents"].append(a)
                        print(f"✅ Antécédent: {a}")
            
            if antecedents_data.get("allergies"):
                for a in antecedents_data["allergies"]:
                    if a and a not in self.data["allergies"]:
                        self.data["allergies"].append(a)
            
            # Mettre à jour CONSTANTES
            vitals = data.get("vitals", {})
            for key, value in vitals.items():
                if value is not None and key not in self.data["vitals"]:
                    self.data["vitals"][key] = value
                    print(f"✅ {key}: {value}")
            
            # Marquer étapes complétées
            if self.data["name"] and self.data["age"] and self.data["sex"]:
                self.collected_identity = True
            
            if len(self.data["symptoms"]) > 0:
                self.collected_symptoms = True
        
        except Exception as e:
            print(f"⚠️ Extraction LLM erreur: {e}")

    def _generate_next_question_llm(self, step: str, last_message: str) -> str:
        """
        Génère la prochaine question avec le LLM + TRACKING.
        """
        # Contexte actuel
        identity_status = f"Prénom: {self.data.get('name') or 'Non'}, Âge: {self.data.get('age') or 'Non'}, Sexe: {self.data.get('sex') or 'Non'}"
        symptoms_status = f"{len(self.data['symptoms'])} symptôme(s): {', '.join(self.data['symptoms']) if self.data['symptoms'] else 'Aucun'}"
        antecedents_status = f"{len(self.data['antecedents'])} antécédent(s)"
        
        vitals_collected = [k for k in ["Temperature", "FC", "TA_systolique", "SpO2", "FR"] if k in self.data["vitals"]]
        vitals_missing = [k for k in ["Temperature", "FC", "TA_systolique", "SpO2", "FR"] if k not in self.data["vitals"]]
        
        prompt = f"""Tu es assistant de triage médical professionnel.

**DONNÉES COLLECTÉES:**
- Identité: {identity_status}
- Symptômes: {symptoms_status}
- Antécédents: {antecedents_status}
- Constantes collectées: {', '.join(vitals_collected) if vitals_collected else 'Aucune'}
- Constantes manquantes: {', '.join(vitals_missing)}

**PROCHAINE ÉTAPE:** {step}

**DERNIÈRE RÉPONSE:** {last_message}

GÉNÈRE LA PROCHAINE QUESTION (professionnel mais concis):

**RÈGLES:**
1. Question claire et directe (2-3 lignes max)
2. Toujours donner des exemples de réponses
3. Ton professionnel mais pas robotique
4. Format: Question + "Ex: réponse1 / réponse2"

**SELON L'ÉTAPE:**

Si step=identity:
"Il me manque [info]. Pouvez-vous me donner [info] ?
Ex: [exemple]"

Si step=symptoms:
"Quel est le symptôme principal du patient ?
Ex: mal de tête / douleur thoracique / fièvre"

Si step=more_symptoms:
"D'autres symptômes associés ?
Ex: oui (préciser) / non / aucun autre"

Si step=symptom_duration:
"Depuis combien de temps ?
Ex: 2 heures / ce matin / depuis hier"

Si step=antecedents:
"Antécédents médicaux du patient ?
Ex: diabète / hypertension / aucun / ne sait pas"

Si step=temperature:
"Température corporelle ?
Ex: 37.5 / 38 / 39"

Si step=fc:
"Fréquence cardiaque (pouls) ?
Ex: 80 / 90 / 100"

Si step=ta:
"Tension artérielle ?
Ex: 120/80 / 140/90 / 110/70"

Si step=spo2:
"Saturation en oxygène (SpO2) ?
Ex: 98 / 95 / 92"

Si step=fr:
"Fréquence respiratoire ?
Ex: 16 / 20 / 25"

RÉPONDS JUSTE LA QUESTION (concise):"""

        try:
            # APPEL API AVEC TRACKING
            api_start = time.time()
            
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=150
            )
            
            api_duration = time.time() - api_start
            
            # TRACKING API
            self._track_api_call(
                model="mistral-large-latest",
                tokens_input=len(prompt.split()) * 1.3,
                tokens_output=len(response.choices[0].message.content.split()) * 1.3,
                duration=api_duration
            )
            
            question = response.choices[0].message.content.strip()
            
            # Nettoyer
            question = question.replace("**", "").strip()
            
            return question
        
        except Exception as e:
            print(f"⚠️ Génération question erreur: {e}")
            return self._fallback_question(step)

    def _get_next_step(self) -> str:
        """Détermine la prochaine étape logique."""
        
        # 1. IDENTITÉ COMPLÈTE ?
        if not self.data.get("name"):
            return "identity"
        if not self.data.get("age"):
            return "identity"
        if not self.data.get("sex"):
            return "identity"
        
        # 2. SYMPTÔMES ?
        if not self.data["symptoms"]:
            return "symptoms"
        
        # 3. DURÉE SYMPTÔMES ?
        if not self.data.get("symptom_duration") and not self.collected_symptoms:
            self.collected_symptoms = True  # Marquer comme collecté
            return "symptom_duration"
        
        # 4. AUTRES SYMPTÔMES ?
        if len(self.data["symptoms"]) == 1 and not self.collected_symptoms:
            self.collected_symptoms = True
            return "more_symptoms"
        
        # 5. ANTÉCÉDENTS ?
        if not self.collected_antecedents:
            self.collected_antecedents = True
            return "antecedents"
        
        # 6. CONSTANTES VITALES (dans l'ordre)
        if "Temperature" not in self.data["vitals"]:
            return "temperature"
        
        if "FC" not in self.data["vitals"]:
            return "fc"
        
        if "TA_systolique" not in self.data["vitals"]:
            return "ta"
        
        if "SpO2" not in self.data["vitals"]:
            return "spo2"
        
        if "FR" not in self.data["vitals"]:
            return "fr"
        
        return "done"

    def _fallback_question(self, step: str) -> str:
        """Questions de secours."""
        fallbacks = {
            "identity": "Pouvez-vous me donner le prénom, l'âge et le sexe du patient ?\nEx: Marie, 45 ans, femme",
            "symptoms": "Quel est le symptôme principal ?\nEx: mal de tête / douleur thoracique / fièvre",
            "more_symptoms": "D'autres symptômes ?\nEx: oui (préciser) / non",
            "symptom_duration": "Depuis combien de temps ?\nEx: 2 heures / ce matin / hier",
            "antecedents": "Antécédents médicaux ?\nEx: diabète / hypertension / aucun",
            "temperature": "Température ?\nEx: 37.5 / 38 / 39",
            "fc": "Fréquence cardiaque ?\nEx: 80 / 90 / 100",
            "ta": "Tension artérielle ?\nEx: 120/80 / 140/90",
            "spo2": "SpO2 ?\nEx: 98 / 95 / 92",
            "fr": "Fréquence respiratoire ?\nEx: 16 / 20 / 25"
        }
        
        return fallbacks.get(step, "Information suivante ?")

    def _parse_json(self, response: str) -> dict:
        """Parse JSON de la réponse LLM."""
        response = response.strip()
        
        # Enlever markdown
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        
        if response.endswith("```"):
            response = response[:-3]
        
        response = response.strip()
        
        return json.loads(response)

    def _track_api_call(self, model: str, tokens_input: float, tokens_output: float, duration: float):
        """Track appel API pour monitoring."""
        try:
            from src.monitoring.metrics_tracker import get_tracker
            
            tracker = get_tracker()
            tracker.track_api_call(
                service="mistral",
                model=model,
                tokens_input=int(tokens_input),
                tokens_output=int(tokens_output),
                latency=duration
            )
        except Exception as e:
            print(f"⚠️ Tracking API erreur: {e}")

    def _track_latency(self, duration: float):
        """Track latence."""
        try:
            from src.monitoring.metrics_tracker import get_tracker
            tracker = get_tracker()
            tracker.track_latency("ChatbotLLM", "message", duration)
        except:
            pass

    def is_ready_for_prediction(self) -> bool:
        """Vérifie si toutes les constantes sont collectées."""
        required = ["Temperature", "FC", "TA_systolique", "SpO2", "FR"]
        return all(k in self.data["vitals"] for k in required)

    def get_summary(self) -> Dict:
        """Résumé pour ML."""
        return {
            "patient_info": {
                "name": self.data.get("name"),
                "age": self.data.get("age"),
                "sex": self.data.get("sex"),
            },
            "symptoms": self.data.get("symptoms", []),
            "vitals": self.data["vitals"],
        }