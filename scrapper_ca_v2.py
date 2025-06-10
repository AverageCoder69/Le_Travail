import subprocess
import json
import re
import os
import time
from bs4 import BeautifulSoup

def scrape_ca_jobs(max_pages=70):
    """Scrape jobs from Credit Agricole website"""
    all_jobs = []
    page = 1
    
    print(f"🔍 Scraping Credit Agricole jobs ({max_pages} pages max)...")
    
    while page <= max_pages:
        try:
            # URL avec pagination
            if page == 1:
                url = 'https://groupecreditagricole.jobs/fr/nos-offres/'
            else:
                url = f'https://groupecreditagricole.jobs/fr/nos-offres/page/{page}/'
            
            print(f"📄 Page {page}/{max_pages}")
            
            # Récupérer le HTML
            result = subprocess.run([
                'wget', '--no-check-certificate', '--timeout=20', '-O', '-', url
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"⚠️  Erreur page {page}: {result.stderr}")
                page += 1
                time.sleep(2)
                continue
            
            # Parser le HTML
            soup = BeautifulSoup(result.stdout, 'html.parser')
            
            # Trouver les cartes d'emploi
            job_cards = soup.find_all('article', class_='card offer detail')
            
            if not job_cards:
                print(f"⚠️  Aucune offre trouvée page {page}")
                break
            
            page_jobs = []
            for card in job_cards:
                job = {}
                
                # Titre du poste (dans le lien principal)
                title_link = card.find('a', href=True)
                if title_link:
                    job['titre'] = title_link.get_text(strip=True)
                    job['lien'] = title_link.get('href', '')
                    
                    # ID unique basé sur le lien
                    if job['lien']:
                        job['id'] = job['lien'].split('/')[-2] if job['lien'].endswith('/') else job['lien'].split('/')[-1]
                
                # Extraire les données depuis les attributs data-gtm
                job['secteur'] = card.get('data-gtm-jobcategory', 'NA')
                job['lieu'] = card.get('data-gtm-jobcity', 'NA')
                job['continent'] = card.get('data-gtm-jobcontinent', 'NA')
                job['type_contrat'] = card.get('data-gtm-jobcontract', 'NA')
                job['niveau'] = card.get('data-gtm-joblevel', 'NA')
                job['employeur'] = card.get('data-gtm-jobentity', 'Groupe Crédit Agricole')
                
                # Informations complémentaires dans le contenu
                content_divs = card.find_all('div')
                for div in content_divs:
                    text = div.get_text(strip=True)
                    
                    # Type de contrat (CDI, CDD, etc.)
                    if any(contract in text.upper() for contract in ['CDI', 'CDD', 'STAGE', 'ALTERNANCE', 'FREELANCE']):
                        if job['type_contrat'] == 'NA':
                            job['type_contrat'] = text
                    
                    # Date (format français)
                    date_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
                    if date_match:
                        job['date_publication'] = date_match.group()
                
                # Valeurs par défaut
                for field in ['date_publication', 'salaire', 'reference']:
                    if field not in job:
                        job[field] = 'NA'
                
                # Ajouter seulement si on a un titre
                if job.get('titre'):
                    page_jobs.append(job)
            
            all_jobs.extend(page_jobs)
            print(f"✅ Page {page}: {len(page_jobs)} offres trouvées")
            
            # Pause entre les requêtes
            time.sleep(1.5)
            page += 1
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout page {page}")
            page += 1
        except Exception as e:
            print(f"❌ Erreur page {page}: {e}")
            page += 1
    
    return all_jobs

if __name__ == "__main__":
    jobs = scrape_ca_jobs()  # Toutes les pages par défaut
    
    if jobs:
        # Sauvegarder en JSON
        script_dir = os.path.dirname(__file__)
        jobs_file = os.path.join(script_dir, 'jobs_ca.json')
        
        with open(jobs_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 {len(jobs)} offres Crédit Agricole sauvegardées dans jobs_ca.json")
        
        # Afficher quelques statistiques
        lieux = [job.get('lieu', 'NA') for job in jobs if job.get('lieu') != 'NA']
        contrats = [job.get('type_contrat', 'NA') for job in jobs if job.get('type_contrat') != 'NA']
        secteurs = [job.get('secteur', 'NA') for job in jobs if job.get('secteur') != 'NA']
        
        print(f"📊 Statistiques:")
        print(f"   - Lieux uniques: {len(set(lieux))}")
        print(f"   - Contrats uniques: {len(set(contrats))}")
        print(f"   - Secteurs uniques: {len(set(secteurs))}")
        
        # Afficher les premiers résultats
        for i, job in enumerate(jobs[:2]):
            print(f"\n--- Job {i+1} ---")
            for key, value in job.items():
                print(f"{key}: {value}")
    else:
        print("❌ Aucun emploi trouvé")