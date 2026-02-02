import re
import time
import os
from typing import Dict, Optional, Tuple, List
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()


class TriageChatbotAPI:
    """Chatbot ultra robuste pour TOUS les utilisateurs."""

    def __init__(self, api_key: str = None, retriever=None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.retriever = retriever
        
        if self.api_key:
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
            "vitals": {},
            "messages": [],
        }
        self.attempts = {}  # Compte tentatives par étape
        self.current_step = "identity"

    def start(self) -> str:
        """Message de bienvenue."""
        return """Bonjour ! Je suis l'assistant de triage. 👋

Je vais vous poser quelques questions simples.

**Pour commencer, dites-moi :**
• Votre prénom
• Votre âge  
• Si vous êtes un homme ou une femme

**Exemple :** Marie, 35 ans, femme"""

    def chat(self, user_message: str) -> str:
        """
        Traite le message utilisateur.
        
        ULTRA ROBUSTE :
        - Gère les réponses partielles
        - Aide si l'utilisateur ne sait pas
        - Accepte toutes les formes
        - Patient et pédagogique
        """
        start_time = time.time()
        
        # Ajouter message user
        self.data["messages"].append({"role": "user", "content": user_message})
        
        # ========== EXTRACTION AGRESSIVE ==========
        self._extract_everything(user_message)
        
        # ========== PROCHAINE ÉTAPE ==========
        next_step = self._smart_next_step()
        
        # ========== GÉNÉRATION RÉPONSE ==========
        if next_step == "done":
            response = """✅ **Parfait ! J'ai toutes les informations.**

Vous pouvez maintenant cliquer sur le bouton **"🎯 Prédire la gravité"** dans le panneau latéral."""
        else:
            response = self._smart_question(next_step, user_message)
        
        # Ajouter message bot
        self.data["messages"].append({"role": "assistant", "content": response})
        
        # Track
        self._track_latency(time.time() - start_time)
        
        # Update step
        self.current_step = next_step
        
        return response

    def _extract_everything(self, msg: str):
        """
        Extraction ULTRA AGRESSIVE.
        
        Cherche PARTOUT dans le message.
        """
        msg_clean = msg.strip()
        msg_lower = msg_clean.lower()
        
        # ========== IDENTITÉ ==========
        
        # Prénom (cherche un mot avec majuscule ou premier mot)
        if not self.data["name"]:
            # Essaie d'extraire prénom de plusieurs façons
            prenom = self._extract_prenom(msg_clean)
            if prenom:
                self.data["name"] = prenom
                print(f"✅ Prénom : {prenom}")
        
        # Âge
        if not self.data["age"]:
            age = self._extract_age(msg_lower)
            if age:
                self.data["age"] = age
                print(f"✅ Âge : {age}")
        
        # Sexe
        if not self.data["sex"]:
            sexe = self._extract_sexe(msg_lower)
            if sexe:
                self.data["sex"] = sexe
                print(f"✅ Sexe : {sexe}")
        
        # ========== SYMPTÔMES ==========
        if not self.data["symptoms"]:
            symptoms = self._extract_symptoms(msg_lower)
            if symptoms:
                self.data["symptoms"] = symptoms
                print(f"✅ Symptômes : {symptoms}")
        
        # ========== CONSTANTES ==========
        
        # Température
        if "Temperature" not in self.data["vitals"]:
            temp = self._extract_temperature(msg_lower)
            if temp:
                self.data["vitals"]["Temperature"] = temp
                print(f"✅ Température : {temp}°C")
        
        # FC
        if "FC" not in self.data["vitals"]:
            fc = self._extract_fc(msg_lower)
            if fc:
                self.data["vitals"]["FC"] = fc
                print(f"✅ FC : {fc} bpm")
        
        # TA
        if "TA_systolique" not in self.data["vitals"]:
            ta = self._extract_ta(msg_lower)
            if ta:
                self.data["vitals"]["TA_systolique"] = ta[0]
                self.data["vitals"]["TA_diastolique"] = ta[1]
                print(f"✅ TA : {ta[0]}/{ta[1]}")
        
        # SpO2
        if "SpO2" not in self.data["vitals"]:
            spo2 = self._extract_spo2(msg_lower)
            if spo2:
                self.data["vitals"]["SpO2"] = spo2
                print(f"✅ SpO2 : {spo2}%")
        
        # FR
        if "FR" not in self.data["vitals"]:
            fr = self._extract_fr(msg_lower)
            if fr:
                self.data["vitals"]["FR"] = fr
                print(f"✅ FR : {fr}/min")

    # ========== EXTRACTEURS INTELLIGENTS ==========
    
    def _extract_prenom(self, msg: str) -> Optional[str]:
        """
        Extrait prénom intelligemment.
        
        Cherche :
        1. Mot avec majuscule au début
        2. Premier mot si pas de majuscule
        3. Entre virgules
        """
        # Enlever ponctuation de fin
        msg = msg.strip('.,;!?')
        
        # Cherche mot avec majuscule
        match = re.search(r'\b([A-ZÀ-Ÿ][a-zà-ÿ]{1,15})\b', msg)
        if match:
            return match.group(1)
        
        # Sinon premier mot (capitalize)
        words = msg.split()
        if words:
            first_word = words[0].strip(',;.')
            if len(first_word) >= 2 and first_word.isalpha():
                return first_word.capitalize()
        
        return None

    def _extract_age(self, msg: str) -> Optional[int]:
        """Extrait âge."""
        # Cherche nombre + "ans" ou juste nombre entre 0 et 120
        match = re.search(r'(\d{1,3})\s*ans?', msg)
        if match:
            age = int(match.group(1))
            if 0 <= age <= 120:
                return age
        
        # Cherche juste un nombre
        numbers = re.findall(r'\b(\d{1,3})\b', msg)
        for num_str in numbers:
            num = int(num_str)
            if 0 < num <= 120:
                return num
        
        return None

    def _extract_sexe(self, msg: str) -> Optional[str]:
        """Extrait sexe."""
        # Homme
        if any(w in msg for w in ['homme', 'masculin', 'h', 'male', 'garçon', 'monsieur', 'mâle', 'gars']):
            return "H"
        
        # Femme
        if any(w in msg for w in ['femme', 'féminin', 'f', 'female', 'fille', 'madame', 'femelle', 'meuf']):
            return "F"
        
        return None

    def _extract_symptoms(self, msg: str) -> Optional[List[str]]:
        """
        Extrait symptômes de manière TRÈS LARGE.
        
        Accepte plein de variantes.
        """
        symptoms = []
        
        symptoms_map = {
            # Douleurs
            'mal': 'Douleur',
            'douleur': 'Douleur',
            'souffr': 'Douleur',
            'ça fait mal': 'Douleur',
            
            # Localisations spécifiques
            'dent': 'Douleur dentaire',
            'tête': 'Céphalées',
            'crâne': 'Céphalées',
            'migraine': 'Céphalées',
            'ventre': 'Douleur abdominale',
            'abdomen': 'Douleur abdominale',
            'estomac': 'Douleur abdominale',
            'poitrine': 'Douleur thoracique',
            'thorax': 'Douleur thoracique',
            'cœur': 'Douleur thoracique',
            'dos': 'Douleur dorsale',
            'jambe': 'Douleur membre',
            'bras': 'Douleur membre',
            
            # Autres symptômes
            'fièvre': 'Fièvre',
            'chaud': 'Fièvre',
            'température': 'Fièvre',
            'toux': 'Toux',
            'nausée': 'Nausées',
            'vomi': 'Vomissements',
            'diarrhée': 'Diarrhée',
            'fatigue': 'Fatigue',
            'faible': 'Fatigue',
            'vertige': 'Vertiges',
            'tourner': 'Vertiges',
            'essouffl': 'Dyspnée',
            'respir': 'Dyspnée',
            'souffle': 'Dyspnée',
        }
        
        for keyword, symptom in symptoms_map.items():
            if keyword in msg:
                if symptom not in symptoms:
                    symptoms.append(symptom)
        
        return symptoms if symptoms else None

    def _extract_temperature(self, msg: str) -> Optional[float]:
        """Extrait température (35-42°C)."""
        # Cherche nombres avec virgule ou point
        numbers = re.findall(r'\d+[,\.]?\d*', msg)
        for num_str in numbers:
            try:
                num = float(num_str.replace(',', '.'))
                if 35.0 <= num <= 42.0:
                    return round(num, 1)
            except:
                pass
        return None

    def _extract_fc(self, msg: str) -> Optional[int]:
        """Extrait FC (30-250 bpm)."""
        numbers = re.findall(r'\d+', msg)
        for num_str in numbers:
            num = int(num_str)
            if 30 <= num <= 250:
                return num
        return None

    def _extract_ta(self, msg: str) -> Optional[Tuple[int, int]]:
        """Extrait TA."""
        # Format X/Y
        match = re.search(r'(\d{2,3})\s*/\s*(\d{2,3})', msg)
        if match:
            sys = int(match.group(1))
            dia = int(match.group(2))
            
            # Format court
            if sys < 50:
                sys *= 10
            if dia < 30:
                dia *= 10
            
            if 50 <= sys <= 250 and 30 <= dia <= 150:
                return (sys, dia)
        
        # Juste un nombre
        numbers = re.findall(r'\d+', msg)
        for num_str in numbers:
            sys = int(num_str)
            if 50 <= sys <= 250:
                dia = int(sys * 0.67)
                return (sys, dia)
        
        return None

    def _extract_spo2(self, msg: str) -> Optional[int]:
        """Extrait SpO2 (50-100%)."""
        numbers = re.findall(r'\d+', msg)
        for num_str in numbers:
            num = int(num_str)
            if 50 <= num <= 100:
                return num
        return None

    def _extract_fr(self, msg: str) -> Optional[int]:
        """Extrait FR (5-60/min)."""
        numbers = re.findall(r'\d+', msg)
        for num_str in numbers:
            num = int(num_str)
            if 5 <= num <= 60:
                return num
        return None

    def _smart_next_step(self) -> str:
        """
        Détermine prochaine étape INTELLIGEMMENT.
        
        Vérifie ce qui manque vraiment.
        """
        # Identité complète ?
        if not self.data.get("name") or not self.data.get("age") or not self.data.get("sex"):
            return "identity"
        
        # Symptômes ?
        if not self.data.get("symptoms"):
            return "symptoms"
        
        # Constantes (dans l'ordre)
        v = self.data["vitals"]
        
        if "Temperature" not in v:
            return "temperature"
        if "FC" not in v:
            return "fc"
        if "TA_systolique" not in v:
            return "ta"
        if "SpO2" not in v:
            return "spo2"
        if "FR" not in v:
            return "fr"
        
        return "done"

    def _smart_question(self, step: str, last_msg: str) -> str:
        """
        Génère question INTELLIGENTE.
        
        ADAPTE selon :
        - Si user a dit "je ne sais pas"
        - Nombre de tentatives
        - Contexte
        """
        # Incrémenter tentatives
        if step not in self.attempts:
            self.attempts[step] = 0
        self.attempts[step] += 1
        
        attempts = self.attempts[step]
        
        # User dit "je ne sais pas" ?
        confused = any(w in last_msg.lower() for w in ['sais pas', 'sait pas', 'connais pas', 'aucune idée'])
        
        name = self.data.get("name", "")
        
        # ========== IDENTITÉ ==========
        if step == "identity":
            # Quelles infos manquent ?
            missing = []
            if not self.data.get("name"):
                missing.append("prénom")
            if not self.data.get("age"):
                missing.append("âge")
            if not self.data.get("sex"):
                missing.append("sexe")
            
            if attempts == 1:
                return f"""**Pour commencer, j'ai besoin de 3 informations simples :**

• Votre **prénom**
• Votre **âge**
• Si vous êtes un **homme** ou une **femme**

**Exemple :** Jean, 30 ans, homme"""
            else:
                missing_str = " et ".join(missing)
                return f"""Il me manque encore : **{missing_str}**

Pouvez-vous me donner cette information ?"""
        
        # ========== SYMPTÔMES ==========
        elif step == "symptoms":
            if attempts == 1:
                return f"""Bonjour **{name}** ! 👋

**Qu'est-ce qui vous amène aujourd'hui ?**

Dites-moi votre symptôme principal (ce qui vous gêne le plus)."""
            else:
                return f"""**{name}**, j'ai besoin de savoir ce qui ne va pas.

**Exemples :** 
• "J'ai mal au ventre"
• "J'ai de la fièvre"
• "Je tousse"

Qu'est-ce qui vous gêne ?"""
        
        # ========== TEMPÉRATURE ==========
        elif step == "temperature":
            if confused and attempts > 1:
                return f"""**Pas de problème {name} !**

On va mesurer votre température ensemble.

**Si vous avez un thermomètre :**
• Mettez-le sous la langue ou sous le bras
• Attendez le bip
• Dites-moi le chiffre

**Si vous n'en avez pas :**
• Tapez juste **"37"** (température normale)"""
            elif attempts == 1:
                return f"""**{name}**, quelle est votre **température** ?

**Exemples acceptés :**
• 37.5
• 38
• 39°C

*(Si vous ne savez pas, dites-le moi)*"""
            else:
                return f"""**{name}**, j'ai vraiment besoin de la température.

Tapez un chiffre entre **35 et 42**.

**Si vous ne savez pas**, tapez juste **37** (température normale)."""
        
        # ========== FC ==========
        elif step == "fc":
            if confused and attempts > 1:
                return f"""**Pas grave {name} !**

**Pour mesurer votre pouls :**
1. Posez 2 doigts sur votre poignet
2. Comptez les battements pendant 15 secondes
3. Multipliez par 4

**Ou tapez 80** (valeur moyenne normale)"""
            elif attempts == 1:
                return f"""**{name}**, quelle est votre **fréquence cardiaque** (pouls) ?

**Exemples :**
• 80
• 90 bpm

*(Si vous ne savez pas, dites-le)*"""
            else:
                return f"""**{name}**, j'ai besoin du pouls.

Tapez un chiffre entre **50 et 150**.

**Si vous ne savez pas**, tapez **80** (valeur normale)."""
        
        # ========== TA ==========
        elif step == "ta":
            if confused and attempts > 1:
                return f"""**Ce n'est pas grave {name} !**

Si vous n'avez pas de tensiomètre, tapez :

**120/80** (tension normale)"""
            elif attempts == 1:
                return f"""**{name}**, quelle est votre **tension artérielle** ?

**Format :** 2 chiffres séparés par un /

**Exemples :**
• 120/80
• 13/8
• 14/9

*(Si vous ne savez pas, dites-le)*"""
            else:
                return f"""**{name}**, j'ai besoin de la tension.

**Format :** X/Y (exemple: 120/80)

**Si vous ne savez pas**, tapez **120/80** (normale)."""
        
        # ========== SPO2 ==========
        elif step == "spo2":
            if confused and attempts > 1:
                return f"""**Pas de souci {name} !**

Si vous n'avez pas d'oxymètre, tapez :

**98** (saturation normale)"""
            elif attempts == 1:
                return f"""**{name}**, quelle est votre **saturation en oxygène** (SpO2) ?

**Exemples :**
• 98
• 95%

*(Si vous ne savez pas, dites-le)*"""
            else:
                return f"""**{name}**, j'ai besoin du SpO2.

Tapez un chiffre entre **90 et 100**.

**Si vous ne savez pas**, tapez **98** (normale)."""
        
        # ========== FR ==========
        elif step == "fr":
            if confused and attempts > 1:
                return f"""**Ce n'est pas grave {name} !**

**Pour compter :**
• Respirez normalement
• Comptez combien de fois vous respirez en 1 minute

**Ou tapez 16** (respiration normale)"""
            elif attempts == 1:
                return f"""**{name}**, quelle est votre **fréquence respiratoire** ?

**Combien de fois respirez-vous par minute ?**

**Exemples :**
• 16
• 18/min

*(Si vous ne savez pas, dites-le)*"""
            else:
                return f"""**{name}**, dernière info !

Tapez un chiffre entre **12 et 25**.

**Si vous ne savez pas**, tapez **16** (normale)."""
        
        return "Une question ?"

    def _track_latency(self, duration: float):
        """Track latence."""
        try:
            from ..monitoring.metrics_tracker import get_tracker
            tracker = get_tracker()
            tracker.track_latency("Chatbot", "message", duration)
        except:
            pass

    def is_ready_for_prediction(self) -> bool:
        """Vérifie si prêt."""
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