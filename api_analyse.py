"""
API Flask pour l'analyse Airbnb
Backend pour le site web
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from analyse_airbnb_ameliore import AnalyseAirbnbAmeliore
import json
import os

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'API Analyse Airbnb - Utilisez /analyse pour analyser une annonce'
    })

@app.route('/analyse', methods=['POST'])
def analyser_airbnb():
    """Endpoint pour analyser une annonce Airbnb"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                'error': 'URL manquante',
                'status': 'error'
            }), 400
        
        # Valider que c'est une URL Airbnb
        if 'airbnb' not in url.lower():
            return jsonify({
                'error': 'URL Airbnb invalide',
                'status': 'error'
            }), 400
        
        # Lancer l'analyse
        analyseur = AnalyseAirbnbAmeliore(url, use_cache=True)
        resultats = analyseur.analyser()
        
        if not resultats:
            return jsonify({
                'error': 'Impossible d\'analyser l\'annonce. Vérifiez l\'URL ou réessayez plus tard.',
                'status': 'error'
            }), 500
        
        return jsonify({
            'status': 'success',
            'data': resultats
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/rapport/<id_listing>')
def rapport_html(id_listing):
    """Génère un rapport HTML pour un listing"""
    # Cette fonction pourrait récupérer un rapport sauvegardé
    return jsonify({
        'message': 'Rapport HTML - Fonctionnalité à implémenter'
    })

if __name__ == '__main__':
    # Créer le dossier cache s'il n'existe pas
    if not os.path.exists('cache'):
        os.makedirs('cache')
    
    print("🚀 Démarrage de l'API Analyse Airbnb...")
    print("📡 API disponible sur http://localhost:5000")
    print("📝 Endpoint: POST /analyse")
    
    app.run(debug=True, port=5000, host='0.0.0.0')

