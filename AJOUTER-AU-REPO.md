# 📤 Ajouter les nouveaux fichiers au repo GitHub

## 🔗 Votre repo
**URL** : https://github.com/matthieu2910/AirBnb-ranking.git

## 📋 Fichiers à ajouter

### ✅ Déjà dans le repo
- `maquette-airbnb-ranking.html`
- `index.html`
- `netlify-demo.toml`
- `ouvrir-maquette.bat`
- `README-AIRBNB-RANKING.md`

### 🆕 Nouveaux fichiers à ajouter

#### API et Analyse
- `api_analyse.py` ⭐ **Important**
- `analyse_airbnb_ameliore.py` ⭐ **Important**
- `analyse_airbnb.py`
- `analyse_airbnb_selenium.py`
- `requirements_api.txt` ⭐ **Important**
- `requirements_analyse.txt`

#### Pages Web
- `resultats_analyse.html` ⭐ **Important**

#### Configuration
- `.netlifyignore`

#### Documentation
- `README-INTEGRATION.md` ⭐ **Important**
- `DEMARRAGE-API.md` ⭐ **Important**
- `RESUME-INTEGRATION.md`
- `RAPPORT-TEST-ANALYSE.md`
- `README-ANALYSE-AIRBNB.md`
- `QUICK-START-NETLIFY.md`
- `DEPLOIEMENT-NETLIFY.md`

#### Tests
- `test_analyse.py`

## 🚀 Méthode 1 : GitHub Desktop (Recommandé)

1. **Ouvrez GitHub Desktop**
2. **Sélectionnez le repo** "AirBnb-ranking"
3. **Dans l'onglet "Changes"**, vous verrez tous les nouveaux fichiers
4. **Cochez tous les fichiers** listés ci-dessus
5. **Message de commit** :
   ```
   Add API d'analyse Airbnb et intégration complète
   
   - API Flask pour l'analyse d'annonces Airbnb
   - Scripts d'analyse améliorés avec cache et validation
   - Page de résultats HTML
   - Documentation complète
   ```
6. **Cliquez sur "Commit to main"**
7. **Cliquez sur "Push origin"**

## 🚀 Méthode 2 : Ligne de commande Git

```bash
# Ajouter tous les nouveaux fichiers
git add api_analyse.py
git add analyse_airbnb_ameliore.py
git add analyse_airbnb.py
git add analyse_airbnb_selenium.py
git add requirements_api.txt
git add requirements_analyse.txt
git add resultats_analyse.html
git add .netlifyignore
git add README-INTEGRATION.md
git add DEMARRAGE-API.md
git add RESUME-INTEGRATION.md
git add RAPPORT-TEST-ANALYSE.md
git add README-ANALYSE-AIRBNB.md
git add QUICK-START-NETLIFY.md
git add DEPLOIEMENT-NETLIFY.md
git add test_analyse.py

# Vérifier
git status

# Committer
git commit -m "Add API d'analyse Airbnb et intégration complète

- API Flask pour l'analyse d'annonces Airbnb
- Scripts d'analyse améliorés avec cache et validation
- Page de résultats HTML
- Documentation complète"

# Pousser
git push origin main
```

## 🚀 Méthode 3 : Interface Web GitHub

1. Allez sur https://github.com/matthieu2910/AirBnb-ranking
2. Cliquez sur **"Add file"** → **"Upload files"**
3. Glissez-déposez tous les nouveaux fichiers
4. Message de commit : `Add API d'analyse Airbnb et intégration complète`
5. Cliquez sur **"Commit changes"**

## 📝 Structure finale du repo

```
AirBnb-ranking/
├── maquette-airbnb-ranking.html    ✅ Déjà présent
├── index.html                       ✅ Déjà présent
├── resultats_analyse.html          🆕 À ajouter
├── api_analyse.py                  🆕 À ajouter
├── analyse_airbnb_ameliore.py      🆕 À ajouter
├── analyse_airbnb.py               🆕 À ajouter
├── analyse_airbnb_selenium.py      🆕 À ajouter
├── requirements_api.txt            🆕 À ajouter
├── requirements_analyse.txt         🆕 À ajouter
├── netlify-demo.toml               ✅ Déjà présent
├── .netlifyignore                  🆕 À ajouter
├── ouvrir-maquette.bat             ✅ Déjà présent
├── README-AIRBNB-RANKING.md        ✅ Déjà présent
├── README-INTEGRATION.md           🆕 À ajouter
├── DEMARRAGE-API.md                🆕 À ajouter
├── RESUME-INTEGRATION.md           🆕 À ajouter
├── RAPPORT-TEST-ANALYSE.md         🆕 À ajouter
├── README-ANALYSE-AIRBNB.md        🆕 À ajouter
├── QUICK-START-NETLIFY.md          🆕 À ajouter
├── DEPLOIEMENT-NETLIFY.md          🆕 À ajouter
└── test_analyse.py                 🆕 À ajouter
```

## ⚠️ Fichiers à NE PAS ajouter

Ces fichiers sont locaux et ne doivent pas être commités :
- `cache/` (créé automatiquement)
- Fichiers temporaires
- Fichiers de configuration locale

## ✅ Après avoir ajouté les fichiers

Votre repo contiendra :
- ✅ Maquette HTML complète
- ✅ API Flask fonctionnelle
- ✅ Scripts d'analyse
- ✅ Page de résultats
- ✅ Documentation complète
- ✅ Configuration Netlify

## 🔗 Vérification

Après le push, vérifiez sur :
https://github.com/matthieu2910/AirBnb-ranking

Tous les nouveaux fichiers devraient apparaître !

