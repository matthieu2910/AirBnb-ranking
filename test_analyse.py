"""
Script de test pour l'analyse Airbnb
Teste les différentes fonctionnalités du script d'analyse
"""

import sys
import os

def test_imports():
    """Teste si les dépendances sont installées"""
    print("🔍 Test des imports...")
    try:
        import requests
        print("  ✅ requests")
    except ImportError:
        print("  ❌ requests - Installez avec: pip install requests")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  ✅ beautifulsoup4")
    except ImportError:
        print("  ❌ beautifulsoup4 - Installez avec: pip install beautifulsoup4")
        return False
    
    try:
        import lxml
        print("  ✅ lxml")
    except ImportError:
        print("  ⚠️ lxml - Optionnel mais recommandé")
    
    return True

def test_url_format():
    """Teste le format de l'URL"""
    print("\n🔍 Test du format URL...")
    url = "https://www.airbnb.fr/rooms/1551342108913458049"
    
    import re
    match = re.search(r'/rooms/(\d+)', url)
    if match:
        print(f"  ✅ ID extrait: {match.group(1)}")
        return True
    else:
        print("  ❌ Format URL invalide")
        return False

def test_analyse_basique():
    """Teste l'analyse basique (sans requête réseau)"""
    print("\n🔍 Test de l'analyse (simulation)...")
    
    try:
        from analyse_airbnb import AnalyseAirbnb
        
        url = "https://www.airbnb.fr/rooms/1551342108913458049"
        analyseur = AnalyseAirbnb(url)
        
        # Test extraction ID
        id_listing = analyseur.extraire_id_listing()
        if id_listing:
            print(f"  ✅ ID listing extrait: {id_listing}")
        else:
            print("  ❌ Échec extraction ID")
        
        print("  ✅ Classe AnalyseAirbnb initialisée")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_selenium():
    """Teste si Selenium est disponible"""
    print("\n🔍 Test de Selenium...")
    try:
        from selenium import webdriver
        print("  ✅ Selenium installé")
        print("  ⚠️ ChromeDriver requis pour l'utilisation")
        return True
    except ImportError:
        print("  ⚠️ Selenium non installé - Optionnel")
        print("     Installez avec: pip install selenium")
        return False

def main():
    """Lance tous les tests"""
    print("=" * 60)
    print("🧪 TESTS DE L'ALGORITHME D'ANALYSE AIRBNB")
    print("=" * 60)
    
    results = {
        'imports': test_imports(),
        'url_format': test_url_format(),
        'analyse_basique': test_analyse_basique(),
        'selenium': test_selenium(),
    }
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}")
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés !")
        print("   Vous pouvez maintenant exécuter: python analyse_airbnb.py")
    else:
        print("\n⚠️ Certains tests ont échoué")
        print("   Installez les dépendances manquantes")
        print("   Commande: pip install -r requirements_analyse.txt")

if __name__ == "__main__":
    main()

