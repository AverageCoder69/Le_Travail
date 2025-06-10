#!/usr/bin/env python3
"""
Le Travail - Scraper unifié RAPIDE
Fusion optimisée des offres Sécurité Sociale + Crédit Agricole
Utilise le scraping parallèle pour accélérer le processus
"""

import subprocess
import json
import re
import os
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Lock pour l'affichage thread-safe
print_lock = threading.Lock()

def safe_print(message):
    """Print thread-safe"""
    with print_lock:
        print(message)

def scrape_secu_jobs():
    """Scrape jobs from Sécurité Sociale website"""
    safe_print("🔍 Scraping Sécurité Sociale jobs...")
    
    try:
        # Récupérer le HTML avec TOUTES les offres
        result = subprocess.run(['wget', '--no-check-certificate', '--timeout=30', '-O', '-', 'https://www.lasecurecrute.fr/recherche?&nbre=tous'], 
                               capture_output=True, text=True, timeout=45)
        
        if result.returncode != 0:
            safe_print(f"❌ Erreur Sécurité Sociale: {result.stderr}")
            return []
        
        # Parser le HTML
        soup = BeautifulSoup(result.stdout, 'html.parser')
        job_cards = soup.find_all('article', class_='carte-offre')
        
        jobs = []
        for card in job_cards:
            job = {}
            
            # Titre du poste
            title_elem = card.find('h3') or card.find('h2')
            if title_elem:
                job['titre'] = title_elem.get_text(strip=True)
            
            # Employeur
            titles = card.find_all(['h2', 'h3', 'h4'])
            if len(titles) > 1:
                job['employeur'] = titles[1].get_text(strip=True)
            
            # Lien vers l'offre
            link_elem = card.find('a', href=True)
            if link_elem:
                job['lien'] = link_elem['href']
                if not job['lien'].startswith('http'):
                    job['lien'] = 'https://www.lasecurecrute.fr' + job['lien']
            
            # Initialiser les champs
            job['lieu'] = 'NA'
            job['salaire'] = 'NA'
            job['type_contrat'] = 'NA'
            job['date_publication'] = 'NA'
            job['date_limite'] = 'NA'
            job['reference'] = 'NA'
            job['niveau'] = 'NA'
            job['secteur'] = 'Sécurité Sociale'
            job['source'] = 'Sécurité Sociale'
            
            # Informations détaillées (version rapide)
            meta_items = card.find_all('li')
            for meta in meta_items:
                text = meta.get_text(strip=True)
                span = meta.find('span')
                
                if text and span:
                    classes = span.get('class', [])
                    
                    # Localisation
                    if 'ico-localisation' in classes:
                        job['lieu'] = text.replace('Localisation', '').strip()
                    
                    # Salaire
                    elif 'ico-monnaie' in classes:
                        job['salaire'] = text.replace('Rémunération', '').strip()
                    
                    # Type de contrat
                    elif 'ico-fiche' in classes:
                        job['type_contrat'] = text.replace('Type de contrat', '').strip()
                    
                    # Niveau
                    elif 'ico-contrat' in classes:
                        job['niveau'] = text.replace('Niveau', '').strip()
                    
                    # Date de publication
                    elif 'ico-horloge' in classes:
                        job['date_publication'] = text
                    
                    # Date limite
                    elif 'ico-sablier' in classes:
                        job['date_limite'] = text
                    
                    # Référence
                    elif 'ico-ref' in classes:
                        job['reference'] = text.replace('Référence', '').strip()
                
                # Patterns alternatifs plus rapides
                if 'Publié' in text:
                    job['date_publication'] = text
                elif 'Limite de candidature' in text:
                    job['date_limite'] = text
            
            # ID
            if card.get('id'):
                job['id'] = f"secu_{card.get('id')}"
            elif job.get('lien'):
                job['id'] = f"secu_{job['lien'].split('/')[-1]}"
            
            if job.get('titre'):
                jobs.append(job)
        
        safe_print(f"✅ Sécurité Sociale: {len(jobs)} offres trouvées")
        return jobs
        
    except Exception as e:
        safe_print(f"❌ Erreur Sécurité Sociale: {e}")
        return []

def scrape_ca_page(page_num, max_pages):
    """Scrape une page spécifique du Crédit Agricole"""
    try:
        # URL avec pagination
        if page_num == 1:
            url = 'https://groupecreditagricole.jobs/fr/nos-offres/'
        else:
            url = f'https://groupecreditagricole.jobs/fr/nos-offres/page/{page_num}/'
        
        # Récupérer le HTML avec timeout réduit
        result = subprocess.run([
            'wget', '--no-check-certificate', '--timeout=15', '--tries=2', '-O', '-', url
        ], capture_output=True, text=True, timeout=20)
        
        if result.returncode != 0:
            return page_num, []
        
        # Parser le HTML
        soup = BeautifulSoup(result.stdout, 'html.parser')
        job_cards = soup.find_all('article', class_='card offer detail')
        
        if not job_cards:
            return page_num, []
        
        page_jobs = []
        for card in job_cards:
            job = {}
            
            # Titre du poste
            title_link = card.find('a', href=True)
            if title_link:
                job['titre'] = title_link.get_text(strip=True)
                job['lien'] = title_link.get('href', '')
                
                # ID unique
                if job['lien']:
                    job['id'] = f"ca_{job['lien'].split('/')[-2] if job['lien'].endswith('/') else job['lien'].split('/')[-1]}"
            
            # Données depuis les attributs (plus rapide)
            job['secteur'] = card.get('data-gtm-jobcategory', 'NA')
            job['lieu'] = card.get('data-gtm-jobcity', 'NA')
            job['continent'] = card.get('data-gtm-jobcontinent', 'NA')
            job['type_contrat'] = card.get('data-gtm-jobcontract', 'NA')
            job['niveau'] = card.get('data-gtm-joblevel', 'NA')
            job['employeur'] = card.get('data-gtm-jobentity', 'Groupe Crédit Agricole')
            
            # Recherche rapide de dates
            card_text = card.get_text()
            date_match = re.search(r'\d{2}/\d{2}/\d{4}', card_text)
            if date_match:
                job['date_publication'] = date_match.group()
            else:
                job['date_publication'] = 'NA'
            
            # Valeurs par défaut
            job['salaire'] = 'NA'
            job['reference'] = 'NA'
            job['date_limite'] = 'NA'
            job['description'] = 'NA'
            job['source'] = 'Crédit Agricole'
            
            if job.get('titre'):
                page_jobs.append(job)
        
        return page_num, page_jobs
        
    except Exception as e:
        return page_num, []

def scrape_ca_jobs_parallel(max_pages=70, max_workers=10):
    """Scrape jobs du Crédit Agricole en parallèle"""
    safe_print(f"🔍 Scraping Crédit Agricole jobs ({max_pages} pages) avec {max_workers} workers...")
    
    all_jobs = []
    completed_pages = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Soumettre toutes les tâches
        future_to_page = {executor.submit(scrape_ca_page, page, max_pages): page 
                         for page in range(1, max_pages + 1)}
        
        # Traiter les résultats au fur et à mesure
        for future in as_completed(future_to_page):
            page_num, page_jobs = future.result()
            completed_pages += 1
            
            if page_jobs:
                all_jobs.extend(page_jobs)
                if completed_pages % 10 == 0:
                    safe_print(f"📄 Progression: {completed_pages}/{max_pages} pages ({len(all_jobs)} offres)")
            else:
                # Si plusieurs pages consécutives sont vides, on peut arrêter
                if page_num > 60 and len(page_jobs) == 0:
                    # Compter les pages vides récentes
                    empty_count = sum(1 for p in range(max(1, page_num-5), page_num+1) 
                                    if p in [f.result()[0] for f in future_to_page.keys() 
                                           if f.done() and len(f.result()[1]) == 0])
                    if empty_count >= 3:
                        safe_print(f"⚠️  Arrêt anticipé détecté à la page {page_num}")
                        break
    
    safe_print(f"✅ Crédit Agricole: {len(all_jobs)} offres trouvées")
    return all_jobs

def merge_jobs_fast():
    """Fusion rapide des offres des deux sources"""
    safe_print("🔄 Fusion rapide des offres...")
    start_time = time.time()
    
    # Utiliser ThreadPoolExecutor pour scraper en parallèle
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Lancer les deux scrapings en parallèle
        secu_future = executor.submit(scrape_secu_jobs)
        ca_future = executor.submit(scrape_ca_jobs_parallel, 70, 8)  # 8 workers pour CA
        
        # Récupérer les résultats
        secu_jobs = secu_future.result()
        ca_jobs = ca_future.result()
    
    # Fusionner
    all_jobs = secu_jobs + ca_jobs
    
    # Dédoublonner intelligemment - seulement entre sources différentes
    seen = set()
    unique_jobs = []
    
    # D'abord, ajouter tous les jobs CA sans déduplication interne
    ca_jobs = [job for job in all_jobs if job.get('source') == 'Crédit Agricole']
    secu_jobs = [job for job in all_jobs if job.get('source') == 'Sécurité Sociale']
    
    # Ajouter tous les jobs CA
    unique_jobs.extend(ca_jobs)
    ca_keys = set()
    for job in ca_jobs:
        key = f"{job.get('titre', '')[:50]}|{job.get('lieu', '')}"
        ca_keys.add(key)
    
    # Ajouter les jobs Sécu seulement s'ils ne sont pas déjà dans CA
    for job in secu_jobs:
        key = f"{job.get('titre', '')[:50]}|{job.get('lieu', '')}"
        if key not in ca_keys:
            unique_jobs.append(job)
    
    elapsed_time = time.time() - start_time
    
    safe_print(f"📊 Résumé (en {elapsed_time:.1f}s):")
    safe_print(f"   - Sécurité Sociale: {len(secu_jobs)} offres")
    safe_print(f"   - Crédit Agricole: {len(ca_jobs)} offres") 
    safe_print(f"   - Total brut: {len(all_jobs)} offres")
    safe_print(f"   - Total unique: {len(unique_jobs)} offres")
    safe_print(f"   - CA conservées: {len([j for j in unique_jobs if j.get('source') == 'Crédit Agricole'])} (100%)")
    safe_print(f"   - Sécu conservées: {len([j for j in unique_jobs if j.get('source') == 'Sécurité Sociale'])} offres")
    safe_print(f"   - Vitesse: {len(unique_jobs)/elapsed_time:.1f} offres/seconde")
    
    return unique_jobs

if __name__ == "__main__":
    jobs = merge_jobs_fast()
    
    if jobs:
        # Sauvegarder en JSON
        script_dir = os.path.dirname(__file__)
        jobs_file = os.path.join(script_dir, 'jobs_fusion.json')
        
        with open(jobs_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        
        safe_print(f"\n🎉 {len(jobs)} offres fusionnées sauvegardées dans jobs_fusion.json")
        
        # Statistiques par source
        sources = {}
        for job in jobs:
            source = job.get('source', 'Inconnue')
            sources[source] = sources.get(source, 0) + 1
        
        safe_print(f"📈 Répartition par source:")
        for source, count in sources.items():
            safe_print(f"   - {source}: {count} offres")
        
        # Afficher quelques exemples
        safe_print(f"\n--- Exemples d'offres ---")
        for i, job in enumerate(jobs[:3]):
            safe_print(f"\nJob {i+1} ({job.get('source')}):")
            safe_print(f"  Titre: {job.get('titre')}")
            safe_print(f"  Lieu: {job.get('lieu')}")
            safe_print(f"  Contrat: {job.get('type_contrat')}")
            safe_print(f"  Secteur: {job.get('secteur')}")
    else:
        safe_print("❌ Aucun emploi trouvé")