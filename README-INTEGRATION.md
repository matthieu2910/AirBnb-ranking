# 🔗 Intégration Analyse Airbnb dans le Site

## 📁 Fichiers créés

### Backend (API)
- **`api_analyse.py`** - Serveur Flask pour l'analyse
- **`analyse_airbnb_ameliore.py`** - Script d'analyse amélioré
- **`requirements_api.txt`** - Dépendances Python

### Frontend
- **`resultats_analyse.html`** - Page d'affichage des résultats
- **`maquette-airbnb-ranking.html`** - Modifié pour intégrer l'analyse

## 🔄 Flux de fonctionnement

1. **Utilisateur entre une URL** dans le formulaire de la maquette
2. **Redirection** vers `resultats_analyse.html?url=...`
3. **Page de résultats** fait une requête POST à l'API Flask
4. **API analyse** l'annonce Airbnb
5. **Résultats affichés** sur la page HTML

## 🚀 Démarrage rapide

### 1. Installer les dépendances
```bash
pip install -r requirements_api.txt
```

### 2. Démarrer l'API
```bash
python api_analyse.py
```

### 3. Ouvrir la maquette
- Ouvrez `maquette-airbnb-ranking.html` dans un navigateur
- Ou servez avec : `python -m http.server 8000`

### 4. Tester
- Entrez une URL Airbnb
- Cliquez sur "Analyse gratuite"
- Consultez les résultats

## 📊 Améliorations implémentées

✅ **Cache** - Évite les requêtes répétées  
✅ **Gestion d'erreurs** - Messages clairs  
✅ **Validation des données** - Détecte les incohérences  
✅ **Export HTML** - Rapport formaté  
✅ **Export JSON** - Données structurées  
✅ **Temps d'analyse** - Mesure de performance  

## 🔧 Configuration

### Modifier l'URL de l'API

Dans `resultats_analyse.html`, ligne ~50 :
```javascript
const apiUrl = urlParams.get('api') || 'http://localhost:5000/analyse';
```

### Désactiver le cache

Dans `analyse_airbnb_ameliore.py` :
```python
analyseur = AnalyseAirbnbAmeliore(url, use_cache=False)
```

## 📝 Structure des données

Les résultats contiennent :
- `infos_principales` : localisation, type, chambres, capacité, superficie
- `description` : texte de l'annonce
- `prix_disponibilite` : prix par nuit
- `qualite` : note, avis, équipements
- `warnings` : avertissements de validation

## 🌐 Déploiement

### Netlify (Frontend)
- Déployez les fichiers HTML sur Netlify
- L'API doit être hébergée séparément

### Heroku / Railway (Backend)
- Déployez `api_analyse.py` sur Heroku ou Railway
- Modifiez l'URL de l'API dans `resultats_analyse.html`

## ⚠️ Limitations

- L'API doit être accessible depuis le navigateur
- Airbnb peut bloquer les requêtes automatisées
- Utilisez Selenium pour les pages JavaScript complexes

