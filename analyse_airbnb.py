"""
Algorithme d'analyse Airbnb
Extrait les informations principales d'une annonce Airbnb
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse, parse_qs
import time

class AnalyseAirbnb:
    def __init__(self, url_airbnb):
        self.url = url_airbnb
        self.data = {}
        self.session = requests.Session()
        # Headers pour simuler un navigateur
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extraire_id_listing(self):
        """Extrait l'ID du listing depuis l'URL"""
        try:
            # Format: /rooms/1551342108913458049
            match = re.search(r'/rooms/(\d+)', self.url)
            if match:
                return match.group(1)
        except:
            pass
        return None
    
    def fetch_page(self):
        """Récupère la page HTML"""
        try:
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Erreur lors de la récupération de la page: {e}")
            return None
    
    def extraire_donnees_json(self, html):
        """Extrait les données JSON embarquées dans la page"""
        data = {}
        
        # Chercher les scripts JSON-LD
        soup = BeautifulSoup(html, 'html.parser')
        
        # Script avec les données structurées
        scripts = soup.find_all('script', type='application/json')
        for script in scripts:
            try:
                content = script.string
                if content and ('listing' in content.lower() or 'room' in content.lower()):
                    json_data = json.loads(content)
                    if isinstance(json_data, dict):
                        data.update(json_data)
            except:
                pass
        
        # Chercher dans les scripts inline
        scripts_inline = soup.find_all('script')
        for script in scripts_inline:
            if script.string:
                # Chercher les patterns JSON courants
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
        """Extrait les informations principales"""
        soup = BeautifulSoup(html, 'html.parser')
        infos = {}
        
        # Ville / Station / Quartier
        location_elements = soup.find_all(['span', 'div', 'h1', 'h2'], 
                                         string=re.compile(r'(Verbier|Zermatt|Crans|Montana|Valais|Sion|Martigny)', re.I))
        if location_elements:
            infos['localisation'] = location_elements[0].get_text(strip=True)
        else:
            # Chercher dans les meta tags
            meta_location = soup.find('meta', property='airbnb:location')
            if meta_location:
                infos['localisation'] = meta_location.get('content', '')
        
        # Titre
        title = soup.find('h1') or soup.find('title')
        if title:
            infos['titre'] = title.get_text(strip=True)
        
        # Type de bien
        type_patterns = [
            r'(appartement|apartment)',
            r'(chalet|chalet)',
            r'(maison|house)',
            r'(villa|villa)',
            r'(studio|studio)',
        ]
        for pattern in type_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                infos['type_bien'] = match.group(1).capitalize()
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
        soup = BeautifulSoup(html, 'html.parser')
        prix_info = {}
        
        # Prix par nuit
        prix_patterns = [
            r'(\d+)\s*€\s*(par|per)\s*(nuit|night)',
            r'(\d+)\s*CHF\s*(par|per)\s*(nuit|night)',
            r'(\d+)\s*€',
        ]
        for pattern in prix_patterns:
            matches = re.findall(pattern, html, re.I)
            if matches:
                prix_list = [int(m[0]) if isinstance(m, tuple) else int(m) for m in matches]
                prix_info['prix_nuit'] = min(prix_list)  # Prix minimum trouvé
                prix_info['prix_nuit_max'] = max(prix_list)  # Prix maximum
                break
        
        # Calendrier - chercher les dates réservées
        # Note: Le calendrier complet nécessite une API ou Selenium
        dates_reservees = re.findall(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', html)
        if dates_reservees:
            prix_info['dates_trouvees'] = dates_reservees[:10]  # Limiter à 10
        
        return prix_info
    
    def analyser_qualite(self, html):
        """Extrait les éléments qualitatifs"""
        soup = BeautifulSoup(html, 'html.parser')
        qualite = {}
        
        # Note globale
        note_patterns = [
            r'(\d+[.,]\d+)\s*(étoile|star|rating)',
            r'rating[:\s]*(\d+[.,]\d+)',
            r'(\d+[.,]\d+)\s*\/\s*5',
        ]
        for pattern in note_patterns:
            match = re.search(pattern, html, re.I)
            if match:
                qualite['note'] = float(match.group(1).replace(',', '.'))
                break
        
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
            'Jacuzzi', 'jacuzzi', 'spa', 'Spa',
            'cheminée', 'fireplace', 'Fireplace',
            'parking', 'Parking', 'garage',
            'Wi-Fi', 'wifi', 'internet', 'Internet',
            'vue', 'view', 'mountain', 'montagne',
            'terrasse', 'terrace', 'balcon', 'balcony',
            'piscine', 'pool', 'swimming',
        ]
        for equip in equipements_list:
            if equip.lower() in html.lower():
                equipements.append(equip)
        
        qualite['equipements'] = list(set(equipements))  # Supprimer les doublons
        
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
            # Chercher dans les meta descriptions
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description['texte'] = meta_desc.get('content', '')
        
        return description
    
    def analyser(self):
        """Lance l'analyse complète"""
        print(f"🔍 Analyse de l'annonce Airbnb...")
        print(f"URL: {self.url}\n")
        
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
            'infos_principales': self.analyser_infos_principales(html, json_data),
            'description': self.analyser_description(html),
            'prix_disponibilite': self.analyser_prix_disponibilite(html),
            'qualite': self.analyser_qualite(html),
        }
        
        return self.data
    
    def afficher_resultats(self):
        """Affiche les résultats de l'analyse"""
        if not self.data:
            print("❌ Aucune donnée à afficher")
            return
        
        print("=" * 60)
        print("📊 RÉSULTATS DE L'ANALYSE AIRBNB")
        print("=" * 60)
        
        # Infos principales
        print("\n📍 INFORMATIONS PRINCIPALES")
        print("-" * 60)
        infos = self.data.get('infos_principales', {})
        print(f"Localisation: {infos.get('localisation', 'Non trouvé')}")
        print(f"Type de bien: {infos.get('type_bien', 'Non trouvé')}")
        print(f"Nombre de chambres: {infos.get('nombre_chambres', 'Non trouvé')}")
        print(f"Capacité: {infos.get('capacite', 'Non trouvé')} personnes")
        print(f"Superficie: {infos.get('superficie', 'Non trouvé')}")
        
        # Description
        print("\n📝 TITRE ET DESCRIPTION")
        print("-" * 60)
        print(f"Titre: {infos.get('titre', 'Non trouvé')}")
        desc = self.data.get('description', {})
        if desc.get('texte'):
            texte = desc['texte'][:200] + "..." if len(desc['texte']) > 200 else desc['texte']
            print(f"Description: {texte}")
        
        # Prix et disponibilité
        print("\n💰 PRIX ET DISPONIBILITÉ")
        print("-" * 60)
        prix = self.data.get('prix_disponibilite', {})
        if prix.get('prix_nuit'):
            print(f"Prix par nuit: {prix['prix_nuit']} €")
            if prix.get('prix_nuit_max') and prix['prix_nuit_max'] != prix['prix_nuit']:
                print(f"Prix max trouvé: {prix['prix_nuit_max']} €")
        else:
            print("Prix: Non trouvé")
        
        # Qualité
        print("\n⭐ ÉLÉMENTS QUALITATIFS")
        print("-" * 60)
        qualite = self.data.get('qualite', {})
        if qualite.get('note'):
            print(f"Note globale: {qualite['note']}/5")
        if qualite.get('nombre_avis'):
            print(f"Nombre d'avis: {qualite['nombre_avis']}")
        if qualite.get('equipements'):
            print(f"Équipements clés: {', '.join(qualite['equipements'])}")
        
        print("\n" + "=" * 60)
    
    def exporter_json(self, filename='analyse_airbnb.json'):
        """Exporte les résultats en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"✅ Résultats exportés dans {filename}")


# Exemple d'utilisation
if __name__ == "__main__":
    url = "https://www.airbnb.fr/rooms/1551342108913458049?viralityEntryPoint=1&unique_share_id=1FFCCBEA-83D8-4889-B7C9-4DD29403595D&slcid=e8509629b48f442da1653d4586751f14&s=76&adults=1&slug=wk139XJU&source_impression_id=p3_1765894325_P3Q7AFIP6vLyfsdM"
    
    analyseur = AnalyseAirbnb(url)
    resultats = analyseur.analyser()
    
    if resultats:
        analyseur.afficher_resultats()
        analyseur.exporter_json()
    else:
        print("❌ Erreur lors de l'analyse")

