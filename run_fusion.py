#!/usr/bin/env python3
"""
Le Travail - Alpha 0.0.1
Interface unifiée Sécurité Sociale + Crédit Agricole

Pour lancer l'application:
    python run_fusion.py

URLs disponibles:
- Interface principale: http://localhost:5003
- Carte interactive: http://localhost:5003/carte  
- API jobs: http://localhost:5003/jobs
- Statistiques: http://localhost:5003/stats
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
    """Lance le scraping initial si jobs_fusion.json n'existe pas"""
    jobs_file = os.path.join(os.path.dirname(__file__), 'jobs_fusion.json')
    
    if not os.path.exists(jobs_file):
        print("🔍 Première exécution - Scraping fusion Sécurité Sociale + Crédit Agricole...")
        print("⏰ Version optimisée: 3-5 minutes (scraping parallèle)...")
        print("📊 Sécurité Sociale: ~1400 offres")
        print("📊 Crédit Agricole: ~2200 offres (70 pages)")
        
        try:
            result = subprocess.run([sys.executable, 'scrapper_fusion_fast.py'], 
                                  capture_output=True, text=True, timeout=900)  # 15 minutes
            if result.returncode == 0:
                print("✅ Scraping fusion terminé")
                print(result.stdout)
            else:
                print(f"❌ Erreur lors du scraping: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("⏰ Timeout lors du scraping initial (15 min)")
            return False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    else:
        print("✅ Fichier jobs_fusion.json existant trouvé")
    
    return True

def main():
    """Fonction principale"""
    print("💼 Le Travail - Interface Unifiée - Alpha 0.0.1")
    print("=" * 60)
    print("🏛️  Sécurité Sociale + 🏦 Crédit Agricole")
    print("=" * 60)
    
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
    print("📍 Interface: http://localhost:5003")
    print("🗺️  Carte: http://localhost:5003/carte")
    print("📊 Stats: http://localhost:5003/stats")
    print("🔄 Actualiser: http://localhost:5003/refresh")
    try:
        from app_fusion import app
        app.run(debug=False, host='0.0.0.0', port=5003)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()