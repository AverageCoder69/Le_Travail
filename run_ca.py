#!/usr/bin/env python3
"""
Crédit Agricole Jobs - Alpha 0.1.0
Script de démarrage principal

Pour lancer l'application:
    python run_ca.py

URLs disponibles:
- Interface principale: http://localhost:5002
- Carte interactive: http://localhost:5002/carte  
- API jobs: http://localhost:5002/jobs
- Statistiques: http://localhost:5002/stats
"""

import os
import sys
import subprocess

def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    try:
        import flask
        import bs4
        print("✅ Dépendances Python OK")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installation requise:")
        print("   pip install flask beautifulsoup4")
        return False
    
    # Vérifier wget
    try:
        subprocess.run(['wget', '--version'], capture_output=True, check=True)
        print("✅ wget OK")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ wget non trouvé")
        print("📦 Installation requise:")
        print("   - macOS: brew install wget")
        print("   - Ubuntu: sudo apt install wget")
        print("   - Windows: https://eternallybored.org/misc/wget/")
        return False
    
    return True

def initial_scrape():
    """Lance le scraping initial si jobs_ca.json n'existe pas"""
    jobs_file = os.path.join(os.path.dirname(__file__), 'jobs_ca.json')
    
    if not os.path.exists(jobs_file):
        print("🔍 Première exécution - Scraping des offres Crédit Agricole...")
        print("⏰ Cela peut prendre plusieurs minutes (320+ offres)...")
        try:
            result = subprocess.run([sys.executable, 'scrapper_ca_v2.py'], 
                                  capture_output=True, text=True, timeout=600)  # 10 minutes
            if result.returncode == 0:
                print("✅ Scraping initial terminé")
                print(result.stdout)
            else:
                print(f"❌ Erreur lors du scraping: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("⏰ Timeout lors du scraping initial (10 min)")
            return False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    else:
        print("✅ Fichier jobs_ca.json existant trouvé")
    
    return True

def main():
    """Fonction principale"""
    print("🏦 Crédit Agricole Jobs - Alpha 0.1.0")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("\n❌ Veuillez installer les dépendances manquantes")
        sys.exit(1)
    
    # Scraping initial si nécessaire
    if not initial_scrape():
        print("\n❌ Impossible de démarrer sans données")
        sys.exit(1)
    
    # Lancer l'application Flask
    print("\n🌐 Démarrage du serveur web...")
    print("📍 Interface: http://localhost:5002")
    print("🗺️  Carte: http://localhost:5002/carte")
    try:
        from app_ca import app
        app.run(debug=False, host='0.0.0.0', port=5002)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()