from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
import sys
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    """Page d'accueil avec l'interface des jobs Crédit Agricole"""
    return send_from_directory('.', 'index_ca.html')

@app.route('/carte')
def carte():
    """Page carte interactive des jobs Crédit Agricole"""
    return send_from_directory('.', 'carte_ca.html')

@app.route('/jobs')
def get_jobs():
    """API pour récupérer les données des jobs Crédit Agricole"""
    try:
        with open('jobs_ca.json', 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        return jsonify(jobs)
    except FileNotFoundError:
        return jsonify({"error": "Fichier jobs_ca.json non trouvé"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Erreur de format JSON"}), 500

@app.route('/refresh')
def refresh_jobs():
    """Endpoint pour relancer le scraping et mettre à jour les jobs"""
    try:
        # Utiliser l'interpréteur Python actuel
        python_path = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), 'scrapper_ca_v2.py')
        
        result = subprocess.run([
            python_path, 
            script_path
        ], capture_output=True, text=True, timeout=300)  # 5 minutes timeout
        
        if result.returncode == 0:
            return jsonify({"message": "Jobs Crédit Agricole mis à jour avec succès", "output": result.stdout})
        else:
            return jsonify({"error": "Erreur lors du scraping", "details": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erreur: {str(e)}"}), 500

@app.route('/stats')
def get_stats():
    """API pour obtenir des statistiques sur les jobs"""
    try:
        with open('jobs_ca.json', 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        # Calculer des statistiques
        total_jobs = len(jobs)
        jobs_with_date = len([job for job in jobs if job.get('date_publication') != 'NA'])
        unique_locations = len(set(job.get('lieu') for job in jobs if job.get('lieu') != 'NA'))
        unique_sectors = len(set(job.get('secteur') for job in jobs if job.get('secteur') != 'NA'))
        
        # Répartition par type de contrat
        contracts = {}
        for job in jobs:
            contract = job.get('type_contrat', 'Non précisé')
            contracts[contract] = contracts.get(contract, 0) + 1
        
        # Répartition par secteur
        sectors = {}
        for job in jobs:
            sector = job.get('secteur', 'Non précisé')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        return jsonify({
            "total_jobs": total_jobs,
            "jobs_with_date": jobs_with_date,
            "unique_locations": unique_locations,
            "unique_sectors": unique_sectors,
            "contracts": contracts,
            "sectors": sectors
        })
        
    except FileNotFoundError:
        return jsonify({"error": "Fichier jobs_ca.json non trouvé"}), 404

if __name__ == '__main__':
    print("🏦 Serveur Crédit Agricole Jobs")
    print("📍 URL: http://localhost:5002")
    print("🔄 Actualiser les jobs: http://localhost:5002/refresh")
    print("📊 Statistiques: http://localhost:5002/stats")
    print("🛑 Arrêter le serveur: Ctrl+C")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5002)