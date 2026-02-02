from typing import Any
import json
import re
from .base_agent import BaseAgent
from ..llm.base_llm import BaseLLMProvider
from ..models.patient import Patient, Constantes


class PatientGenerator(BaseAgent):
    """Générateur de patient réaliste."""

    def __init__(self, llm_provider: BaseLLMProvider):
        system_prompt = "Expert médical. Génère des profils patients réalistes. JSON uniquement."
        super().__init__(
            llm_provider=llm_provider, system_prompt=system_prompt, name="PatientGenerator"
        )

    def run(self, input_data: str) -> dict:
        patient = self.generate_from_description(input_data)
        return {"patient": patient}
    
    def _clean_list(self, value: Any, default: list = None) -> list:
        """
        Nettoie une valeur pour s'assurer qu'elle est une liste valide.
        Gère les cas où l'IA renvoie un dict, une string, ou autre chose.
        """
        if default is None:
            default = []
        
        if value is None:
            return default
        
        # Si c'est déjà une liste
        if isinstance(value, list):
            return value
        
        # Si c'est un dict, extraire les valeurs
        if isinstance(value, dict):
            return list(value.values())
        
        # Si c'est une string, la mettre dans une liste
        if isinstance(value, str):
            return [value] if value.strip() else default
        
        return default
    
    def _clean_number(self, value: Any, default: float, is_float: bool = False) -> float:
        """
        Nettoie une valeur pour extraire un nombre valide.
        Gère les cas comme '>20', '<95', '95-98', etc.
        """
        if value is None:
            return default
        
        # Si c'est déjà un nombre valide
        if isinstance(value, (int, float)):
            return float(value) if is_float else int(value)
        
        # Si c'est une string, extraire le nombre
        if isinstance(value, str):
            # Enlever les espaces
            value = value.strip()
            
            # Extraire tous les nombres (avec décimales si nécessaire)
            if is_float:
                numbers = re.findall(r'\d+\.?\d*', value)
            else:
                numbers = re.findall(r'\d+', value)
            
            if numbers:
                try:
                    return float(numbers[0]) if is_float else int(numbers[0])
                except (ValueError, IndexError):
                    return default
        
        return default

    def generate_from_description(self, description: str) -> Patient:
        prompt = f"""Génère un patient COMPLET et RÉALISTE pour cette pathologie.

PATHOLOGIE : {description}

RÉPONDS UNIQUEMENT EN JSON (pas de texte avant/après) :

{{
  "prenom": "prénom français",
  "nom": "nom français",
  "age": nombre entier,
  "sexe": "M" ou "F",
  "symptomes_exprimes": ["symptôme en langage patient", ...],
  "duree_symptomes": "depuis quand",
  "antecedents": ["antécédent1", ...],
  "constantes": {{
    "fc": nombre entier (60-180),
    "fr": nombre entier (12-35),
    "spo2": nombre entier (85-100),
    "ta_systolique": nombre entier (80-200),
    "ta_diastolique": nombre entier (50-120),
    "temperature": nombre décimal (36.0-40.5)
  }}
}}  

RÈGLES CONSTANTES (IMPORTANT) :
- Infarctus → FC 100-130, SpO2 88-93, TA basse
- Pneumonie → FC 100-120, FR 25-32, SpO2 85-92, Temp 38.5-40.0
- Fracture → FC 85-95, tout normal
- Gastro → FC normal, Temp 37.5-38.5

CRITIQUE : Les constantes doivent être des NOMBRES EXACTS (pas de >, <, ou ranges).
Exemples VALIDES : "fc": 95, "spo2": 92, "temperature": 38.2
Exemples INVALIDES : "fc": ">90", "spo2": "<95", "temperature": "38-39"

JSON uniquement :"""

        response = self.llm.generate(
            messages=[{"role": "user", "content": prompt}], temperature=0.7, max_tokens=600
        )

        data = self._extract_json_from_response(response)

        # Sexe
        sexe_raw = str(data.get("sexe", "M")).upper()[0]
        sexe = "M" if sexe_raw == "M" else "F"

        
        c = data.get("constantes", {})
        
       
        fc = self._clean_number(c.get("fc"), 80, is_float=False)
        fr = self._clean_number(c.get("fr"), 16, is_float=False)
        spo2 = self._clean_number(c.get("spo2"), 97, is_float=False)
        ta_systolique = self._clean_number(c.get("ta_systolique"), 120, is_float=False)
        ta_diastolique = self._clean_number(c.get("ta_diastolique"), 80, is_float=False)
        temperature = self._clean_number(c.get("temperature"), 37.0, is_float=True)
        
        # Validation des ranges
        fc = max(40, min(200, fc))  # Range 40-200
        fr = max(8, min(40, fr))  # Range 8-40
        spo2 = max(70, min(100, spo2))  # Range 70-100
        ta_systolique = max(60, min(220, ta_systolique))  # Range 60-220
        ta_diastolique = max(40, min(130, ta_diastolique))  # Range 40-130
        temperature = max(35.0, min(42.0, temperature))  # Range 35-42
        
        constantes = Constantes(
            fc=int(fc),
            fr=int(fr),
            spo2=int(spo2),
            ta_systolique=int(ta_systolique),
            ta_diastolique=int(ta_diastolique),
            temperature=float(round(temperature, 1)),
        )

        # Nettoyer l'âge aussi
        age = self._clean_number(data.get("age"), 50, is_float=False)
        age = max(0, min(120, int(age)))  # Range 0-120
        
        # Nettoyer duree_symptomes 
        duree_raw = data.get("duree_symptomes", "depuis quelques heures")
        if isinstance(duree_raw, dict):
            # Si c'est un dict, prendre la première valeur ou concaténer
            duree_symptomes = list(duree_raw.values())[0] if duree_raw else "depuis quelques heures"
        else:
            duree_symptomes = str(duree_raw) if duree_raw else "depuis quelques heures"
        
        # Nettoyer les listes 
        symptomes_exprimes = self._clean_list(data.get("symptomes_exprimes"), [])
        antecedents = self._clean_list(data.get("antecedents"), [])

        patient = Patient(
            prenom=data.get("prenom", "Jean"),
            nom=data.get("nom", "Dupont"),
            age=age,
            sexe=sexe,
            symptomes_exprimes=symptomes_exprimes,
            constantes=constantes,
            antecedents=antecedents,
            duree_symptomes=duree_symptomes,
        )
        return patient