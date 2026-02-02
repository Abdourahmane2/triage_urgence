# Système de Triage Intelligent des Urgences

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![Python](https://img.shields.io/badge/python-3.9+-green.svg) ![License](https://img.shields.io/badge/license-MIT-orange.svg) ![Status](https://img.shields.io/badge/status-production-success.svg)

**Un système d'aide à la décision médicale combinant Intelligence Artificielle et Machine Learning pour optimiser le triage des patients aux urgences**

[Démarrage Rapide](#démarrage-rapide) • [Architecture](#architecture) • [Documentation](#documentation) • [Démo](#démo)

---

## Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Monitoring](#monitoring)
- [Contribution](#contribution)

---

## Vue d'ensemble

### Le Problème

Les services d'urgences font face à un défi majeur : **trier rapidement et efficacement** les patients selon la gravité de leur état. Un mauvais triage peut avoir des conséquences graves :

- Retard dans la prise en charge des urgences vitales
- Risque pour le pronostic vital
- Engorgement des urgences

### Notre Solution

Un **système intelligent** qui assiste les infirmiers d'accueil en :

1. Collectant les informations via un chatbot conversationnel
2. Analysant les constantes vitales avec un modèle ML
3. Enrichissant les recommandations via des protocoles médicaux (RAG)
4. Prédisant le niveau de gravité : ROUGE / JAUNE / VERT / GRIS

---

## Fonctionnalités

### 1. Chatbot Conversationnel Intelligent

```
┌─────────────────────────────────────┐
│ Assistant Mistral AI                │
│                                     │
│ Bot: Bonjour, quel est votre       │
│      symptôme principal ?          │
│                                     │
│ Patient: Mal de tête violent       │
│                                     │
│ Bot: Quelle est votre température? │
│      Exemple: 38.5                 │
│                                     │
│ Patient: 39.2                      │
│                                     │
│ Collecte automatique des           │
│ 5 constantes vitales               │
└─────────────────────────────────────┘
```

**Caractéristiques :**

- Mistral Large pour compréhension naturelle
- Extraction automatique des données
- Validation des constantes en temps réel
- Guide l'infirmier étape par étape

### 2. Prédiction Machine Learning

```
┌──────────────────────────────────────┐
│ Modèle: Random Forest                │
│                                      │
│ Entrées (8 features):                │
│ ├─ FC: 130 bpm                       │
│ ├─ FR: 25/min                        │
│ ├─ SpO2: 92%                         │
│ ├─ TA: 160/95 mmHg                   │
│ ├─ Temp: 39.5°C                      │
│ ├─ Âge: 65 ans                       │
│ └─ Sexe: H                           │
│                                      │
│ Sortie:                              │
│ ROUGE - 87% confiance                │
│ "Urgence vitale immédiate"           │
└──────────────────────────────────────┘
```

**Performances :**

- Précision : ~70%
- Temps de prédiction : <0.5s
- 4 classes : ROUGE, JAUNE, VERT, GRIS

### 3. RAG (Retrieval Augmented Generation)

```
┌─────────────────────────────────────────┐
│ Base documentaire médicale              │
│                                         │
│ Recherche: "ROUGE + Tachycardie"        │
│                                         │
│ Protocole trouvé:                       │
│ ┌───────────────────────────────────┐   │
│ │ "Urgence vitale:                  │   │
│ │ • APPELER SMUR                    │   │
│ │ • Monitoring continu              │   │
│ │ • Voie veineuse                   │   │
│ │ • NE PAS faire attendre"          │   │
│ └───────────────────────────────────┘   │
│                                         │
│ Sources: Protocoles urgences 2024       │
└─────────────────────────────────────────┘
```

**Avantages :**

- 303 chunks de protocoles médicaux
- Recherche sémantique pertinente
- Recommandations contextualisées
- Sources citées

### 4. Monitoring en Temps Réel

```
┌──────────────────────────────────┐
│ Coûts API                        │
│ Total: 2.5c€ aujourd'hui         │
│ ├─ Mistral: 2.0c€                │
│ └─ Embeddings: 0.5c€             │
│                                  │
│ Appels API: 150                  │
│ Latence moy: 0.35s               │
│ Prédictions: 45                  │
│                                  │
│ Distribution gravité:            │
│ ROUGE: 12 (27%)                  │
│ JAUNE: 18 (40%)                  │
│ VERT: 12 (27%)                   │
│ GRIS: 3 (6%)                     │
└──────────────────────────────────┘
```

---

## Architecture

### Vue d'ensemble simplifiée

```
┌─────────────────────────────────────────────────────────────────────┐
│ INTERFACE STREAMLIT                                                 │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│ │Génération│ │Prédiction│ │ Chatbot  │ │Monitoring│               │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘               │
└─────────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ COUCHE MÉTIER                                                       │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐    │
│ │ Chatbot API      │ │ ML Predictor     │ │ RAG System       │    │
│ │                  │ │                  │ │                  │    │
│ │ Mistral Large    │ │ Random Forest    │ │ Vector Store     │    │
│ │                  │ │                  │ │                  │    │
│ │ • Conversation   │ │ • 8 features     │ │ • 303 chunks     │    │
│ │ • Extraction     │ │ • 4 classes      │ │ • Semantic       │    │
│ │ • Validation     │ │ • 85% accuracy   │ │   search         │    │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ COUCHE DONNÉES                                                      │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐    │
│ │ Metrics Tracker  │ │ Models           │ │ Documents        │    │
│ │                  │ │                  │ │                  │    │
│ │ • API calls      │ │ • RF Model       │ │ • Protocoles     │    │
│ │ • Latences       │ │   (.pkl)         │ │   médicaux       │    │
│ │ • Prédictions    │ │ • Embeddings     │ │ • Cas cliniques  │    │
│ │ • Coûts          │ │                  │ │                  │    │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### Workflow Détaillé

#### Étape 1 : Conversation (Chatbot)

```
┌─────────┐
│ Patient │
└────┬────┘
     │ "J'ai mal à la tête"
     ▼
┌─────────────────────┐
│ Mistral Large API   │
│ ┌───────────────┐   │
│ │ System Prompt │   │ ← Instructions intelligentes
│ │ + Contexte    │   │   selon l'étape
│ └───────────────┘   │
│         │           │
│         ▼           │
│ ┌───────────────┐   │
│ │ Génération    │   │ → "Quelle est votre
│ │ Réponse       │   │    température ?"
│ └───────────────┘   │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Extraction Auto     │
│ • Regex patterns    │
│ • Validation        │
│ • Storage           │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ État Patient        │
│ ├─ Prénom: Jean     │
│ ├─ Âge: 65          │
│ ├─ Symptômes: [...] │
│ └─ Constantes: 4/5  │ ← Progression
└─────────────────────┘
```

#### Étape 2 : Prédiction ML

```
┌──────────────────────┐
│ Données Patient      │
│ ┌────────────────┐   │
│ │ FC: 130 bpm    │   │
│ │ FR: 25/min     │   │
│ │ SpO2: 92%      │   │
│ │ TA: 160/95     │   │
│ │ Temp: 39.5°C   │   │
│ │ Âge: 65        │   │
│ │ Sexe: H        │   │
│ └────────────────┘   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Préparation Features │
│ • Normalisation      │
│ • Encoding sexe      │
│ • Vector [8]         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Random Forest        │
│ ┌────────────────┐   │
│ │ 100 arbres     │   │
│ │ Max depth: 10  │   │
│ └────────────────┘   │
│         │            │
│         ▼            │
│ ┌────────────────┐   │
│ │ predict()      │   │
│ │ predict_proba()│   │
│ └────────────────┘   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Résultat             │
│ • Classe: ROUGE      │
│ • Confiance: 87%     │
│ • Probas: {...}      │
└──────────────────────┘
```

#### Étape 3 : Enrichissement RAG

```
┌──────────────────────┐
│ Niveau: ROUGE        │
│ Symptômes: [...]     │
│ Red flags: [...]     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Requête RAG          │
│ "protocole ROUGE     │
│  tachycardie fièvre" │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Vector Store         │
│ ┌────────────────┐   │
│ │ ChromaDB       │   │
│ │ 303 chunks     │   │
│ │ Embeddings     │   │
│ │ 384 dim        │   │
│ └────────────────┘   │
│         │            │
│         ▼            │
│ Recherche sémantique │
│ (cosine similarity)  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Top 3 Chunks         │
│ ┌────────────────┐   │
│ │ Chunk 1:       │   │
│ │ "Urgence..."   │   │
│ │ Score: 0.92    │   │
│ ├────────────────┤   │
│ │ Chunk 2:       │   │
│ │ "Protocole..." │   │
│ │ Score: 0.88    │   │
│ ├────────────────┤   │
│ │ Chunk 3:       │   │
│ │ "Actions..."   │   │
│ │ Score: 0.85    │   │
│ └────────────────┘   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Justification        │
│ Enrichie             │
│                      │
│ "ML: ROUGE           │
│  RAG:                │
│  • SMUR              │
│  • Monitoring        │
│  • Urgence"          │
└──────────────────────┘
```

#### Étape 4 : Monitoring

```
┌──────────────────────┐
│ Actions Trackées     │
└──────────┬───────────┘
           │
     ├─────────────────────────┐
     │                         │
     ▼                         ▼
┌──────────────────┐   ┌──────────────────┐
│ API Calls        │   │ Latences         │
│ ┌────────────┐   │   │ ┌────────────┐   │
│ │ Service    │   │   │ │ Component  │   │
│ │ Model      │   │   │ │ Operation  │   │
│ │ Tokens in  │   │   │ │ Duration   │   │
│ │ Tokens out │   │   │ └────────────┘   │
│ │ Latency    │   │   │                  │
│ │ Success    │   │   │ Chatbot: 0.05s   │
│ └────────────┘   │   │ ML: 0.35s        │
│                  │   │ RAG: 0.12s       │
│ → api_calls.json │   │ → latencies.json │
└──────────────────┘   └──────────────────┘
           │
           ▼
┌──────────────────────┐
│ Prédictions          │
│ ┌────────────┐       │
│ │ Severity   │       │
│ │ Age/Sex    │       │
│ │ Red flags  │       │
│ │ Confidence │       │
│ └────────────┘       │
│                      │
│ → predictions.json   │
└──────────────────────┘
           │
           ▼
┌──────────────────────┐
│ Calcul Coûts         │
│ ┌────────────┐       │
│ │ Mistral:   │       │
│ │ 1€/1M in   │       │
│ │ 3€/1M out  │       │
│ └────────────┘       │
│                      │
│ Total: 2.5c€         │
└──────────────────────┘
```

### Structure du Projet

```
triage-urgences/
│
├── app/                        # Interface Streamlit
│   ├── Home.py                 # Page d'accueil
│   └── pages/
│       ├── 1_Generation.py     # Génération conversations IA
│       ├── 2_Prediction.py     # Prédictions ML standalone
│       ├── 3_Chatbot_RAG.py    # Chatbot intelligent complet
│       └── 4_Monitoring.py     # Dashboard monitoring
│
├── src/                        # Code source
│   ├── rag/
│   │   ├── chatbot.py          # Chatbot Mistral Large
│   │   ├── predictor.py        # Prédicteur ML + RAG
│   │   ├── vector_store.py     # ChromaDB management
│   │   └── document_loader.py  # Chargement documents
│   │
│   ├── monitoring/
│   │   ├── metrics_tracker.py  # Tracking métriques
│   │   └── cost_calculator.py  # Calcul coûts API
│   │
│   ├── models/
│   │   └── random_forest_simple.pkl  # Modèle ML entraîné
│   │
│   └── llm/
│       └── llm_factory.py      # Factory Mistral API
│
├── data/                       # Données
│   ├── vector_db/              # Base ChromaDB
│   ├── rag_documents/          # Documents médicaux
│   │   ├── 1_arbre_questions.md
│   │   ├── 2_criteres_classification.md
│   │   ├── 3_signes_alerte.md
│   │   ├── 4_protocoles_action.md
│   │   └── 5_cas_exemples.md
│   │
│   └── monitoring/             # Métriques
│       ├── api_calls.json
│       ├── latencies.json
│       └── predictions.json
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01_test_clinical_bert.ipynb
│   ├── 02_feature_extraction.ipynb
│   ├── 03_generate_dataset.ipynb
│   └── 04_train_model.ipynb
│
├── .env                        # Variables d'environnement
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

---

## Technologies

### Intelligence Artificielle

| Technologie | Usage | Pourquoi |
|-------------|-------|----------|
| **Mistral Large** | Chatbot conversationnel | Meilleure compréhension du langage naturel, génération de questions pertinentes, adaptation au contexte |
| **Random Forest** | Prédiction gravité | Robuste aux données manquantes, interprétabilité, rapide en production |
| **ChromaDB** | Recherche sémantique | Recherche vectorielle efficace, stockage persistant, scaling facile |
| **Sentence Transformers** | Embeddings | Support multilingue, embeddings de qualité, léger et rapide |

### Stack Technique

```
┌─────────────────────────────────────────┐
│ Frontend / UI                           │
│ • Streamlit 1.31+                       │
│ • Plotly (graphiques interactifs)       │
│ • Markdown (formatting)                 │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│ Backend / Logic                         │
│ • Python 3.9+                           │
│ • Mistral AI API                        │
│ • scikit-learn (ML)                     │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│ Data Layer                              │
│ • ChromaDB (vector store)               │
│ • JSON (metrics storage)                │
│ • Pickle (model serialization)          │
└─────────────────────────────────────────┘
```

**Dépendances principales :**

```python
streamlit>=1.31.0
mistralai>=0.1.0
scikit-learn>=1.3.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
plotly>=5.18.0
python-dotenv>=1.0.0
```

---

## Installation

### Prérequis

- Python 3.9 ou supérieur
- Clé API Mistral (gratuite : https://console.mistral.ai)

### Installation Rapide

```bash
# 1. Cloner le repository
git clone https://github.com/Abdourahmane2/triage_urgence/
cd triage-urgences

# 2. Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configuration
cp .env.example .env
# Éditer .env et ajouter votre clé API Mistral

# 5. Créer structure de données
mkdir -p data/monitoring
mkdir -p data/vector_db
mkdir -p src/models

# 6. Initialiser RAG (optionnel)
python src/rag/build_rag.py

# 7. Lancer l'application
streamlit run app/Home.py
```

### Configuration `.env`

```bash
# API Keys
MISTRAL_API_KEY=votre_cle_api_ici

# Paths
MODEL_PATH=src/models/random_forest_simple.pkl
VECTOR_DB_PATH=data/vector_db

# Settings
MAX_TOKENS=100
TEMPERATURE=0.4
```

---

## Utilisation

### Page Génération (Entraînement)

**Objectif:** Générer des données synthétiques pour entraîner le modèle

1. Cliquer sur "Générer 1 conversation"
2. Le système simule un dialogue infirmier-patient
3. Les constantes vitales sont générées automatiquement
4. Télécharger le dataset (JSON/CSV)
5. Utiliser les notebooks pour entraîner le modèle

**Exemple de conversation générée :**

```
Infirmier: Quel est votre symptôme principal ?
Patient: J'ai une douleur thoracique intense

Infirmier: Depuis combien de temps ?
Patient: Depuis 30 minutes

→ Génère automatiquement:
  FC: 120 bpm (tachycardie cohérente)
  SpO2: 94% (hypoxie légère)
  TA: 150/95 (hypertension)
  Temp: 37.2°C

→ Gravité: ROUGE
```

### Page Chatbot RAG (Production)

**Objectif:** Utiliser le système en situation réelle

1. Cliquer "Démarrer la conversation"
2. Répondre aux questions du bot
3. Le bot collecte automatiquement les 5 constantes
4. Cliquer "Obtenir prédiction ML"
5. Consulter le résultat enrichi (ML + RAG)

**Interface :**

```
┌─────────────────────────────────────┐
│ Conversation                        │
│                                     │
│ Bot: Bonjour Jean. Quel est votre  │
│      symptôme ?                     │
│                                     │
│ Vous: Mal de tête intense           │
│                                     │
│ Bot: Température ?                  │
│      Exemple: 38.5                  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Dossier Patient                     │
│                                     │
│ Prénom: Jean                        │
│ Âge: 65                             │
│ Sexe: Homme                         │
│                                     │
│ Symptômes:                          │
│ • Céphalée                          │
│                                     │
│ Constantes: 5/5                     │
│ Temp: 39.5°C                        │
│ FC: 130 bpm                         │
│ TA: 160/95                          │
│ SpO2: 92%                           │
│ FR: 25/min                          │
│                                     │
│ [Obtenir prédiction ML]             │
└─────────────────────────────────────┘
```

### Page Monitoring

**Objectif:** Suivre performance et coûts

- Coûts API en temps réel
- Distribution des prédictions
- Latences par composant
- Graphiques interactifs
- Export CSV des métriques

---

## Monitoring

### Métriques Trackées

| Métrique | Description | Visualisation |
|----------|-------------|---------------|
| **API Calls** | Service, modèle, tokens, latence | Tableau + Graphique évolution |
| **Latences** | Composant, opération, durée | Box plot + Moyenne |
| **Prédictions** | Niveau, âge, sexe, confiance | Pie chart + Stats |
| **Coûts** | Mistral, embeddings, total | Camembert + Projection |

### Dashboard

```
┌─────────────────────────────────────────────────────┐
│ Coût Total              Appels API                  │
│ 2.5c€                   150                         │
│                                                     │
│ Latence Moy             Prédictions                 │
│ 0.35s                   45                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Distribution Gravité                                │
│                                                     │
│ ROUGE ████████░░░░░ 27% (12)                        │
│ JAUNE ████████████░░ 40% (18)                       │
│ VERT  ████████░░░░░ 27% (12)                        │
│ GRIS  ██░░░░░░░░░░░ 6% (3)                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Latences par Composant                              │
│                                                     │
│ Chatbot      ▓░░░░░░░░░ 0.05s                       │
│ ML Predictor ▓▓▓░░░░░░ 0.35s                        │
│ RAG          ▓▓░░░░░░░░ 0.12s                       │
│ Generation   ▓▓▓▓▓▓▓▓░░ 2.50s                       │
└─────────────────────────────────────────────────────┘
```

### Export Données

```bash
# Export automatique en CSV
data/monitoring/
├── api_calls_export_2024-01-31.csv
├── latencies_export_2024-01-31.csv
└── predictions_export_2024-01-31.csv
```

---

## Contribution

### Comment contribuer ?

1. **Fork** le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une **Pull Request**

---

## License

MIT License - Voir [LICENSE](LICENSE) pour plus de détails.

---

## Auteurs

- Bah Mohamed
- Vial Anne-Camille
- Curty-Menez Marvin
- Lecomte Thibaud
- Timera Abdourahmane

**Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**