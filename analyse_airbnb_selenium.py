"""
Version améliorée avec Selenium pour analyser les pages Airbnb avec JavaScript
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import time
import re

class AnalyseAirbnbSelenium:
    def __init__(self, url_airbnb, headless=True):
        self.url = url_airbnb
        self.data = {}
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Configure le driver Selenium"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
        except Exception as e:
            print(f"⚠️ Erreur lors de l'initialisation de Chrome: {e}")
            print("💡 Assurez-vous d'avoir ChromeDriver installé")
            print("   Téléchargez-le sur: https://chromedriver.chromium.org/")
    
    def analyser(self):
        """Lance l'analyse complète avec Selenium"""
        if not self.driver:
            print("❌ Driver non initialisé")
            return None
        
        print(f"🔍 Analyse de l'annonce Airbnb avec Selenium...")
        print(f"URL: {self.url}\n")
        
        try:
            # Charger la page
            self.driver.get(self.url)
            time.sleep(3)  # Attendre le chargement JavaScript
            
            # Accepter les cookies si nécessaire
            try:
                cookie_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Accepter') or contains(text(), 'Accept')]")
                cookie_button.click()
                time.sleep(1)
            except:
                pass
            
            # Extraire les données
            self.data = {
                'url': self.url,
                'infos_principales': self.extraire_infos_principales(),
                'description': self.extraire_description(),
                'prix_disponibilite': self.extraire_prix_disponibilite(),
                'qualite': self.extraire_qualite(),
            }
            
            return self.data
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
    
    def extraire_infos_principales(self):
        """Extrait les informations principales"""
        infos = {}
        
        try:
            # Localisation
            location_elements = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'location') or contains(text(), 'Verbier') or contains(text(), 'Zermatt')]")
            if location_elements:
                infos['localisation'] = location_elements[0].text.strip()
            
            # Titre
            title = self.driver.find_element(By.TAG_NAME, "h1")
            if title:
                infos['titre'] = title.text.strip()
            
            # Type de bien, chambres, capacité
            page_text = self.driver.page_source
            
            # Type de bien
            types = ['appartement', 'chalet', 'maison', 'villa', 'studio']
            for t in types:
                if t.lower() in page_text.lower():
                    infos['type_bien'] = t.capitalize()
                    break
            
            # Nombre de chambres
            chambres_match = re.search(r'(\d+)\s*(chambre|bedroom|bed)', page_text, re.I)
            if chambres_match:
                infos['nombre_chambres'] = int(chambres_match.group(1))
            
            # Capacité
            capacite_match = re.search(r'(\d+)\s*(personne|guest|hôte)', page_text, re.I)
            if capacite_match:
                infos['capacite'] = int(capacite_match.group(1))
            
            # Superficie
            superficie_match = re.search(r'(\d+)\s*m[²2]', page_text)
            if superficie_match:
                infos['superficie'] = f"{superficite_match.group(1)} m²"
                
        except Exception as e:
            print(f"⚠️ Erreur extraction infos principales: {e}")
        
        return infos
    
    def extraire_description(self):
        """Extrait la description"""
        description = {}
        
        try:
            # Chercher la section description
            desc_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'description') or contains(@class, 'about')]")
            if desc_elements:
                description['texte'] = ' '.join([elem.text for elem in desc_elements[:3]])
        except Exception as e:
            print(f"⚠️ Erreur extraction description: {e}")
        
        return description
    
    def extraire_prix_disponibilite(self):
        """Extrait les prix et disponibilité"""
        prix_info = {}
        
        try:
            # Prix
            prix_elements = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'price') or contains(text(), '€')]")
            prix_list = []
            for elem in prix_elements:
                text = elem.text
                match = re.search(r'(\d+)', text.replace(' ', ''))
                if match:
                    prix_list.append(int(match.group(1)))
            
            if prix_list:
                prix_info['prix_nuit'] = min(prix_list)
                prix_info['prix_nuit_max'] = max(prix_list)
        except Exception as e:
            print(f"⚠️ Erreur extraction prix: {e}")
        
        return prix_info
    
    def extraire_qualite(self):
        """Extrait les éléments qualitatifs"""
        qualite = {}
        
        try:
            page_text = self.driver.page_source
            
            # Note
            note_match = re.search(r'(\d+[.,]\d+)\s*\/\s*5', page_text)
            if note_match:
                qualite['note'] = float(note_match.group(1).replace(',', '.'))
            
            # Nombre d'avis
            avis_match = re.search(r'(\d+)\s*(avis|review)', page_text, re.I)
            if avis_match:
                qualite['nombre_avis'] = int(avis_match.group(1))
            
            # Équipements
            equipements = []
            equipements_list = ['Jacuzzi', 'cheminée', 'parking', 'Wi-Fi', 'vue', 'terrasse', 'piscine']
            for equip in equipements_list:
                if equip.lower() in page_text.lower():
                    equipements.append(equip)
            
            qualite['equipements'] = list(set(equipements))
            
        except Exception as e:
            print(f"⚠️ Erreur extraction qualité: {e}")
        
        return qualite
    
    def afficher_resultats(self):
        """Affiche les résultats"""
        if not self.data:
            print("❌ Aucune donnée à afficher")
            return
        
        print("=" * 60)
        print("📊 RÉSULTATS DE L'ANALYSE AIRBNB (Selenium)")
        print("=" * 60)
        
        infos = self.data.get('infos_principales', {})
        print(f"\n📍 Localisation: {infos.get('localisation', 'N/A')}")
        print(f"🏠 Type: {infos.get('type_bien', 'N/A')}")
        print(f"🛏️ Chambres: {infos.get('nombre_chambres', 'N/A')}")
        print(f"👥 Capacité: {infos.get('capacite', 'N/A')}")
        print(f"📐 Superficie: {infos.get('superficie', 'N/A')}")
        
        prix = self.data.get('prix_disponibilite', {})
        if prix.get('prix_nuit'):
            print(f"\n💰 Prix: {prix['prix_nuit']} €/nuit")
        
        qualite = self.data.get('qualite', {})
        if qualite.get('note'):
            print(f"\n⭐ Note: {qualite['note']}/5 ({qualite.get('nombre_avis', 0)} avis)")
        if qualite.get('equipements'):
            print(f"🔧 Équipements: {', '.join(qualite['equipements'])}")


# Exemple d'utilisation
if __name__ == "__main__":
    url = "https://www.airbnb.fr/rooms/1551342108913458049"
    
    print("⚠️ Note: Cette version nécessite ChromeDriver installé")
    print("📥 Téléchargez ChromeDriver: https://chromedriver.chromium.org/\n")
    
    analyseur = AnalyseAirbnbSelenium(url, headless=False)
    resultats = analyseur.analyser()
    
    if resultats:
        analyseur.afficher_resultats()

