#  Guide de Contribution - Triage Urgence IA

<div align="center">

![Contributors](https://img.shields.io/github/contributors/votre-username/triage-urgence?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)
![Code of Conduct](https://img.shields.io/badge/Code%20of-Conduct-blue?style=for-the-badge)

**Merci de contribuer à rendre le triage médical plus intelligent ! 🏥**

</div>

---

## 📋 Table des Matières

1. [ Types de Contributions](#-types-de-contributions)
2. [ Démarrage Rapide](#-démarrage-rapide)
3. [ Guidelines](#-guidelines)
4. [ Workflow de Développement](#-workflow-de-développement)
5. [ Checklist PR](#-checklist-pr)
6. [ Tests](#-tests)
7. [ Documentation](#-documentation)
8. [ Reconnaissance](#-reconnaissance)

---

##  Types de Contributions

Toutes les contributions sont bienvenues ! Voici comment vous pouvez aider :

###  Reporter des Bugs

**Trouvé un bug ?** Créez une **Issue** avec :

-  **Titre clair** : "Bug: Le chatbot ne détecte pas la température"
-  **Description** : Qu'attendiez-vous vs ce qui s'est passé
-  **Étapes** : Comment reproduire le bug
-  **Environnement** : OS, Python version, navigateur
-  **Screenshots** : Si applicable

**Template Issue Bug :**
```markdown
## Description
Le chatbot n'extrait pas la température quand je tape "38.5"

## Étapes pour Reproduire
1. Lancer le chat
2. Taper "38.5" quand demandé
3. La température n'est pas détectée

## Comportement Attendu
Extraction automatique de 38.5°C

## Environnement
- OS: Windows 11
- Python: 3.11.5
- Navigateur: Chrome 120

## Screenshots
[Capture d'écran]
```

---

###  Proposer des Features

**Une idée géniale ?** Créez une **Issue** avec :

-  **Problème** : Quel besoin cette feature résout
-  **Solution** : Votre proposition
-  **Alternatives** : Autres options considérées
-  **Exemples** : Cas d'usage concrets

**Template Issue Feature :**
```markdown
## Problème à Résoudre
Les utilisateurs veulent exporter les rapports en PDF

## Solution Proposée
Ajouter un bouton "Exporter PDF" qui génère un rapport formaté

## Alternatives
- Export Word (.docx)
- Email direct

## Exemples
- Clinique X a besoin de PDF pour archivage
- Hôpital Y veut imprimer les rapports

## Complexité Estimée
Moyenne (2-3 jours)
```

---

###  Améliorer la Documentation

**La doc peut être mieux ?** Vous pouvez :

-  Corriger typos/erreurs
-  Clarifier sections confuses
-  Ajouter exemples
-  Traduire en autres langues
-  Créer tutoriels vidéo

---

###  Design & UX

**Vous êtes designer ?** Aidez sur :

-  Améliorer l'UI
-  Créer des wireframes
-  Optimiser l'UX
-  Accessibilité (a11y)

---

###  Code

**Vous codez ?** Contribuez sur :

-  Corriger bugs
-  Implémenter features
-  Optimiser performance
-  Ajouter tests
-  Refactoring

---

##  Démarrage Rapide

### 1. Fork & Clone

```bash
# 1. Fork le repo sur GitHub (bouton "Fork")

# 2. Clone VOTRE fork
git clone https://github.com/VOTRE-USERNAME/triage-urgence.git
cd triage-urgence

# 3. Ajouter remote upstream
git remote add upstream https://github.com/ORIGINAL-OWNER/triage-urgence.git

# 4. Vérifier remotes
git remote -v
# origin    https://github.com/VOTRE-USERNAME/triage-urgence.git (fetch)
# origin    https://github.com/VOTRE-USERNAME/triage-urgence.git (push)
# upstream  https://github.com/ORIGINAL-OWNER/triage-urgence.git (fetch)
# upstream  https://github.com/ORIGINAL-OWNER/triage-urgence.git (push)
```

---

### 2. Setup Environnement

```bash
# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer dépendances + dev tools
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Si existe

# Installer pre-commit hooks
pre-commit install
```

---

### 3. Créer Branche

```bash
# Sync avec upstream
git fetch upstream
git checkout main
git merge upstream/main

# Créer nouvelle branche
git checkout -b feature/ma-feature
# ou
git checkout -b fix/mon-bug
# ou
git checkout -b docs/amelioration-readme
```

**Convention Nommage Branches :**
- `feature/` - Nouvelle fonctionnalité
- `fix/` - Correction bug
- `docs/` - Documentation
- `refactor/` - Refactoring code
- `test/` - Ajout/modification tests
- `perf/` - Optimisation performance

---

##  Guidelines

### Style de Code (PEP 8)

**Python :**
```python
#  BON
def calculate_severity_score(vitals: Dict[str, float]) -> float:
    """
    Calcule le score de gravité.
    
    Args:
        vitals: Dictionnaire des constantes vitales
        
    Returns:
        Score entre 0 et 1
    """
    if not vitals:
        return 0.0
    
    score = sum(vitals.values()) / len(vitals)
    return round(score, 2)


#  MAUVAIS
def calc(v):
    if not v:return 0.0
    s=sum(v.values())/len(v)
    return round(s,2)
```

**Règles :**
-  4 espaces (pas tabs)
-  Max 88 caractères par ligne
-  Docstrings Google style
-  Type hints partout
-  Noms explicites (snake_case)

---

### Git Commits

**Convention : Conventional Commits**

```bash
# Format
<type>(<scope>): <description>

[optional body]

[optional footer]

# Types
feat:     Nouvelle feature
fix:      Correction bug
docs:     Documentation
style:    Formatage (pas de changement code)
refactor: Refactoring
test:     Ajout tests
perf:     Optimisation
chore:    Maintenance

# Exemples
git commit -m "feat(chat): ajouter extraction température avec virgule"
git commit -m "fix(ml): corriger prédiction quand constantes manquantes"
git commit -m "docs(readme): ajouter section installation Windows"
```

**Bonnes Pratiques :**
-  Commits atomiques (1 changement = 1 commit)
-  Messages en français ou anglais (cohérent)
-  Présent de l'impératif ("ajouter" pas "ajouté")
-  Première ligne < 72 caractères

---

### Documentation Code

**Docstrings (Google Style) :**

```python
def predict_severity(
    patient_data: Dict[str, Any],
    model: RandomForestClassifier,
    confidence_threshold: float = 0.6
) -> Dict[str, Any]:
    """
    Prédit le niveau de gravité d'un patient.
    
    Utilise un modèle Random Forest entraîné sur des cas réels
    pour classifier en 4 niveaux : ROUGE, JAUNE, VERT, GRIS.
    
    Args:
        patient_data: Dictionnaire contenant :
            - age (int): Âge du patient
            - sex (str): Sexe (H/F)
            - vitals (Dict): Constantes vitales
        model: Modèle Random Forest entraîné
        confidence_threshold: Seuil de confiance minimum (default: 0.6)
        
    Returns:
        Dictionnaire avec :
            - severity_level (str): ROUGE, JAUNE, VERT ou GRIS
            - confidence (float): Score de confiance (0-1)
            - probabilities (Dict): Probabilités par niveau
            - red_flags (List[str]): Drapeaux rouges détectés
            
    Raises:
        ValueError: Si patient_data invalide
        ModelNotTrainedError: Si model non entraîné
        
    Example:
        >>> data = {"age": 45, "sex": "H", "vitals": {...}}
        >>> result = predict_severity(data, model)
        >>> print(result["severity_level"])
        'ROUGE'
        
    Note:
        Les constantes vitales doivent être validées avant.
    """
    # Implementation
    pass
```

---

## 🔧 Workflow de Développement

### Étape par Étape

```bash
# 1. Sync avec upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Créer branche
git checkout -b feature/export-pdf

# 3. Coder
# ... faire vos modifications ...

# 4. Tester
pytest tests/
flake8 src/
black src/

# 5. Commit
git add .
git commit -m "feat(export): ajouter export PDF rapports"

# 6. Push vers VOTRE fork
git push origin feature/export-pdf

# 7. Créer Pull Request sur GitHub
# (Voir section suivante)
```

---

### Créer une Pull Request

1. **Allez sur votre fork** sur GitHub
2. **Cliquez** "Compare & pull request"
3. **Remplissez** le template :

```markdown
## Type de Changement
- [ ] Bug fix
- [x] Nouvelle feature
- [ ] Breaking change
- [ ] Documentation

## Description
Ajout de l'export PDF des rapports de triage.

## Motivation
Les cliniques ont besoin de rapports imprimables pour archivage légal.

## Changes
- Ajout classe `PDFExporter` dans `src/export/pdf_exporter.py`
- Ajout bouton "Export PDF" dans `Chat_interactif.py`
- Ajout dépendance `reportlab` dans `requirements.txt`
- Ajout tests dans `tests/test_pdf_export.py`

## Tests
- [x] Tests unitaires ajoutés
- [x] Tests passent localement
- [x] Testé manuellement

## Screenshots
[Capture du bouton Export PDF]
[Exemple de PDF généré]

## Checklist
- [x] Code suit le style PEP 8
- [x] Docstrings ajoutés
- [x] Tests ajoutés
- [x] Documentation mise à jour
```

4. **Cliquez** "Create Pull Request"

---

##  Checklist PR

Avant de soumettre votre PR, vérifiez :

### Code

- [ ] Suit PEP 8 (flake8 passe)
- [ ] Formaté avec Black
- [ ] Type hints ajoutés
- [ ] Pas de code commenté inutile
- [ ] Pas de print() de debug

### Tests

- [ ] Tests unitaires ajoutés
- [ ] Tests passent (`pytest`)
- [ ] Coverage > 80% (si applicable)
- [ ] Testé manuellement

### Documentation

- [ ] Docstrings à jour
- [ ] README mis à jour si besoin
- [ ] CHANGELOG.md mis à jour
- [ ] Commentaires clairs

### Git

- [ ] Commits atomiques
- [ ] Messages clairs
- [ ] Pas de merge conflicts
- [ ] Branche à jour avec main

---

##  Tests

### Lancer les Tests

```bash
# Tous les tests
pytest

# Avec coverage
pytest --cov=src tests/

# Test spécifique
pytest tests/test_chatbot.py

# Verbose
pytest -v

# Stop au premier échec
pytest -x
```

---

### Écrire des Tests

**Structure :**
```python
# tests/test_chatbot.py
import pytest
from src.rag.chatbot import TriageChatbotAPI


class TestChatbot:
    """Tests pour le chatbot de triage."""
    
    @pytest.fixture
    def chatbot(self):
        """Fixture chatbot pour tests."""
        return TriageChatbotAPI(api_key="test-key")
    
    def test_extract_temperature_formats(self, chatbot):
        """Teste extraction température - différents formats."""
        # Arrange
        test_cases = [
            ("37.5", 37.5),
            ("38", 38.0),
            ("39°C", 39.0),
            ("37,5", 37.5),
        ]
        
        # Act & Assert
        for input_msg, expected in test_cases:
            result = chatbot._extract_temperature(input_msg)
            assert result == expected, f"Failed for input: {input_msg}"
    
    def test_chat_flow_complete(self, chatbot):
        """Teste flux complet conversation."""
        # Arrange
        messages = [
            "Jean, 45 ans, homme",
            "mal à la tête",
            "37.5",
            "80",
            "120/80",
            "98",
            "16"
        ]
        
        # Act
        for msg in messages:
            response = chatbot.chat(msg)
            assert response, "Response should not be empty"
        
        # Assert
        assert chatbot.is_ready_for_prediction()
        summary = chatbot.get_summary()
        assert summary["patient_info"]["age"] == 45
```

---

### Coverage

```bash
# Générer rapport coverage
pytest --cov=src --cov-report=html tests/

# Ouvrir rapport
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Objectif :** > 80% coverage

---

##  Documentation

### README.md

-  Mis à jour si feature change l'usage
-  Screenshots ajoutés si UI modifié
-  Exemples de code si nouvelle API

### Docstrings

-  Toutes les fonctions/classes documentées
-  Google style
-  Args, Returns, Raises, Examples

### CHANGELOG.md

Ajoutez votre changement :

```markdown
## [Unreleased]

### Added
- Export PDF des rapports de triage (#123)

### Fixed
- Correction extraction température avec virgule (#124)

### Changed
- Amélioration performance RAG retrieval (#125)
```

---

##  Reconnaissance

### Hall of Fame

Les contributeurs sont listés dans :
- README.md (section Contributors)
- CONTRIBUTORS.md
- GitHub Contributors page

### Badges

Gagnez des badges selon vos contributions :

-  **First PR** : Première PR mergée
-  **Bug Hunter** : 5+ bugs corrigés
-  **Feature Master** : 3+ features ajoutées
-  **Doc Hero** : 10+ PRs documentation
-  **Test Guru** : Coverage > 90%
-  **Core Contributor** : 20+ PRs mergées

---

##  Questions ?

-  **Discord** : [Rejoindre](https://discord.gg/votre-serveur)
-  **Email** : contribute@triage-urgence.io
-  **Issues** : [GitHub](https://github.com/votre-repo/issues)

---

##  Code of Conduct

Nous attendons de tous les contributeurs :

 **Respect** : Soyez respectueux
 **Bienveillance** : Aidez les autres
 **Patience** : Tout le monde apprend
 **Professionnalisme** : Code de qualité

 **Inacceptable** :
- Harcèlement
- Discrimination
- Spam
- Trolling

Lire le [Code of Conduct](./CODE_OF_CONDUCT.md) complet.

---

<div align="center">

**Merci de contribuer ! **

**Ensemble, rendons le triage médical plus intelligent ! **

---

[⬆ Retour en haut](#-guide-de-contribution---triage-urgence-ia)

</div>
