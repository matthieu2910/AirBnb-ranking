# 🔍 Vérifier votre repo GitHub

## Comment vérifier votre repo GitHub

### Option 1 : Via GitHub Desktop
1. Ouvrez **GitHub Desktop**
2. Vérifiez le nom du repo dans le menu déroulant en haut
3. Vérifiez l'URL du remote dans **Repository → Repository Settings → Remote**

### Option 2 : Via ligne de commande Git
```bash
# Voir les remotes configurés
git remote -v

# Voir le statut
git status

# Voir les branches
git branch -a
```

### Option 3 : Via le navigateur
1. Allez sur [github.com](https://github.com)
2. Connectez-vous
3. Cherchez votre repo "Airbnb-ranking" ou "airbnb-ranking-valais"

## 📁 Fichiers créés pour Airbnb Ranking

Tous ces fichiers sont prêts à être commités :

### Maquette
- ✅ `maquette-airbnb-ranking.html` - Maquette principale
- ✅ `index.html` - Redirection
- ✅ `resultats_analyse.html` - Page de résultats

### API et Analyse
- ✅ `api_analyse.py` - API Flask
- ✅ `analyse_airbnb_ameliore.py` - Script d'analyse amélioré
- ✅ `analyse_airbnb.py` - Script d'analyse basique
- ✅ `analyse_airbnb_selenium.py` - Version Selenium

### Configuration
- ✅ `netlify-demo.toml` - Config Netlify
- ✅ `.netlifyignore` - Fichiers à exclure
- ✅ `requirements_api.txt` - Dépendances API
- ✅ `requirements_analyse.txt` - Dépendances analyse

### Documentation
- ✅ `README-AIRBNB-RANKING.md` - Documentation principale
- ✅ `README-INTEGRATION.md` - Guide d'intégration
- ✅ `DEMARRAGE-API.md` - Guide API
- ✅ `DEPLOIEMENT-NETLIFY.md` - Guide Netlify
- ✅ `RESUME-INTEGRATION.md` - Résumé
- ✅ `RAPPORT-TEST-ANALYSE.md` - Rapport de test

## 🚀 Si vous voulez créer un nouveau repo

1. **Sur GitHub.com** :
   - Créez un nouveau repo "airbnb-ranking-valais"
   - Ne cochez PAS "Initialize with README"

2. **Localement** :
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Maquette et API d'analyse Airbnb"
   git remote add origin https://github.com/VOTRE_USERNAME/airbnb-ranking-valais.git
   git push -u origin main
   ```

## 📝 Fichiers à inclure dans le repo

### Essentiels
- `maquette-airbnb-ranking.html`
- `resultats_analyse.html`
- `index.html`
- `api_analyse.py`
- `analyse_airbnb_ameliore.py`
- `requirements_api.txt`
- `README-AIRBNB-RANKING.md`

### Optionnels (documentation)
- Tous les fichiers `.md` de documentation
- `netlify-demo.toml`
- `.netlifyignore`

### À exclure (déjà dans .gitignore)
- `node_modules/`
- `.next/`
- `cache/` (peut être créé automatiquement)

