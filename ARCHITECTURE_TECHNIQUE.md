#  Architecture Technique - Système de Triage IA

<div align="center">

![Architecture](https://img.shields.io/badge/Documentation-Technique-red?style=for-the-badge)
![Niveau](https://img.shields.io/badge/Niveau-Avancé-orange?style=for-the-badge)

**Documentation technique complète du système**

</div>

---

##  Table des Matières

1. [ Vue d'Ensemble](#-vue-densemble)
2. [ Architecture Globale](#️-architecture-globale)
3. [ Structure du Projet](#-structure-du-projet)
4. [ Composants Principaux](#-composants-principaux)
5. [ Flux de Données](#-flux-de-données)
6. [ Stockage & Persistance](#️-stockage--persistance)
7. [ Intelligence Artificielle](#-intelligence-artificielle)
8. [ Monitoring & Métriques](#-monitoring--métriques)
9. [ Sécurité](#-sécurité)
10. [ Performance](#-performance)

---

##  Vue d'Ensemble

### Philosophie du Système

Le système suit une **architecture en couches** avec séparation claire des responsabilités :

```
┌─────────────────────────────────────────┐
│         PRÉSENTATION (UI)               │  ← Streamlit
├─────────────────────────────────────────┤
│      ORCHESTRATION (Workflows)          │  ← Business Logic
├─────────────────────────────────────────┤
│   AGENTS (IA Conversationnelle)         │  ← Intelligent Agents
├─────────────────────────────────────────┤
│      SERVICES (ML, RAG, LLM)            │  ← AI Services
├─────────────────────────────────────────┤
│     MODÈLES (Data & Domain)             │  ← Data Models
└─────────────────────────────────────────┘
```

### Principes de Design

1. **Modularité** : Composants indépendants et réutilisables
2. **Extensibilité** : Facile d'ajouter de nouvelles features
3. **Maintenabilité** : Code clair et documenté
4. **Performance** : Optimisations ciblées
5. **Robustesse** : Gestion d'erreurs complète

---

##  Architecture Globale

### Diagramme Complet

```
┌───────────────────────────────────────────────────────────────┐
│                        UTILISATEUR                             │
│                     (Navigateur Web)                           │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APP                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   Home   │  │   Chat   │  │ Generate │  │ Monitor  │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                       WORKFLOWS                                │
│  ┌─────────────────────────┐  ┌─────────────────────────┐   │
│  │  InteractiveWorkflow    │  │  SimulationWorkflow     │   │
│  │  (Chat Interactif)      │  │  (Génération)           │   │
│  └─────────────────────────┘  └─────────────────────────┘   │
└───────────────────────────────┬───────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   AGENTS     │      │   SERVICES   │      │   STORAGE    │
│              │      │              │      │              │
│ • Nurse      │      │ • LLM        │      │ • ChromaDB   │
│ • Patient    │      │ • ML         │      │ • JSON       │
│ • Analyzer   │      │ • RAG        │      │ • Pickle     │
└──────────────┘      └──────────────┘      └──────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Mistral AI  │  │ Embeddings   │  │  Monitoring  │       │
│  │  (API)       │  │ (HuggingFace)│  │  (Local)     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────────────────────────────────────────────┘
```

---

##  Structure du Projet

### Arborescence Détaillée

```
triage-urgence/
│
├── 📁 app/                          # Interface Streamlit
│   ├── Home.py                      # Page d'accueil
│   ├── styles.css                   # CSS global
│   │
│   ├── 📁 pages/                    # Pages Streamlit
│   │   ├── Chat_interactif.py       # Module chat
│   │   ├── Generation.py            # Génération datasets
│   │   └── Monitoring.py            # Dashboard analytics
│   │
│   └── 📁 data/                     # Données UI
│       ├── 📁 monitoring/           # Logs monitoring
│       │   ├── api_calls.json
│       │   ├── latencies.json
│       │   └── predictions.json
│       │
│       └── 📁 vector_db/            # Base ChromaDB locale
│
├── 📁 src/                          # Code source métier
│   │
│   ├── 📁 agents/                   # Agents intelligents
│   │   ├── base_agent.py            # Classe abstraite
│   │   ├── nurse_agent.py           # Agent infirmier
│   │   ├── patient_simulator.py    # Simulateur patient
│   │   ├── patient_generator.py    # Générateur profils
│   │   └── conversation_analyzer.py # Analyseur dialogue
│   │
│   ├── 📁 llm/                      # LLM Providers
│   │   ├── base_llm.py              # Interface LLM
│   │   ├── llm_factory.py           # Factory pattern
│   │   └── mistral_provider.py     # Provider Mistral
│   │
│   ├── 📁 rag/                      # RAG System
│   │   ├── chatbot.py               # Chatbot principal
│   │   ├── predictor.py             # ML + RAG prédiction
│   │   ├── document_loader.py       # Chargement docs
│   │   ├── embeddings.py            # Sentence transformers
│   │   ├── vector_store.py          # ChromaDB wrapper
│   │   └── retriever.py             # Retrieval logic
│   │
│   ├── 📁 models/                   # Modèles de données
│   │   ├── conversation.py          # Messages & historique
│   │   ├── patient.py               # Patient & constantes
│   │   ├── triage.py                # Résultat triage
│   │   └── random_forest_simple.pkl # Modèle ML persisté
│   │
│   ├── 📁 workflows/                # Orchestration
│   │   ├── interactive_workflow.py  # Workflow chat
│   │   └── simulation_workflow.py  # Workflow génération
│   │
│   ├── 📁 monitoring/               # Métriques & logs
│   │   ├── metrics_tracker.py       # Tracking metrics
│   │   └── cost_calculator.py      # Calcul coûts API
│   │
│   └── 📁 utils/                    # Utilitaires
│       ├── logger.py                # Logging config
│       └── validators.py            # Validations
│
├── 📁 data/                         # Données & ressources
│   ├── 📁 rag_document/             # Docs pour RAG
│   │   ├── protocoles_action.md
│   │   ├── criteres_classification.md
│   │   ├── arbre_questions.md
│   │   ├── signes_alerte.md
│   │   └── cas_exemples.md
│   │
│   └── 📁 vector_db/                # Base vectorielle
│       └── chroma.sqlite3
│
├── 📁 config/                       # Configuration
│   ├── settings.py                  # Paramètres globaux
│   └── prompts.py                   # Prompts LLM
│
├── 📁 tests/                        # Tests unitaires
│   ├── test_chatbot.py
│   ├── test_ml.py
│   └── test_rag.py
│
├── .env                             # Variables d'environnement
├── .env.example                     # Template .env
├── requirements.txt                 # Dépendances Python
├── README.md                        # Documentation principale
└── LICENSE                          # Licence MIT
```

---

## 🔧 Composants Principaux

### 1. Chatbot (src/rag/chatbot.py)

**Responsabilité :** Orchestrer le dialogue de triage

**Classe Principale :**
```python
class TriageChatbotAPI:
    """Chatbot ultra robuste pour tous utilisateurs."""
    
    def __init__(self, api_key, retriever):
        # Initialisation Mistral + RAG
        
    def chat(self, user_message: str) -> str:
        # Logique principale
        # 1. Extraction infos
        # 2. Déterminer étape
        # 3. Générer réponse
        
    def _extract_everything(self, msg: str):
        # Extraction agressive multi-formats
        
    def is_ready_for_prediction(self) -> bool:
        # Vérifier complétude données
```

**Features Clés :**
-  Extraction temps réel (5 constantes + identité)
-  Validation automatique des valeurs
-  Adaptation niveau utilisateur
-  Gestion "je ne sais pas"
-  Questions progressivement simplifiées

---

### 2. ML Predictor (src/rag/predictor.py)

**Responsabilité :** Prédire la gravité avec ML + RAG

**Classe Principale :**
```python
class MLTriagePredictor:
    """Prédiction Random Forest + enrichissement RAG."""
    
    def __init__(self, model_path, rag_retriever):
        # Charger modèle + RAG
        
    def predict(self, chatbot_summary: Dict) -> Dict:
        # 1. Préparer features
        # 2. Prédire avec RF
        # 3. Enrichir avec RAG
        # 4. Générer justification
        # 5. Retourner résultat complet
        
    def _red_flags(self, vitals, symptoms) -> List[str]:
        # Détection drapeaux rouges
```

**Pipeline de Prédiction :**
```
Input: Résumé chatbot
  ↓
1. Extraction features (8 dimensions)
  ↓
2. Normalisation valeurs
  ↓
3. Random Forest predict
  ↓
4. Calcul probabilités
  ↓
5. Détection red flags
  ↓
6. RAG retrieval (contexte médical)
  ↓
7. Génération justification
  ↓
Output: Résultat complet
```

---

### 3. Random Forest (src/models/random_forest_simple.pkl)

**Architecture ML :**

```python
RandomForestClassifier(
    n_estimators=100,      # 100 arbres
    max_depth=20,          # Profondeur max
    min_samples_split=5,   # Split minimum
    min_samples_leaf=2,    # Leaf minimum
    random_state=42        # Reproductibilité
)
```

**Features (8 dimensions) :**

| # | Feature | Type | Plage | Normalisation |
|---|---------|------|-------|---------------|
| 1 | FC | int | 30-250 | (x-70)/30 |
| 2 | FR | int | 5-60 | (x-16)/5 |
| 3 | SpO2 | int | 50-100 | (x-95)/5 |
| 4 | TA_sys | int | 50-250 | (x-120)/20 |
| 5 | TA_dia | int | 30-150 | (x-80)/10 |
| 6 | Temp | float | 35-42 | (x-37)/2 |
| 7 | Age | int | 0-120 | (x-50)/25 |
| 8 | Sexe | binary | 0/1 | One-hot |

**Classes (4) :**
- 0 → GRIS
- 1 → VERT  
- 2 → JAUNE
- 3 → ROUGE

---

### 4. RAG System (src/rag/)

**Architecture RAG :**

```
Documents Markdown
       ↓
   Chunking (800 chars, overlap 150)
       ↓
   Embeddings (MiniLM-L12-v2, 384 dims)
       ↓
   ChromaDB (persistance)
       ↓
   Retrieval (similarité cosinus, top-3)
       ↓
   Context enrichment
```

**Composants :**

1. **DocumentLoader** : Charge et découpe docs
2. **EmbeddingProvider** : Génère embeddings
3. **VectorStore** : Interface ChromaDB
4. **RAGRetriever** : Récupère contexte

**Documents Indexés :**
- `protocoles_action.md` (500 chunks)
- `criteres_classification.md` (300 chunks)
- `arbre_questions.md` (400 chunks)
- `signes_alerte.md` (200 chunks)
- `cas_exemples.md` (600 chunks)

**Total :** ~2000 chunks, ~1.6M tokens

---

### 5. Monitoring (src/monitoring/)

**Métriques Trackées :**

```python
class MetricsTracker:
    """Singleton tracking toutes les métriques."""
    
    def track_api_call(self, service, model, tokens, latency):
        # Log appel API
        
    def track_latency(self, component, operation, duration):
        # Log latence
        
    def track_prediction(self, severity, age, sex, confidence):
        # Log prédiction
```

**Stockage :**
```json
// app/data/monitoring/api_calls.json
[
  {
    "timestamp": "2026-02-02T10:30:00",
    "service": "mistral",
    "model": "mistral-large-latest",
    "tokens_input": 450,
    "tokens_output": 120,
    "cost": 0.0023,
    "latency": 1.2
  }
]
```

---

##  Flux de Données

### Workflow Chat Interactif

```
1. User clique "Démarrer"
        ↓
2. Chatbot.start() → Message initial
        ↓
3. User tape réponse
        ↓
4. Chatbot.chat(msg)
   ├─→ _extract_everything(msg)
   │   ├─→ _extract_prenom()
   │   ├─→ _extract_age()
   │   ├─→ _extract_sexe()
   │   ├─→ _extract_symptoms()
   │   └─→ _extract_constantes()
   │
   ├─→ _smart_next_step()
   │   └─→ Détermine étape suivante
   │
   └─→ _smart_question(step)
       └─→ Génère question adaptée
        ↓
5. Répéter 3-4 jusqu'à complétude
        ↓
6. User clique "Prédire"
        ↓
7. Chatbot.get_summary()
        ↓
8. MLTriagePredictor.predict(summary)
   ├─→ _prep_features()
   ├─→ model.predict()
   ├─→ _red_flags()
   ├─→ _rag_enrich()
   └─→ _justify()
        ↓
9. Affichage résultat
        ↓
10. (Optionnel) Export rapport
```

### Workflow Génération

```
1. User entre pathologie (ou vide)
        ↓
2. SimulationWorkflow.run_simulation(pathology)
        ↓
3. PatientGenerator.generate_from_description(pathology)
   ├─→ LLM génère profil patient
   │   ├─→ Identité (nom, âge, sexe)
   │   ├─→ Symptômes cohérents
   │   └─→ Constantes adaptées
   │
   └─→ Patient object créé
        ↓
4. PatientSimulator.get_initial_complaint()
   └─→ Patient exprime plainte
        ↓
5. NurseAgent.generate_question()
   └─→ Infirmier pose questions
        ↓
6. PatientSimulator.respond(question)
   └─→ Patient répond
        ↓
7. Répéter 5-6 (max_turns fois)
        ↓
8. ConversationAnalyzer.extract_patient_info()
   └─→ Extraction données conversation
        ↓
9. Export format ML
```

---

##  Stockage & Persistance

### Bases de Données

#### **ChromaDB (Vectorielle)**

**Localisation :** `data/vector_db/chroma.sqlite3`

**Structure :**
```
Collection: triage_medical
├─ Documents: ~2000 chunks
├─ Embeddings: 384 dimensions (float32)
├─ Metadata: {source, title, section, chunk_id}
└─ Index: HNSW (Hierarchical Navigable Small World)
```

**Configuration :**
```python
Settings(
    anonymized_telemetry=False,
    allow_reset=True,
    persist_directory="data/vector_db"
)
```

---

#### **Monitoring (JSON)**

**Localisation :** `app/data/monitoring/*.json`

**Fichiers :**

1. **api_calls.json**
```json
{
  "calls": [
    {
      "timestamp": "ISO-8601",
      "service": "mistral|embeddings",
      "model": "model-name",
      "tokens_input": int,
      "tokens_output": int,
      "cost": float,
      "latency": float,
      "success": bool
    }
  ]
}
```

2. **latencies.json**
```json
{
  "latencies": [
    {
      "timestamp": "ISO-8601",
      "component": "Chatbot|ML|RAG",
      "operation": "message|predict|retrieve",
      "duration": float
    }
  ]
}
```

3. **predictions.json**
```json
{
  "predictions": [
    {
      "timestamp": "ISO-8601",
      "severity": "ROUGE|JAUNE|VERT|GRIS",
      "confidence": float,
      "age": int,
      "sex": "H|F",
      "red_flags": ["..."]
    }
  ]
}
```

---

### Modèles Persistés

#### **Random Forest (Pickle)**

**Localisation :** `src/models/random_forest_simple.pkl`

**Format :** scikit-learn pickle (protocol 5)

**Taille :** ~2.5 MB

**Chargement :**
```python
import joblib
model = joblib.load("random_forest_simple.pkl")
```

---

##  Intelligence Artificielle

### Mistral AI (LLM)

**Modèle :** `mistral-large-latest`

**Spécifications :**
- **Contexte :** 32k tokens
- **Multilingue :** Français natif
- **Latence :** ~1-2s par requête
- **Coût :** ~$0.002/message

**Usage dans le Système :**

1. **Génération Questions** (Chatbot)
   ```python
   Temperature: 0.7
   Max Tokens: 100
   System Prompt: "Tu es un infirmier..."
   ```

2. **Génération Patients** (Simulation)
   ```python
   Temperature: 0.8
   Max Tokens: 600
   System Prompt: "Génère un patient réaliste..."
   ```

3. **Simulation Réponses** (Patient Simulator)
   ```python
   Temperature: 0.7
   Max Tokens: 150
   System Prompt: "Tu es le patient..."
   ```

---

### Random Forest (ML)

**Entraînement :**

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
)

# Entraîner
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    random_state=42
)
clf.fit(X_train, y_train)

# Évaluer
accuracy = clf.score(X_test, y_test)
```

**Métriques Obtenues :**
```
Accuracy:  87.3%
Precision: 85.6%
Recall:    86.2%
F1-Score:  85.9%
```

**Matrice de Confusion :**
```
              GRIS  VERT  JAUNE  ROUGE
Prédiction
    GRIS      120    15      8      2
    VERT       10   180     12      3
    JAUNE       8    14    190     11
    ROUGE       2     3     10    195
```

---

### RAG (Retrieval Augmented Generation)

**Pipeline Complet :**

```python
# 1. Chargement documents
loader = DocumentLoader()
docs = loader.load_from_directory("data/rag_document/")

# 2. Chunking
chunks = loader.chunk_documents(docs, size=800, overlap=150)

# 3. Embeddings
embedder = EmbeddingProvider("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = embedder.embed_batch([c['text'] for c in chunks])

# 4. Indexation
vector_store = VectorStore()
vector_store.add_documents(chunks)

# 5. Retrieval
retriever = RAGRetriever(vector_store)
context = retriever.retrieve_context(
    query="protocole urgence vitale",
    top_k=3
)

# 6. Enrichissement LLM
prompt = f"Contexte: {context}\n\nQuestion: ..."
response = llm.generate(prompt)
```

---

##  Monitoring & Métriques

### KPIs Suivis

1. **Performance**
   - Latence moyenne par composant
   - Throughput (requêtes/min)
   - Taux d'erreur

2. **Qualité**
   - Taux de complétude conversations
   - Confiance moyenne prédictions
   - Distribution gravités

3. **Coûts**
   - Coût total API
   - Coût par prédiction
   - Tendance mensuelle

4. **Usage**
   - Nombre de sessions
   - Conversations par jour
   - Prédictions par jour

---

### Dashboards

**Monitoring.py** affiche :

```
┌─────────────────────────────────────────┐
│  KPI Cards                               │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ Cost │ │ Calls│ │Latenc│ │ Pred │   │
│  └──────┘ └──────┘ └──────┘ └──────┘   │
├─────────────────────────────────────────┤
│  Cost Evolution (Plotly)                │
│  [Line Chart: Cumul cost over time]    │
├─────────────────────────────────────────┤
│  Latency Distribution                   │
│  [Box Plot: By component]               │
├─────────────────────────────────────────┤
│  Predictions Distribution               │
│  [Pie Chart: By severity]               │
└─────────────────────────────────────────┘
```

---

##  Sécurité

### Gestion des Secrets

**Variables Sensibles :**
```env
# .env (GIT IGNORED!)
MISTRAL_API_KEY=sk-...
OPENAI_API_KEY=sk-...  # Si utilisé
```

**Chargement Sécurisé :**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Charge .env
api_key = os.getenv("MISTRAL_API_KEY")
```

---

### Validation des Entrées

**Constantes Vitales :**
```python
VALID_RANGES = {
    "Temperature": (35.0, 42.0),
    "FC": (30, 250),
    "FR": (5, 60),
    "SpO2": (50, 100),
    "TA_systolique": (50, 250),
    "TA_diastolique": (30, 150),
}

def validate_vital(name, value):
    min_val, max_val = VALID_RANGES[name]
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name} hors plage")
```

---

### Anonymisation

**Données Patients :**
```python
# Pas de stockage de vraies données médicales
# Seulement données synthétiques pour ML

# Si données réelles → anonymisation requise
patient.id = hash(patient.nom + patient.prenom)
patient.nom = None
patient.prenom = None
```

---

##  Performance

### Optimisations Implémentées

1. **Caching LLM**
   ```python
   @lru_cache(maxsize=128)
   def get_llm_response(prompt_hash):
       # Cache réponses identiques
   ```

2. **Batch Embeddings**
   ```python
   # Au lieu de 1 par 1
   embeddings = model.encode(texts, batch_size=32)
   ```

3. **Lazy Loading**
   ```python
   # Charger modèles seulement si nécessaire
   if self.use_ml:
       self.model = load_model()
   ```

4. **Index Optimisé (ChromaDB)**
   ```python
   # HNSW index pour similarité rapide
   # O(log n) au lieu de O(n)
   ```

---

### Benchmarks

**Configuration Test :**
- CPU: Intel i7-11th Gen
- RAM: 16 GB
- Python: 3.11
- OS: Ubuntu 22.04

**Résultats :**

| Opération | Temps Moyen | Écart-Type |
|-----------|-------------|------------|
| Chat Message | 1.2s | ±0.3s |
| ML Prediction | 0.05s | ±0.01s |
| RAG Retrieval | 0.3s | ±0.1s |
| Full Workflow | 1.8s | ±0.4s |

---

##  Configuration Avancée

### Variables d'Environnement

```env
# API Keys
MISTRAL_API_KEY=sk-...
OPENAI_API_KEY=sk-...  # Optionnel

# Paths
CHROMA_PERSIST_DIR=data/vector_db
MONITORING_DATA_DIR=app/data/monitoring

# ML
ML_MODEL_PATH=src/models/random_forest_simple.pkl
ML_CONFIDENCE_THRESHOLD=0.6

# RAG
RAG_TOP_K=3
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=150
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Performance
CACHE_SIZE=128
BATCH_SIZE=32
```

---

##  Références

### Technologies Utilisées

- **Streamlit** : https://streamlit.io
- **Mistral AI** : https://mistral.ai
- **ChromaDB** : https://www.trychroma.com
- **scikit-learn** : https://scikit-learn.org
- **Sentence Transformers** : https://www.sbert.net
- **Plotly** : https://plotly.com

---

<div align="center">

** Documentation Technique v2.0**

*Mis à jour le 02/02/2026*

**[⬆ Retour en haut](#️-architecture-technique---système-de-triage-ia)**

</div>
