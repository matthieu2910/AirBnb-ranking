# 🔍 Algorithme d'Analyse Airbnb

Script Python pour analyser une annonce Airbnb et extraire les informations principales.

## 📋 Informations extraites

### 1. Infos principales
- Ville / station / quartier
- Type de bien (appartement, chalet, maison...)
- Nombre de chambres
- Capacité d'accueil (nombre de personnes)
- Superficie (m²)

### 2. Titre et description
- Titre de l'annonce
- Description complète (texte visible)

### 3. Disponibilité et prix
- Prix par nuit (haute saison / basse saison si disponible)
- Calendrier visible (jours réservés ou libres approximatifs)

### 4. Éléments qualitatifs
- Note globale et nombre d'avis
- Équipements clés (Jacuzzi, cheminée, parking, Wi‑Fi, vue...)

## 🚀 Installation

```bash
# Installer les dépendances
pip install -r requirements_analyse.txt
```

## 💻 Utilisation

### Utilisation basique

```python
from analyse_airbnb import AnalyseAirbnb

url = "https://www.airbnb.fr/rooms/1551342108913458049..."

analyseur = AnalyseAirbnb(url)
resultats = analyseur.analyser()

if resultats:
    analyseur.afficher_resultats()
    analyseur.exporter_json('resultats.json')
```

### Exécution directe

```bash
python analyse_airbnb.py
```

Le script analysera l'URL par défaut et affichera les résultats.

## 📊 Format des résultats

Les résultats sont exportés en JSON avec la structure suivante :

```json
{
  "url": "...",
  "id_listing": "1551342108913458049",
  "infos_principales": {
    "localisation": "Verbier, Valais",
    "type_bien": "Chalet",
    "nombre_chambres": 4,
    "capacite": 8,
    "superficie": "120 m²"
  },
  "description": {
    "texte": "..."
  },
  "prix_disponibilite": {
    "prix_nuit": 250,
    "prix_nuit_max": 450
  },
  "qualite": {
    "note": 4.8,
    "nombre_avis": 127,
    "equipements": ["Jacuzzi", "cheminée", "parking", "Wi-Fi"]
  }
}
```

## ⚠️ Limitations

- **Web scraping** : Airbnb peut bloquer les requêtes automatisées
- **JavaScript** : Certaines données nécessitent l'exécution de JavaScript (nécessite Selenium)
- **Calendrier** : Le calendrier complet nécessite l'API Airbnb ou Selenium
- **Prix saisonniers** : L'extraction des prix haute/basse saison nécessite une analyse plus poussée

## 🔧 Améliorations possibles

1. **Utiliser Selenium** pour les pages JavaScript
2. **API Airbnb** (si disponible) pour des données plus fiables
3. **Cache** pour éviter les requêtes répétées
4. **Gestion d'erreurs** améliorée
5. **Support multi-URLs** pour analyser plusieurs annonces

## 📝 Notes

- Le script utilise des headers pour simuler un navigateur
- Certaines informations peuvent nécessiter une connexion authentifiée
- Respectez les conditions d'utilisation d'Airbnb lors du scraping

## 🛠️ Dépendances

- `requests` : Pour les requêtes HTTP
- `beautifulsoup4` : Pour le parsing HTML
- `lxml` : Parser XML/HTML rapide

