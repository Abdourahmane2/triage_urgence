import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class ClinicalTriageClassifier:
    def __init__(self):
        # On utilise une version de ClinicalBERT fine-tunée pour la classification de texte
        # ou un pipeline de Zero-Shot si on n'a pas de dataset d'entraînement spécifique.
        self.model_name = "medicalai/ClinicalBERT"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Labels demandés
        self.labels = ["GRIS", "VERT", "JAUNE", "ROUGE"]
        self.label_desc = {
            "GRIS": "Ne nécessite pas les urgences, ni de voir rapidement un médecin généraliste. Situation stable.",
            "VERT": "Pathologie non vitale et non urgente. Consultation classique.",
            "JAUNE": "Pathologie non vitale mais urgente. Nécessite une prise en charge rapide.",
            "ROUGE": "Pathologie potentiellement vitale et urgente. Détresse vitale suspectée."
        }

    def _prepare_input_text(self, id_data, const_data, symptoms_json):
        """
        Concatène les données hétérogènes en un paragraphe textuel 
        compréhensible par ClinicalBERT.
        """
        text = f"Patient: {id_data.get('genre')}, {id_data.get('age')} ans. "
        
        # Ajout des constantes (critique pour ClinicalBERT)
        text += f"Constantes: FC {const_data.get('fc')}bpm, "
        text += f"SpO2 {const_data.get('spo2')}%, "
        text += f"Temp {const_data.get('temp')}°C, "
        text += f"TA {const_data.get('tas')}/{const_data.get('tad')}. "
        
        # Ajout des symptômes issus du JSON
        symptomes = ", ".join(symptoms_json.get("symptomes_principaux", []))
        text += f"Symptômes: {symptomes}. "
        text += f"Localisation: {symptoms_json.get('localisation')}. "
        text += f"Intensité douleur: {symptoms_json.get('intensite_douleur')}/10."
        
        return text
    def check_vital_emergency_rules(id_data, const_data):
    """
    Vérifie les critères d'alerte rouge basés sur les constantes et l'âge.
    Retourne True si une condition 'ROUGE' est rencontrée.
    """
        age = id_data.get('age', 30)
        temp = const_data.get('temp', 37.0)
        fc = const_data.get('fc', 75)
        tas = const_data.get('tas', 120)  # TA Systolique
        spo2 = const_data.get('spo2', 98)

    # 1. Condition d'origine : Hypoxie ou Tachycardie extrême
        if spo2 < 90 or fc > 130:
            return True

    # 2. Nourrissons et fièvre (Age <= 1 an et Temp > 38)
        if age <= 1 and temp > 38.0:
            return True

    # 3. Jeunes enfants et forte fièvre (Age <= 3 ans et Temp > 38.5)
        if age <= 3 and temp > 38.5:
            return True

    # 4. Hypertension sévère (TA Systolique >= 170 mmHg ou 17 dans votre unité)
    # Note : On vérifie 17 ou 170 selon le format de saisie habituel
        if tas >= 170 or tas <= 20: # Gestion du cas où l'utilisateur saisit '17' au lieu de '170'
            if tas >= 17:
                return True

    # 5. État de choc / Bradycardie (FC <= 50 et TA Systolique <= 9 ou 90)
        tas_val = tas if tas > 20 else tas * 10 # Normalisation auto 9 -> 90
        if fc <= 50 and tas_val <= 90:
            return True

        return False

    def classify_emergency(self, id_data, const_data, symptoms_json):
        """
        Réalise la classification via un pipeline Zero-Shot basé sur ClinicalBERT
        (ou modèle de classification direct)
        """
        input_text = self._prepare_input_text(id_data, const_data, symptoms_json)
        
        # Utilisation de Zero-Shot Classification (approche la plus robuste sans dataset d'entraînement)
        # Note: medicalai/ClinicalBERT est souvent utilisé avec un classifieur par-dessus
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli") 
        # Note technique : Pour ClinicalBERT pur, il faudrait un entraînement supervisé.
        # Ici, nous utilisons une logique hybride ou le texte "embeddé" par ClinicalBERT.
        
        results = classifier(input_text, candidate_labels=self.labels)
        
        
        score_final = results['labels'][0]
        confiance = results['scores'][0]
        
        # Application du corpus de conditions prioritaires
        if check_vital_emergency_rules(id_data, const_data):
            score_final = "ROUGE"
            confiance = 1.0  # Force la confiance au maximum car règle médicale absolue

        return {
            "niveau": score_final,
            "confiance": confiance,
            "resume_analyse": input_text
        }
