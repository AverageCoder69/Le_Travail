#!/usr/bin/env python3
"""
Le Travail - Alpha 0.1.0
Script de démarrage principal

Pour lancer l'application:
    python run.py

URLs disponibles:
- Interface principale: http://localhost:5001
- Carte interactive: http://localhost:5001/carte
- API jobs: http://localhost:5001/jobs
- Statistiques: http://localhost:5001/stats
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
    """Lance le scraping initial si jobs.json n'existe pas"""
    jobs_file = os.path.join(os.path.dirname(__file__), 'jobs.json')
    
    if not os.path.exists(jobs_file):
        print("🔍 Première exécution - Scraping des offres d'emploi...")
        try:
            result = subprocess.run([sys.executable, 'scrapper.py'], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print("✅ Scraping initial terminé")
            else:
                print(f"❌ Erreur lors du scraping: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("⏰ Timeout lors du scraping initial")
            return False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    else:
        print("✅ Fichier jobs.json existant trouvé")
    
    return True

def main():
    """Fonction principale"""
    print("🚀 Le Travail - Alpha 0.1.0")
    print("=" * 40)
    
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
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()