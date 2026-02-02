#  Guide d'Utilisation - Système de Triage Médical IA

<div align="center">

![Guide](https://img.shields.io/badge/Guide-Utilisateur-blue?style=for-the-badge)
![Niveau](https://img.shields.io/badge/Niveau-Débutant_à_Avancé-green?style=for-the-badge)

**Guide complet pour utiliser le système de triage**

</div>

---

##  Table des Matières

1. [ Premier Démarrage](#-premier-démarrage)
2. [ Module Chat Interactif](#-module-chat-interactif)
3. [ Module Génération](#-module-génération)
4. [ Module Monitoring](#-module-monitoring)
5. [ FAQ](#-faq)
6. [ Résolution de Problèmes](#-résolution-de-problèmes)
7. [ Astuces & Bonnes Pratiques](#-astuces--bonnes-pratiques)

---

## Premier Démarrage

### Étape 1 : Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API
cp .env.example .env
# Éditez .env et ajoutez votre MISTRAL_API_KEY
```

### Étape 2 : Lancement

```bash
streamlit run app/Home.py
```

### Étape 3 : Accès

Ouvrez votre navigateur : **http://localhost:8501**

---

##  Module Chat Interactif

###  Objectif

Dialoguer avec un patient (simulé ou réel) pour collecter les informations nécessaires au triage, puis obtenir une prédiction de gravité.

---

###  Processus Complet

#### **1. Démarrer une Conversation**

1. Cliquez sur **" Chat Interactif"** dans la sidebar
2. Cliquez sur le bouton **" Démarrer l'Entretien"**

![Start](https://via.placeholder.com/600x100/667eea/ffffff?text=Bouton+Démarrer)

#### **2. Identité du Patient**

Le bot va d'abord demander :
- **Prénom**
- **Âge**
- **Sexe**

**Exemples de réponses acceptées :**

```
 "Marie, 35 ans, femme"
 "Jean" (puis "30 ans" puis "homme")
 "Mohammed 45 H"
 "Sophie" "42" "F"
```

**Le bot comprend :**
- Réponses complètes ou partielles
- Majuscules/minuscules
- Abréviations (H/F, M/F)

#### **3. Symptôme Principal**

Le bot demande : *"Quel est votre symptôme principal ?"*

**Exemples acceptés :**

```
 "J'ai mal au ventre"
 "Douleur thoracique"
 "mal de tête"
 "fièvre"
 "je tousse beaucoup"
```

**Le bot extrait automatiquement :**
- Type de douleur
- Localisation
- Symptôme en langage simple

#### **4. Constantes Vitales**

Le bot va ensuite demander **5 constantes** dans l'ordre :

#####  **1. Température**

**Question :** *"Quelle est votre température ?"*

**Réponses acceptées :**
```
 37.5
 38
 39°C
 37,5
 trente-sept
```

**Si vous ne savez pas :**
```
User: "je ne sais pas"
Bot: "Pas de problème ! Tapez 37 (température normale)"
```

**Plage valide :** 35.0 - 42.0°C

---

#####  **2. Fréquence Cardiaque (FC)**

**Question :** *"Quelle est votre fréquence cardiaque (pouls) ?"*

**Réponses acceptées :**
```
 80
 90 bpm
 mon coeur bat à 85
```

**Aide si besoin :**
```
1. Posez 2 doigts sur votre poignet
2. Comptez pendant 15 secondes
3. Multipliez par 4
```

**Plage valide :** 30 - 250 bpm

---
#####  **3. Tension Artérielle (TA)**

**Question :** *"Quelle est votre tension artérielle ?"*

**Réponses acceptées :**
```
 120/80
 12/8 (converti auto en 120/80)
 140/90
 13/9
```

**Si juste un chiffre :**
```
User: "120"
Bot:  Assume 120/80
```

**Plage valide :**
- Systolique : 50-250 mmHg
- Diastolique : 30-150 mmHg

---

#####  **4. Saturation Oxygène (SpO2)**

**Question :** *"Quelle est votre saturation en oxygène ?"*

**Réponses acceptées :**
```
 98
 95%
 saturation 97
```

**Plage valide :** 50 - 100%

---

#####  **5. Fréquence Respiratoire (FR)**

**Question :** *"Quelle est votre fréquence respiratoire ?"*

**Réponses acceptées :**
```
 16
 18/min
 je respire 20 fois par minute
```

**Aide si besoin :**
```
Comptez combien de fois vous respirez
pendant 1 minute (inspiration + expiration = 1)
```

**Plage valide :** 5 - 60/min

---

#### **5. Prédiction de Gravité**

Une fois les **5 constantes** collectées :

1. Cliquez sur **" Prédire la Gravité"** dans la sidebar
2. Le système analyse avec :
   - **Machine Learning** (Random Forest)
   - **RAG** (si disponible)
3. Vous obtenez :
   - **Niveau de gravité** (🔴 ROUGE, 🟡 JAUNE, 🟢 VERT, ⚪ GRIS)
   - **Action recommandée**
   - **Drapeaux rouges** (si présents)
   - **Probabilités** pour chaque niveau
   - **Niveau de confiance**
   - **Justification médicale**

---

###  Interprétation des Résultats

####  **ROUGE - Urgence Vitale**

```
Label:  URGENCE VITALE
Action: Prise en charge immédiate
Exemples: Infarctus, AVC, détresse respiratoire
```

**Que faire ?**
-  Appeler le 15 (SAMU)
-  Intervention immédiate
-  Ne pas déplacer le patient

---

#### 🟡 **JAUNE - Urgent**

```
Label: 🟡 URGENCE
Action: Consultation dans l'heure
Exemples: Fracture, douleur intense, fièvre élevée
```

**Que faire ?**
-  Aller aux urgences rapidement
-  Dans l'heure maximum
-  Transport possible en voiture

---

#### 🟢 **VERT - Non Urgent**

```
Label: 🟢 NON URGENT
Action: Consultation sous 24-48h
Exemples: Entorse légère, rhume, plaie superficielle
```

**Que faire ?**
-  Prendre RDV médecin
-  Sous 24-48h
-  Surveillance à domicile OK

---

#### ⚪ **GRIS - Pas d'Urgence**

```
Label: ⚪ PAS D'URGENCE
Action: Médecin traitant
Exemples: Problème chronique, consultation de suivi
```

**Que faire ?**
-  Consulter médecin traitant
-  Prendre RDV normal
-  Pas besoin des urgences

---

###  Exporter le Rapport

Cliquez sur **" Exporter le Rapport"** pour télécharger :

**Contenu du rapport :**
```markdown
# RAPPORT DE TRIAGE

## 🔴 URGENCE VITALE

**Action:** Prise en charge immédiate

**Confiance:** 92.5%

##  Drapeaux Rouges
- Tachycardie (130 bpm)
- Hypoxie (88%)

##  Conversation
[Historique complet]

##  Constantes
- FC : 130 bpm
- SpO2 : 88%
...
```

---

##  Module Génération

###  Objectif

Créer des conversations synthétiques pour :
- Entraîner des modèles ML
- Tester le système
- Simuler des scénarios

---

###  Utilisation

#### **Génération Aléatoire**

1. Allez sur **" Génération"**
2. Laissez le champ **"Pathologie"** vide
3. Cliquez sur :
   - **" Générer 1"** → 1 conversation
   - **" Générer 10"** → 10 conversations

**Le système crée automatiquement :**
- Profil patient réaliste
- Symptômes cohérents
- Constantes adaptées
- Conversation complète

---

#### **Génération Guidée**

1. Entrez une **pathologie** :
   ```
   Exemples:
   - "Infarctus du myocarde"
   - "Pneumonie sévère"
   - "Fracture du poignet"
   - "Gastro-entérite"
   ```

2. Cliquez **" Générer 1"**

3. Le système adapte :
   - **Symptômes** à la pathologie
   - **Constantes** cohérentes
   - **Gravité** attendue

**Exemple - Infarctus :**
```python
Constantes générées:
- FC: 110-130 bpm (tachycardie)
- SpO2: 88-92% (hypoxie légère)
- TA: 90-100/60-70 (hypotension)
- Température: 36.5-37.5°C (normale)
```

---

###  Voir les Résultats

**Onglets disponibles :**

1. ** Conversation**
   - Dialogue complet infirmier ↔ patient
   - Messages animés

2. ** Patient**
   - Identité
   - Symptômes
   - Antécédents

3. ** Extraction**
   - Score de complétude
   - Infos manquantes
   - Constantes extraites

4. ** Données ML**
   - Format JSON
   - Prêt pour training
   - Téléchargeable

---

###  Exporter le Dataset

**Format JSON :**
```json
[
  {
    "id": "uuid-123",
    "age": 45,
    "sexe": "M",
    "symptomes": ["Douleur thoracique"],
    "constantes": {
      "fc": 120,
      "fr": 22,
      "spo2": 90,
      ...
    },
    "gravite": "ROUGE"
  },
  ...
]
```

**Format CSV :**
```csv
id,age,sexe,fc,fr,spo2,ta_sys,ta_dia,temp,gravite
uuid-123,45,M,120,22,90,110,70,37.2,ROUGE
...
```

**Utilisation :**
```python
import pandas as pd

# Charger
df = pd.read_csv("dataset_triage.csv")

# Features
X = df[['fc', 'fr', 'spo2', ...]]
y = df['gravite']

# Entraîner
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X, y)
```

---

##  Module Monitoring

###  Objectif

Suivre les performances du système en temps réel.

---

###  Métriques Suivies

#### ** Coûts API**

**Affiche :**
- Coût total consommé
- Répartition par service :
  - Mistral AI (LLM)
  - Embeddings (RAG)
- Évolution temporelle
- Budget warnings

**Graphiques :**
-  Pie chart répartition
-  Ligne évolution
-  Gauge budget

---

#### **⏱ Latences**

**Mesure le temps de réponse :**
- Chatbot (dialogue)
- ML Predictor (classification)
- RAG Retrieval (recherche)

**Visualisations :**
-  Box plots par composant
-  Évolution temporelle
-  Heatmap horaire

---

#### ** Prédictions**

**Statistiques :**
- Nombre total
- Distribution par gravité
- Taux de confiance moyen
- Red flags détectés

**Graphiques :**
-  Pie chart gravités
-  Histogramme confiance
-  Timeline prédictions

---

###  Rafraîchissement

- **Auto-refresh** : Toutes les 30s
- **Manuel** : Bouton " Rafraîchir"

---

##  FAQ

### **Q : Le chatbot répète la même question**

**R :** Vérifiez que vous utilisez le fichier `chatbot_PARFAIT.py`. L'ancienne version avait ce bug.

---

### **Q : "Je ne sais pas ma tension"**

**R :** Pas de problème ! Dites juste "je ne sais pas" et le bot vous proposera une valeur normale (120/80).

---

### **Q : Le bot ne comprend pas ma réponse**

**R :** Le bot accepte plein de variantes. Exemples :
```
 "jdlqksjdlkqsjd" → Pas compris
 "37" → Compris (température)
 "j'ai mal" → Compris (douleur)
 "80 bpm" → Compris (FC)
```

---

### **Q : Combien coûte une prédiction ?**

**R :** ~0.002$ par conversation complète (Mistral API)

---

### **Q : Le RAG est optionnel ?**

**R :** Oui ! Le système fonctionne sans RAG (juste ML). Le RAG enrichit juste les explications.

---

### **Q : Puis-je utiliser sans API Mistral ?**

**R :** Oui, en mode "règles" (moins intelligent). Mais recommandé avec API.

---

##  Résolution de Problèmes

### **Erreur : "MISTRAL_API_KEY not found"**

**Solution :**
```bash
# Vérifiez .env
cat .env

# Devrait contenir :
MISTRAL_API_KEY=votre_clé_ici

# Si absent, ajoutez-le
echo "MISTRAL_API_KEY=sk-..." >> .env
```

---

### **Erreur : "Module not found"**

**Solution :**
```bash
# Réinstaller dépendances
pip install -r requirements.txt

# Vérifier environnement virtuel actif
which python  # Doit pointer vers venv/
```

---

### **Le chatbot boucle à l'infini**

**Solution :**
```bash
# Utiliser la dernière version
cp chatbot_PARFAIT.py src/rag/chatbot.py

# Relancer
streamlit run app/Home.py
```

---

### **Constantes pas extraites**

**Vérifiez les valeurs :**
```
Température : 35-42°C
FC : 30-250 bpm
TA : 50-250 / 30-150 mmHg
SpO2 : 50-100%
FR : 5-60/min
```

Hors de ces plages → rejeté automatiquement

---

##  Astuces & Bonnes Pratiques

###  **DO - À Faire**

```diff
+ Répondre naturellement (le bot comprend)
+ Dire "je ne sais pas" si incertain
+ Utiliser des chiffres simples (37, 80, 120/80)
+ Exporter les rapports importants
+ Consulter le monitoring régulièrement
```

---

###  **DON'T - À Éviter**

```diff
- N'inventez pas de valeurs irréalistes
- Ne tapez pas n'importe quoi
- N'utilisez pas de caractères spéciaux
- Ne spammez pas le bot
- Ne partagez pas de vraies données médicales sensibles
```

---

###  **Raccourcis Clavier**

```
Ctrl + R : Rafraîchir la page
Ctrl + K : Ouvrir la recherche
Esc : Fermer les popups
```

---

###  **Version Mobile**

Le site est **responsive** :
-  Smartphone
-  Tablette
-  Desktop

Optimisé pour tous les écrans !

---

##  Tutoriels Vidéo

*Coming soon...*

-  Installation complète (5 min)
-  Premier triage (3 min)
-  Génération de datasets (4 min)
-  Analyse du monitoring (6 min)

---

##  Besoin d'Aide ?

**Support :**
-  Email : support@triage-ia.com
-  Discord : [Rejoindre](https://discord.gg/votre-serveur)
-  Issues : [GitHub](https://github.com/votre-username/triage-urgence/issues)

---

<div align="center">

** Guide d'Utilisation v2.0**

*Mis à jour le 02/02/2026*

**[⬆Retour en haut](#-guide-dutilisation---système-de-triage-médical-ia)**

</div>
