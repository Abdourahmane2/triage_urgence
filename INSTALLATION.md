#  Guide d'Installation - Triage Urgence IA

<div align="center">

![Installation](https://img.shields.io/badge/Guide-Installation-blue?style=for-the-badge)
![Difficulté](https://img.shields.io/badge/Difficulté-Facile-green?style=for-the-badge)
![Temps](https://img.shields.io/badge/Temps-10_minutes-orange?style=for-the-badge)

**Guide complet pour installer le système sur votre machine**

</div>

---

##  Table des Matières

1. [ Prérequis](#️-prérequis)
2. [ Installation Rapide](#-installation-rapide)
3. [ Installation Détaillée](#-installation-détaillée)
4. [ Configuration API](#-configuration-api)
5. [ Vérification](#-vérification)
6. [ Troubleshooting](#-troubleshooting)
7. [ Différentes Plateformes](#️-différentes-plateformes)

---

## ⚙️ Prérequis

### Système

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| **OS** | Windows 10, macOS 10.15, Ubuntu 20.04 | Windows 11, macOS 13+, Ubuntu 22.04 |
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4 GB | 8+ GB |
| **Stockage** | 2 GB libre | 5+ GB libre |
| **Internet** | Connexion stable | Haut débit |

### Logiciels Requis

#### 1. Python 3.11+

**Vérifier la version :**
```bash
python --version
# ou
python3 --version
```

**Si absent, installer :**

<details>
<summary><b>Windows</b></summary>

1. Télécharger : [python.org/downloads](https://www.python.org/downloads/)
2. Lancer l'installateur
3.  Cocher **"Add Python to PATH"**
4. Cliquer **"Install Now"**

</details>

<details>
<summary><b>macOS</b></summary>

```bash
# Via Homebrew (recommandé)
brew install python@3.11

# Ou télécharger depuis python.org
```

</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

</details>

#### 2. pip (Gestionnaire de Paquets)

**Vérifier :**
```bash
pip --version
```

**Installer/Mettre à jour :**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### 3. Git (Optionnel mais recommandé)

```bash
git --version
```

Si absent : [git-scm.com/downloads](https://git-scm.com/downloads)

---

##  Installation Rapide

### Pour les Pressés (5 minutes)

```bash
# 1. Cloner
git clone https://github.com/votre-username/triage-urgence.git
cd triage-urgence

# 2. Installer
pip install -r requirements.txt

# 3. Configurer
cp .env.example .env
# Éditez .env et ajoutez MISTRAL_API_KEY

# 4. Lancer
streamlit run app/Home.py
```

 **C'est tout !** L'app tourne sur `http://localhost:8501`

---

##  Installation Détaillée

### Étape 1 : Récupérer le Code

#### Option A : Avec Git (Recommandé)

```bash
# Cloner le repository
git clone https://github.com/votre-username/triage-urgence.git

# Entrer dans le dossier
cd triage-urgence

# Vérifier la structure
ls -la
```

#### Option B : Téléchargement ZIP

1. Allez sur [github.com/votre-username/triage-urgence](https://github.com/votre-username/triage-urgence)
2. Cliquez **Code** → **Download ZIP**
3. Décompressez le fichier
4. Ouvrez un terminal dans le dossier

---

### Étape 2 : Environnement Virtuel (Fortement Recommandé)

**Pourquoi ?** Isoler les dépendances du projet

#### Créer l'environnement

```bash
# Créer
python -m venv venv

# Ou avec python3
python3 -m venv venv
```

#### Activer l'environnement

<details>
<summary><b>Windows (CMD)</b></summary>

```cmd
venv\Scripts\activate.bat
```

</details>

<details>
<summary><b>Windows (PowerShell)</b></summary>

```powershell
venv\Scripts\Activate.ps1

# Si erreur de politique d'exécution :
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

</details>

<details>
<summary><b>macOS / Linux</b></summary>

```bash
source venv/bin/activate
```

</details>

**Vérifier activation :**
```bash
# Le prompt doit afficher (venv)
(venv) user@machine:~/triage-urgence$
```

---

### Étape 3 : Installer les Dépendances

#### Installation Standard

```bash
pip install -r requirements.txt
```

**Temps estimé :** 3-5 minutes

**Progression :**
```
Collecting streamlit>=1.35.0
Downloading streamlit-1.35.0-py3-none-any.whl (8.3 MB)
...
Successfully installed streamlit-1.35.0 pandas-2.2.0 ...
```

#### Installation avec Upgrades

```bash
# Si besoin de dernières versions
pip install --upgrade -r requirements.txt
```

#### Vérifier l'installation

```bash
pip list

# Devrait afficher :
# streamlit        1.35.0
# mistralai        0.1.6
# chromadb         0.4.22
# scikit-learn     1.5.0
# ...
```

---

### Étape 4 : Configuration

#### A. Fichier .env

```bash
# Copier le template
cp .env.example .env

# Linux/Mac
nano .env

# Windows
notepad .env
```

#### B. Obtenir Clé API Mistral

**Étapes détaillées :**

1. **Créer un compte**
   - Allez sur [console.mistral.ai](https://console.mistral.ai)
   - Cliquez **"Sign up"**
   - Vérifiez votre email

2. **Générer une clé**
   - Allez dans **API Keys**
   - Cliquez **"Create new key"**
   - Nommez-la : `triage-urgence`
   - Copiez la clé (commence par `sk-...`)

3. **Ajouter dans .env**
   ```env
   MISTRAL_API_KEY=sk-votre-cle-ici
   ```

 **Important :** La clé est secrète ! Ne la partagez jamais.

#### C. Configuration Optionnelle

```env
# Paths (par défaut OK)
CHROMA_PERSIST_DIR=data/vector_db
MONITORING_DATA_DIR=app/data/monitoring

# ML
ML_MODEL_PATH=src/models/random_forest_simple.pkl
ML_CONFIDENCE_THRESHOLD=0.6

# RAG
RAG_TOP_K=3
RAG_CHUNK_SIZE=800
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Logging
LOG_LEVEL=INFO
```

---

### Étape 5 : Initialisation (Optionnel - RAG)

#### A. Charger la Base Vectorielle

```bash
python init_rag_db.py
```

**Output attendu :**
```
 Chargement modèle embeddings: paraphrase-multilingual-MiniLM-L12-v2
 Modèle chargé
 Chargement documents depuis data/rag_document/
 2143 chunks chargés
 Indexation dans ChromaDB...
 Base vectorielle prête !
```

**Temps estimé :** 2-3 minutes

#### B. Tester le RAG

```bash
python demo_rag.py
```

**Test interactif :**
```
 Entrez une question (ou 'quit') :
> Quels sont les critères pour le niveau ROUGE ?

 Résultats :
[Source 1: protocoles_action.md]
Niveau ROUGE - Urgence Vitale Immédiate
- Détresse vitale ou risque de défaillance d'organe
- Prise en charge < 5 minutes
...
```

---

##  Configuration API

### Mistral AI (Requis)

**Pricing :**
- **Free Tier :** 5€ de crédit gratuit
- **Tarification :** ~0.002€ par message
- **Pour 100 patients :** ~0.40€

**Limites Free Tier :**
- Requêtes : 100/min
- Tokens : 200k/mois

### OpenAI (Optionnel)

Si vous voulez tester avec GPT :

```env
OPENAI_API_KEY=sk-...
```

Modifiez `src/llm/llm_factory.py` :
```python
# Changer provider
provider = "openai"  # au lieu de "mistral"
```

---

##  Vérification

### Test 1 : Dépendances

```bash
python -c "import streamlit; import mistralai; import chromadb; print(' OK')"
```

### Test 2 : Modèle ML

```bash
python -c "import joblib; m = joblib.load('src/models/random_forest_simple.pkl'); print(' Modèle chargé')"
```

### Test 3 : API Mistral

```bash
python -c "
from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')
client = Mistral(api_key=api_key)

response = client.chat.complete(
    model='mistral-large-latest',
    messages=[{'role': 'user', 'content': 'Test'}]
)
print(' API fonctionne')
"
```

### Test 4 : Lancer l'App

```bash
streamlit run app/Home.py
```

**Vérifier :**
-  Page s'ouvre sur `http://localhost:8501`
-  Pas d'erreurs dans le terminal
-  Modules visibles dans sidebar

---

##  Troubleshooting

### Problème : "Command not found: python"

**Solution :**
```bash
# Essayez python3
python3 --version

# Ou créez un alias
alias python=python3
```

---

### Problème : "ModuleNotFoundError"

**Solution :**
```bash
# Vérifiez que venv est activé
which python
# Devrait pointer vers venv/bin/python

# Réinstaller
pip install -r requirements.txt
```

---

### Problème : "MISTRAL_API_KEY not found"

**Solution :**
```bash
# Vérifiez .env existe
ls -la .env

# Vérifiez contenu
cat .env

# Devrait contenir :
MISTRAL_API_KEY=sk-...

# Pas de guillemets, pas d'espaces
```

---

### Problème : "Address already in use (port 8501)"

**Solution :**
```bash
# Option 1 : Changer le port
streamlit run app/Home.py --server.port 8080

# Option 2 : Tuer le processus
# Linux/Mac
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

### Problème : "ChromaDB error"

**Solution :**
```bash
# Réinitialiser la base
rm -rf data/vector_db/*

# Recréer
python init_rag_db.py
```

---

### Problème : Erreurs sklearn version

**Solution :**
```bash
# Mettre à jour sklearn
pip install --upgrade scikit-learn

# Réentraîner le modèle si nécessaire
python src/ml/train_model.py
```

---

##  Différentes Plateformes

### Windows

**Particularités :**
```cmd
# Activer venv
venv\Scripts\activate.bat

# Variables d'environnement
set MISTRAL_API_KEY=sk-...

# Paths avec backslash
data\vector_db
```

**Éditeur recommandé :**
- Visual Studio Code
- PyCharm
- Notepad++

---

### macOS

**Particularités :**
```bash
# Installer Python via Homebrew
brew install python@3.11

# Permissions
chmod +x scripts/*.sh

# Activer venv
source venv/bin/activate
```

**Homebrew :**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### Linux (Ubuntu/Debian)

**Installation système :**
```bash
# Mettre à jour
sudo apt update && sudo apt upgrade

# Python + pip
sudo apt install python3.11 python3.11-venv python3-pip

# Git
sudo apt install git

# Dépendances système (pour certains packages)
sudo apt install build-essential python3-dev
```

---

##  Installation Alternative (Docker)

**Coming soon...**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app/Home.py"]
```

```bash
# Build
docker build -t triage-urgence .

# Run
docker run -p 8501:8501 triage-urgence
```

---

##  Checklist Finale

Avant de commencer à utiliser :

- [ ] Python 3.11+ installé
- [ ] Git installé
- [ ] Code récupéré
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées
- [ ] Fichier .env configuré
- [ ] Clé API Mistral ajoutée
- [ ] Tests passés
- [ ] App lance sans erreur

** Tout est coché ? Vous êtes prêt ! **

---

##  Support Installation

Problèmes persistants ?

1. **Vérifiez** les [Issues GitHub](https://github.com/votre-repo/issues)
2. **Créez** une nouvelle issue avec :
   - OS et version
   - Python version
   - Message d'erreur complet
   - Étapes pour reproduire
3. **Rejoignez** notre [Discord](https://discord.gg/votre-serveur)

---

<div align="center">

**[⬆ Retour en haut](#-guide-dinstallation---triage-urgence-ia)**

**[ Guide Utilisation](./USER_GUIDE.md)** • **[ Architecture](./ARCHITECTURE.md)** • **[ Contribuer](./CONTRIBUTING.md)**

</div>
