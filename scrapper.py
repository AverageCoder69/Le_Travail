import subprocess
import json
import re
from bs4 import BeautifulSoup

def scrape_jobs():
    try:
        # Récupérer le HTML avec TOUTES les offres
        result = subprocess.run(['wget', '--no-check-certificate', '-O', '-', 'https://www.lasecurecrute.fr/recherche?&nbre=tous'], 
                               capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return []
        
        # Parser le HTML
        soup = BeautifulSoup(result.stdout, 'html.parser')
        
        # Trouver les cartes d'emploi
        job_cards = soup.find_all('article', class_='carte-offre')
        
        jobs = []
        for card in job_cards:
            job = {}
            
            # Titre du poste (premier h3 ou h2)
            title_elem = card.find('h3') or card.find('h2')
            if title_elem:
                job['titre'] = title_elem.get_text(strip=True)
            
            # Employeur (deuxième titre)
            titles = card.find_all(['h2', 'h3', 'h4'])
            if len(titles) > 1:
                job['employeur'] = titles[1].get_text(strip=True)
            
            # Lien vers l'offre
            link_elem = card.find('a', href=True)
            if link_elem:
                job['lien'] = link_elem['href']
                if not job['lien'].startswith('http'):
                    job['lien'] = 'https://www.lasecurecrute.fr' + job['lien']
            
            # Initialiser les champs avec "NA"
            job['lieu'] = 'NA'
            job['salaire'] = 'NA'
            job['type_contrat'] = 'NA'
            job['date_publication'] = 'NA'
            job['date_limite'] = 'NA'
            job['reference'] = 'NA'
            job['niveau'] = 'NA'
            
            # Informations détaillées (meta)
            meta_items = card.find_all('li')
            for meta in meta_items:
                text = meta.get_text(strip=True)
                span = meta.find('span')
                
                if text:
                    # Localisation
                    if span and 'ico-localisation' in span.get('class', []):
                        # Retirer "Localisation" du début du texte
                        job['lieu'] = text.replace('Localisation', '').strip()
                    
                    # Salaire
                    elif span and 'ico-monnaie' in span.get('class', []):
                        job['salaire'] = text.replace('Rémunération', '').strip()
                    
                    # Type de contrat
                    elif span and 'ico-fiche' in span.get('class', []):
                        job['type_contrat'] = text.replace('Type de contrat', '').strip()
                    
                    # Niveau
                    elif span and 'ico-contrat' in span.get('class', []):
                        job['niveau'] = text.replace('Niveau', '').strip()
                    
                    # Date de publication
                    elif span and 'ico-horloge' in span.get('class', []):
                        job['date_publication'] = text
                    elif 'Publié' in text:
                        job['date_publication'] = text
                    
                    # Date limite de candidature
                    elif span and 'ico-sablier' in span.get('class', []):
                        job['date_limite'] = text
                    elif 'Limite de candidature' in text:
                        job['date_limite'] = text
                    
                    # Référence
                    elif span and 'ico-ref' in span.get('class', []):
                        job['reference'] = text.replace('Référence', '').strip()
            
            # Description courte
            desc_elem = card.find('p')
            if desc_elem:
                job['description'] = desc_elem.get_text(strip=True)[:300]
            
            # ID de l'offre
            if card.get('id'):
                job['id'] = card.get('id')
            
            if job:  # Si on a trouvé au moins une info
                jobs.append(job)
        
        return jobs
        
    except subprocess.TimeoutExpired:
        print("Timeout: Request took too long")
        return []
    except FileNotFoundError:
        print("Error: wget not found. Install with: brew install wget")
        return []
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []

if __name__ == "__main__":
    jobs = scrape_jobs()
    
    if jobs:
        # Sauvegarder en JSON
        with open('/Volumes/JeremyExternal/jeremyext/Documents/Le_Travail/jobs.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        
        print(f"Trouvé {len(jobs)} offres d'emploi sauvegardées dans jobs.json")
        
        # Afficher les premiers résultats
        for i, job in enumerate(jobs[:3]):
            print(f"\n--- Job {i+1} ---")
            for key, value in job.items():
                print(f"{key}: {value}")
    else:
        print("Aucun emploi trouvé")