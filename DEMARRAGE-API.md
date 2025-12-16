# 🚀 Guide de Démarrage de l'API d'Analyse

## 📋 Prérequis

1. **Python 3.7+** installé
2. **Pip** installé

## 🔧 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements_api.txt
```

### 2. Démarrer l'API

```bash
python api_analyse.py
```

L'API sera disponible sur : `http://localhost:5000`

## 📡 Endpoints

### POST `/analyse`
Analyse une annonce Airbnb

**Requête :**
```json
{
  "url": "https://www.airbnb.fr/rooms/1551342108913458049"
}
```

**Réponse :**
```json
{
  "status": "success",
  "data": {
    "url": "...",
    "id_listing": "...",
    "infos_principales": {...},
    "description": {...},
    "prix_disponibilite": {...},
    "qualite": {...}
  }
}
```

## 🌐 Utilisation avec le site

1. **Démarrer l'API** :
   ```bash
   python api_analyse.py
   ```

2. **Ouvrir la maquette** :
   - Ouvrez `maquette-airbnb-ranking.html` dans un navigateur
   - Ou servez-la avec un serveur local (voir ci-dessous)

3. **Tester l'analyse** :
   - Entrez une URL Airbnb dans le formulaire
   - Cliquez sur "Analyse gratuite"
   - Vous serez redirigé vers `resultats_analyse.html` avec les résultats

## 🖥️ Servir les fichiers HTML localement

### Option 1 : Python Simple Server
```bash
# Dans le dossier du projet
python -m http.server 8000
```
Puis ouvrez : `http://localhost:8000/maquette-airbnb-ranking.html`

### Option 2 : Serveur Node.js
```bash
npx http-server -p 8000
```

## ⚙️ Configuration

### Changer le port de l'API

Modifiez dans `api_analyse.py` :
```python
app.run(debug=True, port=5000, host='0.0.0.0')
```

### Changer l'URL de l'API dans le frontend

Dans `resultats_analyse.html`, modifiez :
```javascript
const apiUrl = urlParams.get('api') || 'http://localhost:5000/analyse';
```

Ou passez l'URL en paramètre :
```
resultats_analyse.html?url=...&api=http://votre-serveur:5000/analyse
```

## 🔒 Sécurité (Production)

Pour la production, modifiez `api_analyse.py` :

```python
# Désactiver le mode debug
app.run(debug=False, port=5000, host='0.0.0.0')

# Ajouter l'authentification
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == 'secret'

@app.route('/analyse', methods=['POST'])
@auth.login_required
def analyser_airbnb():
    # ...
```

## 📝 Notes

- Le cache est stocké dans le dossier `cache/`
- Les fichiers HTML peuvent être servis depuis n'importe quel serveur web
- L'API doit être accessible depuis le navigateur (CORS activé)

## 🐛 Dépannage

### Erreur "Connection refused"
- Vérifiez que l'API est bien démarrée
- Vérifiez le port (5000 par défaut)

### Erreur CORS
- L'API a déjà CORS activé avec `flask-cors`
- Si problème, vérifiez la configuration CORS

### Erreur "Module not found"
- Installez les dépendances : `pip install -r requirements_api.txt`

