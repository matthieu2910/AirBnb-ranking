"""
Algorithme d'analyse Airbnb - Version améliorée
Extrait les informations principales d'une annonce Airbnb avec améliorations
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import os
import hashlib
import pickle
import time
from datetime import datetime
from urllib.parse import urlparse

class AnalyseAirbnbAmeliore:
    def __init__(self, url_airbnb, use_cache=True):
        self.url = url_airbnb
        self.data = {}
        self.use_cache = use_cache
        self.session = requests.Session()
        # Headers pour simuler un navigateur
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.airbnb.fr/',
        })
    
    def get_cache_key(self, url):
        """Génère une clé de cache pour l'URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get_cached_page(self, url):
        """Récupère la page depuis le cache si disponible"""
        if not self.use_cache:
            return None
        
        cache_dir = 'cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        cache_key = self.get_cache_key(url)
        cache_file = os.path.join(cache_dir, f"{cache_key}.html")
        
        if os.path.exists(cache_file):
            # Vérifier si le cache est récent (moins de 24h)
            file_time = os.path.getmtime(cache_file)
            if time.time() - file_time < 86400:  # 24 heures
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
        return None
    
    def save_cached_page(self, url, html):
        """Sauvegarde la page dans le cache"""
        if not self.use_cache:
            return
        
        cache_dir = 'cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        cache_key = self.get_cache_key(url)
        cache_file = os.path.join(cache_dir, f"{cache_key}.html")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def extraire_id_listing(self):
        """Extrait l'ID du listing depuis l'URL"""
        try:
            match = re.search(r'/rooms/(\d+)', self.url)
            if match:
                return match.group(1)
        except:
            pass
        return None
    
    def fetch_page(self):
        """Récupère la page HTML avec gestion d'erreurs améliorée"""
        # Vérifier le cache d'abord
        cached = self.get_cached_page(self.url)
        if cached:
            print("📦 Page récupérée depuis le cache")
            return cached
        
        try:
            response = self.session.get(self.url, timeout=15)
            
            if response.status_code == 403:
                return self.handle_blocked()
            elif response.status_code == 404:
                print("❌ Annonce non trouvée (404)")
                return None
            elif response.status_code != 200:
                print(f"⚠️ Code de statut: {response.status_code}")
                return None
            
            response.raise_for_status()
            html = response.text
            
            # Sauvegarder dans le cache
            self.save_cached_page(self.url, html)
            
            return html
            
        except requests.exceptions.Timeout:
            print("⏱️ Timeout - La requête a pris trop de temps")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau: {e}")
            return None
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return None
    
    def handle_blocked(self):
        """Gère le cas où l'accès est bloqué"""
        print("⚠️ Accès bloqué par Airbnb (403)")
        print("💡 Suggestions:")
        print("   - Utilisez la version Selenium")
        print("   - Attendez quelques minutes")
        print("   - Vérifiez votre connexion")
        return None
    
    def extraire_donnees_json(self, html):
        """Extrait les données JSON embarquées dans la page"""
        data = {}
        soup = BeautifulSoup(html, 'html.parser')
        
        # Chercher les scripts JSON-LD
        scripts = soup.find_all('script', type='application/json')
        for script in scripts:
            try:
                content = script.string
                if content:
                    json_data = json.loads(content)
                    if isinstance(json_data, dict):
                        data.update(json_data)
            except:
                pass
        
        # Chercher dans les scripts inline
        scripts_inline = soup.find_all('script')
        for script in scripts_inline:
            if script.string:
                patterns = [
                    r'__NEXT_DATA__\s*=\s*({.+?});',
                    r'data-state="({.+?})"',
                    r'window\.__initialState__\s*=\s*({.+?});',
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, script.string, re.DOTALL)
                    for match in matches:
                        try:
                            json_data = json.loads(match)
                            if isinstance(json_data, dict):
                                data.update(json_data)
                        except:
                            pass
        
        return data
    
    def analyser_infos_principales(self, html, json_data):
        """Extrait les informations principales avec validation"""
        soup = BeautifulSoup(html, 'html.parser')
        infos = {}
        
        # Ville / Station / Quartier
        location_patterns = [
            r'(Verbier|Zermatt|Crans|Montana|Valais|Sion|Martigny|Sierre)',
            r'([A-Z][a-z]+),\s*([A-Z][a-z]+)',
        ]
        for pattern in location_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                infos['localisation'] = match.group(0)
                break
        
        # Titre
        title = soup.find('h1') or soup.find('title')
        if title:
            infos['titre'] = title.get_text(strip=True)
        
        # Type de bien
        type_patterns = [
            (r'(appartement|apartment)', 'Appartement'),
            (r'(chalet)', 'Chalet'),
            (r'(maison|house)', 'Maison'),
            (r'(villa)', 'Villa'),
            (r'(studio)', 'Studio'),
        ]
        for pattern, type_name in type_patterns:
            if re.search(pattern, html, re.I):
                infos['type_bien'] = type_name
                break
        
        # Nombre de chambres
        chambres_patterns = [
            r'(\d+)\s*(chambre|bedroom|bed)',
            r'(\d+)\s*(pièce|room)',
        ]
        for pattern in chambres_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                infos['nombre_chambres'] = int(match.group(1))
                break
        
        # Capacité d'accueil
        capacite_patterns = [
            r'(\d+)\s*(personne|guest|hôte)',
            r'(\d+)\s*(voyageur|traveler)',
            r'(\d+)\s*(hôte|host)',
        ]
        for pattern in capacite_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                infos['capacite'] = int(match.group(1))
                break
        
        # Superficie
        superficie_patterns = [
            r'(\d+)\s*m[²2]',
            r'(\d+)\s*m\s*x\s*(\d+)\s*m',
        ]
        for pattern in superficie_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                if len(match.groups()) == 2:
                    infos['superficie'] = f"{match.group(1)} x {match.group(2)} m²"
                else:
                    infos['superficie'] = f"{match.group(1)} m²"
                break
        
        return infos
    
    def analyser_prix_disponibilite(self, html):
        """Extrait les informations de prix et disponibilité"""
        prix_info = {}
        
        # Prix par nuit - patterns améliorés
        prix_patterns = [
            r'(\d+)\s*€\s*(par|per)\s*(nuit|night)',
            r'(\d+)\s*CHF\s*(par|per)\s*(nuit|night)',
            r'(\d{2,4})\s*€',
            r'(\d{2,4})\s*CHF',
        ]
        prix_list = []
        for pattern in prix_patterns:
            matches = re.findall(pattern, html, re.I)
            for match in matches:
                if isinstance(match, tuple):
                    prix_list.append(int(match[0]))
                else:
                    prix_list.append(int(match))
        
        if prix_list:
            prix_info['prix_nuit'] = min(prix_list)
            prix_info['prix_nuit_max'] = max(prix_list)
            if prix_info['prix_nuit'] == prix_info['prix_nuit_max']:
                del prix_info['prix_nuit_max']
        
        return prix_info
    
    def analyser_qualite(self, html):
        """Extrait les éléments qualitatifs"""
        qualite = {}
        
        # Note globale
        note_patterns = [
            r'(\d+[.,]\d+)\s*(étoile|star|rating)',
            r'rating[:\s]*(\d+[.,]\d+)',
            r'(\d+[.,]\d+)\s*\/\s*5',
            r'(\d+[.,]\d+)\s*out\s*of\s*5',
        ]
        for pattern in note_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                note_str = match.group(1) if match.lastindex >= 1 else match.group(0)
                try:
                    qualite['note'] = float(note_str.replace(',', '.'))
                    if 0 <= qualite['note'] <= 5:
                        break
                    else:
                        qualite.pop('note', None)
                except:
                    pass
        
        # Nombre d'avis
        avis_patterns = [
            r'(\d+)\s*(avis|review|commentaire)',
            r'(\d+)\s*(évaluation|evaluation)',
        ]
        for pattern in avis_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                qualite['nombre_avis'] = int(match.group(1))
                break
        
        # Équipements clés
        equipements = []
        equipements_list = [
            ('Jacuzzi', ['jacuzzi', 'spa', 'hot tub']),
            ('Cheminée', ['cheminée', 'fireplace', 'foyer']),
            ('Parking', ['parking', 'garage', 'stationnement']),
            ('Wi-Fi', ['wifi', 'wi-fi', 'internet', 'wlan']),
            ('Vue', ['vue', 'view', 'panorama', 'panoramic']),
            ('Terrasse', ['terrasse', 'terrace', 'balcon', 'balcony']),
            ('Piscine', ['piscine', 'pool', 'swimming']),
            ('Cuisine équipée', ['cuisine', 'kitchen', 'équipée']),
            ('Lave-linge', ['lave-linge', 'washing machine', 'laundry']),
            ('Chauffage', ['chauffage', 'heating', 'radiateur']),
        ]
        
        html_lower = html.lower()
        for nom, keywords in equipements_list:
            if any(keyword in html_lower for keyword in keywords):
                equipements.append(nom)
        
        qualite['equipements'] = list(set(equipements))
        
        return qualite
    
    def analyser_description(self, html):
        """Extrait la description"""
        soup = BeautifulSoup(html, 'html.parser')
        description = {}
        
        # Description complète
        desc_elements = soup.find_all(['div', 'p'], class_=re.compile(r'description|about|summary', re.I))
        if desc_elements:
            description['texte'] = ' '.join([elem.get_text(strip=True) for elem in desc_elements[:3]])
        else:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description['texte'] = meta_desc.get('content', '')
        
        return description
    
    def valider_donnees(self):
        """Valide la cohérence des données extraites"""
        warnings = []
        infos = self.data.get('infos_principales', {})
        qualite = self.data.get('qualite', {})
        
        # Vérifier que capacité >= nombre de chambres
        if infos.get('capacite') and infos.get('nombre_chambres'):
            if infos['capacite'] < infos['nombre_chambres']:
                warnings.append("⚠️ Attention: Capacité < Nombre de chambres (peut être normal pour studios)")
        
        # Vérifier que la note est entre 0 et 5
        if qualite.get('note'):
            if not 0 <= qualite['note'] <= 5:
                warnings.append("⚠️ Note invalide détectée")
        
        # Vérifier la cohérence des prix
        prix = self.data.get('prix_disponibilite', {})
        if prix.get('prix_nuit'):
            if prix['prix_nuit'] < 20 or prix['prix_nuit'] > 10000:
                warnings.append("⚠️ Prix suspect détecté")
        
        return warnings
    
    def analyser(self):
        """Lance l'analyse complète"""
        print(f"🔍 Analyse de l'annonce Airbnb...")
        print(f"URL: {self.url}\n")
        
        start_time = time.time()
        
        # Récupérer la page
        html = self.fetch_page()
        if not html:
            return None
        
        # Extraire les données JSON
        json_data = self.extraire_donnees_json(html)
        
        # Analyser les différentes sections
        self.data = {
            'url': self.url,
            'id_listing': self.extraire_id_listing(),
            'date_analyse': datetime.now().isoformat(),
            'infos_principales': self.analyser_infos_principales(html, json_data),
            'description': self.analyser_description(html),
            'prix_disponibilite': self.analyser_prix_disponibilite(html),
            'qualite': self.analyser_qualite(html),
        }
        
        # Valider les données
        warnings = self.valider_donnees()
        if warnings:
            self.data['warnings'] = warnings
        
        elapsed_time = time.time() - start_time
        self.data['temps_analyse'] = round(elapsed_time, 2)
        
        return self.data
    
    def exporter_json(self, filename='analyse_airbnb.json'):
        """Exporte les résultats en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"✅ Résultats exportés dans {filename}")
    
    def exporter_html(self, filename='rapport_analyse.html'):
        """Exporte les résultats en HTML formaté"""
        html_template = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'analyse Airbnb</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1B4332;
            border-bottom: 3px solid #1B4332;
            padding-bottom: 10px;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #fafafa;
            border-radius: 5px;
        }}
        .section h2 {{
            color: #1B4332;
            margin-top: 0;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .info-item {{
            padding: 10px;
            background: white;
            border-left: 4px solid #1B4332;
        }}
        .info-label {{
            font-weight: bold;
            color: #666;
            font-size: 0.9em;
        }}
        .info-value {{
            font-size: 1.2em;
            color: #1B4332;
            margin-top: 5px;
        }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .equipements {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}
        .equipement {{
            background: #1B4332;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rapport d'Analyse Airbnb</h1>
        <p><strong>URL:</strong> <a href="{self.data.get('url', '')}">{self.data.get('url', '')}</a></p>
        <p><strong>Date d'analyse:</strong> {self.data.get('date_analyse', '')}</p>
        <p><strong>Temps d'analyse:</strong> {self.data.get('temps_analyse', 0)} secondes</p>
        
        {self._generate_html_sections()}
    </div>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"✅ Rapport HTML exporté dans {filename}")
    
    def _generate_html_sections(self):
        """Génère les sections HTML du rapport"""
        sections = []
        
        # Infos principales
        infos = self.data.get('infos_principales', {})
        sections.append(f"""
        <div class="section">
            <h2>📍 Informations Principales</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Localisation</div>
                    <div class="info-value">{infos.get('localisation', 'Non trouvé')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Type de bien</div>
                    <div class="info-value">{infos.get('type_bien', 'Non trouvé')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Nombre de chambres</div>
                    <div class="info-value">{infos.get('nombre_chambres', 'Non trouvé')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Capacité</div>
                    <div class="info-value">{infos.get('capacite', 'Non trouvé')} personnes</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Superficie</div>
                    <div class="info-value">{infos.get('superficie', 'Non trouvé')}</div>
                </div>
            </div>
        </div>
        """)
        
        # Description
        desc = self.data.get('description', {})
        if desc.get('texte'):
            sections.append(f"""
            <div class="section">
                <h2>📝 Description</h2>
                <p>{desc['texte'][:500]}...</p>
            </div>
            """)
        
        # Prix
        prix = self.data.get('prix_disponibilite', {})
        if prix.get('prix_nuit'):
            sections.append(f"""
            <div class="section">
                <h2>💰 Prix et Disponibilité</h2>
                <div class="info-item">
                    <div class="info-label">Prix par nuit</div>
                    <div class="info-value">{prix['prix_nuit']} €</div>
                </div>
            </div>
            """)
        
        # Qualité
        qualite = self.data.get('qualite', {})
        if qualite:
            equip_html = ''
            if qualite.get('equipements'):
                equip_html = '<div class="equipements">' + ''.join([f'<span class="equipement">{e}</span>' for e in qualite['equipements']]) + '</div>'
            
            sections.append(f"""
            <div class="section">
                <h2>⭐ Éléments Qualitatifs</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Note globale</div>
                        <div class="info-value">{qualite.get('note', 'N/A')}/5</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Nombre d'avis</div>
                        <div class="info-value">{qualite.get('nombre_avis', 'N/A')}</div>
                    </div>
                </div>
                {equip_html}
            </div>
            """)
        
        # Warnings
        if self.data.get('warnings'):
            warnings_html = ''.join([f'<div class="warning">{w}</div>' for w in self.data['warnings']])
            sections.append(f"""
            <div class="section">
                <h2>⚠️ Avertissements</h2>
                {warnings_html}
            </div>
            """)
        
        return ''.join(sections)


# Exemple d'utilisation
if __name__ == "__main__":
    url = "https://www.airbnb.fr/rooms/1551342108913458049"
    
    analyseur = AnalyseAirbnbAmeliore(url, use_cache=True)
    resultats = analyseur.analyser()
    
    if resultats:
        analyseur.exporter_json()
        analyseur.exporter_html()

