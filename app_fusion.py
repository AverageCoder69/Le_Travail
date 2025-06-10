from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
import sys
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    """Page d'accueil avec l'interface des jobs fusionnés"""
    return send_from_directory('.', 'index_fusion.html')

@app.route('/carte')
def carte():
    """Page carte interactive des jobs fusionnés"""
    return send_from_directory('.', 'carte_fusion.html')

@app.route('/jobs')
def get_jobs():
    """API pour récupérer les données des jobs fusionnés"""
    try:
        with open('jobs_fusion.json', 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        return jsonify(jobs)
    except FileNotFoundError:
        return jsonify({"error": "Fichier jobs_fusion.json non trouvé"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Erreur de format JSON"}), 500

@app.route('/refresh')
def refresh_jobs():
    """Endpoint pour relancer le scraping et mettre à jour les jobs"""
    try:
        # Utiliser l'interpréteur Python actuel
        python_path = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), 'scrapper_fusion_fast.py')
        
        print("🔄 Lancement du scraping fusion...")
        result = subprocess.run([
            python_path, 
            script_path
        ], capture_output=True, text=True, timeout=600)  # 10 minutes timeout (version rapide)
        
        if result.returncode == 0:
            return jsonify({"message": "Jobs fusionnés mis à jour avec succès", "output": result.stdout})
        else:
            return jsonify({"error": "Erreur lors du scraping", "details": result.stderr}), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout - Le scraping a pris trop de temps (10 min)"}), 500
    except Exception as e:
        return jsonify({"error": f"Erreur: {str(e)}"}), 500

@app.route('/stats')
def get_stats():
    """API pour obtenir des statistiques sur les jobs"""
    try:
        with open('jobs_fusion.json', 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        # Calculer des statistiques
        total_jobs = len(jobs)
        jobs_with_salary = len([job for job in jobs if job.get('salaire') != 'NA'])
        unique_locations = len(set(job.get('lieu') for job in jobs if job.get('lieu') != 'NA'))
        unique_employers = len(set(job.get('employeur') for job in jobs))
        
        # Répartition par type de contrat
        contracts = {}
        for job in jobs:
            contract = job.get('type_contrat', 'Non précisé')
            contracts[contract] = contracts.get(contract, 0) + 1
        
        # Répartition par source
        sources = {}
        for job in jobs:
            source = job.get('source', 'Inconnue')
            sources[source] = sources.get(source, 0) + 1
        
        # Répartition par secteur
        sectors = {}
        for job in jobs:
            sector = job.get('secteur', 'Non précisé')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        return jsonify({
            "total_jobs": total_jobs,
            "jobs_with_salary": jobs_with_salary,
            "unique_locations": unique_locations,
            "unique_employers": unique_employers,
            "contracts": contracts,
            "sources": sources,
            "sectors": sectors
        })
        
    except FileNotFoundError:
        return jsonify({"error": "Fichier jobs_fusion.json non trouvé"}), 404

if __name__ == '__main__':
    print("💼 Serveur Le Travail - Jobs Fusionnés")
    print("📍 URL: http://localhost:5003")
    print("🔄 Actualiser les jobs: http://localhost:5003/refresh")
    print("📊 Statistiques: http://localhost:5003/stats")
    print("🗺️  Carte: http://localhost:5003/carte")
    print("🛑 Arrêter le serveur: Ctrl+C")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5003)