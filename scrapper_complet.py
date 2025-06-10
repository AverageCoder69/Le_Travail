import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """Configure le driver Chrome en mode headless"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Erreur lors de l'initialisation du driver Chrome: {e}")
        print("Tentative avec le mode non-headless...")
        try:
            # Essayer sans headless pour debug
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e2:
            print(f"Erreur: {e2}")
            return None

def parse_job_card(card):
    """Parse une carte d'offre d'emploi"""
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
    
    # ID de l'offre
    if card.get('id'):
        job['id'] = card.get('id')
    
    return job

def scrape_all_jobs():
    """Scrape toutes les offres d'emploi en cliquant sur 'Voir plus'"""
    driver = setup_driver()
    if not driver:
        return []
    
    try:
        print("🔍 Chargement de la page principale...")
        driver.get("https://www.lasecurecrute.fr/recherche")
        
        # Attendre que la page se charge
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "carte-offre"))
        )
        
        all_jobs = []
        clicks = 0
        max_clicks = 100  # Limite de sécurité
        previous_count = 0
        
        while clicks < max_clicks:
            # Parser les offres actuelles
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_cards = soup.find_all('article', class_='carte-offre')
            current_count = len(job_cards)
            
            print(f"📋 Trouvé {current_count} offres sur la page actuelle...")
            
            # Vérifier si de nouvelles offres ont été chargées
            if clicks > 0 and current_count == previous_count:
                print("⚠️ Aucune nouvelle offre chargée, arrêt")
                break
            
            previous_count = current_count
            
            # Chercher le bouton "Voir plus d'offres" visible
            try:
                load_more_buttons = driver.find_elements(By.CSS_SELECTOR, ".load-more:not(.hidden) button")
                
                if not load_more_buttons:
                    print("✅ Plus de bouton 'Voir plus' disponible")
                    break
                
                button = load_more_buttons[0]
                
                # Scroll vers le bouton et attendre
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                time.sleep(2)
                
                # Essayer plusieurs méthodes de clic
                print(f"🔄 Clic sur 'Voir plus d'offres' ({clicks + 1})...")
                try:
                    # Méthode 1: Clic normal
                    button.click()
                except Exception:
                    try:
                        # Méthode 2: Clic JavaScript
                        driver.execute_script("arguments[0].click();", button)
                    except Exception:
                        # Méthode 3: Clic avec ActionChains
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(driver).move_to_element(button).click().perform()
                
                # Attendre que de nouvelles offres se chargent
                print("⏳ Attente du chargement des nouvelles offres...")
                time.sleep(5)
                
                # Attendre explicitement qu'il y ait plus d'offres
                try:
                    WebDriverWait(driver, 10).until(
                        lambda d: len(d.find_elements(By.CLASS_NAME, "carte-offre")) > current_count
                    )
                    print("✅ Nouvelles offres détectées!")
                except TimeoutException:
                    print("⚠️ Timeout - pas de nouvelles offres détectées")
                
                clicks += 1
                
            except (TimeoutException, NoSuchElementException):
                print("✅ Plus de bouton 'Voir plus' disponible")
                break
            except Exception as e:
                print(f"❌ Erreur lors du clic: {e}")
                break
        
        # Parser toutes les offres finales
        print("📊 Parsing final de toutes les offres...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_cards = soup.find_all('article', class_='carte-offre')
        
        for i, card in enumerate(job_cards):
            job = parse_job_card(card)
            if job:
                # Assigner un ID unique si pas présent
                if 'id' not in job or not job['id']:
                    job['id'] = f'offre_{i+1}'
                all_jobs.append(job)
        
        print(f"✅ Total de {len(all_jobs)} offres récupérées!")
        return all_jobs
        
    except Exception as e:
        print(f"❌ Erreur lors du scraping: {e}")
        return []
    
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🚀 Début du scraping complet...")
    jobs = scrape_all_jobs()
    
    if jobs:
        # Sauvegarder en JSON
        with open('/Volumes/JeremyExternal/jeremyext/Documents/Le_Travail/jobs.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        
        print(f"💾 {len(jobs)} offres d'emploi sauvegardées dans jobs.json")
        
        # Afficher quelques statistiques
        with_salary = len([job for job in jobs if job.get('salaire') != 'NA'])
        locations = set(job.get('lieu') for job in jobs if job.get('lieu') != 'NA')
        contracts = set(job.get('type_contrat') for job in jobs if job.get('type_contrat') != 'NA')
        
        print(f"📊 Statistiques:")
        print(f"   - Offres avec salaire: {with_salary}")
        print(f"   - Villes différentes: {len(locations)}")
        print(f"   - Types de contrats: {len(contracts)}")
        
    else:
        print("❌ Aucune offre récupérée")