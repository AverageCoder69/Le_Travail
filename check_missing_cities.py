import json

# Charger les jobs
with open('/Volumes/JeremyExternal/jeremyext/Documents/Le_Travail/jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

# Coordonnées des principales villes françaises (copié de la carte)
frenchCities = {
    'PARIS': [48.8566, 2.3522],
    'Paris': [48.8566, 2.3522],
    'MARSEILLE': [43.2965, 5.3698],
    'Marseille': [43.2965, 5.3698],
    'LYON': [45.7640, 4.8357],
    'Lyon': [45.7640, 4.8357],
    'TOULOUSE': [43.6047, 1.4442],
    'Toulouse': [43.6047, 1.4442],
    'NICE': [43.7102, 7.2620],
    'Nice': [43.7102, 7.2620],
    'NANTES': [47.2184, -1.5536],
    'Nantes': [47.2184, -1.5536],
    'MONTPELLIER': [43.6110, 3.8767],
    'Montpellier': [43.6110, 3.8767],
    'STRASBOURG': [48.5734, 7.7521],
    'Strasbourg': [48.5734, 7.7521],
    'BORDEAUX': [44.8378, -0.5792],
    'Bordeaux': [44.8378, -0.5792],
    'LILLE': [50.6292, 3.0573],
    'Lille': [50.6292, 3.0573],
    'RENNES': [48.1173, -1.6778],
    'Rennes': [48.1173, -1.6778],
    'REIMS': [49.2583, 4.0317],
    'Reims': [49.2583, 4.0317],
    'NANCY': [48.6921, 6.1844],
    'Nancy': [48.6921, 6.1844],
    'MULHOUSE': [47.7508, 7.3359],
    'Mulhouse': [47.7508, 7.3359],
    'METZ': [49.1193, 6.1757],
    'Metz': [49.1193, 6.1757],
    'ORLEANS': [47.9029, 1.9039],
    'Orléans': [47.9029, 1.9039],
    'DIJON': [47.3220, 5.0415],
    'Dijon': [47.3220, 5.0415],
    'ANGERS': [47.4784, -0.5632],
    'Angers': [47.4784, -0.5632],
    'CAEN': [49.1829, -0.3707],
    'Caen': [49.1829, -0.3707],
    'BREST': [48.3905, -4.4861],
    'Brest': [48.3905, -4.4861],
    'TOURS': [47.3941, 0.6848],
    'Tours': [47.3941, 0.6848],
    'AMIENS': [49.8941, 2.2957],
    'Amiens': [49.8941, 2.2957],
    'ROUEN': [49.4431, 1.0993],
    'Rouen': [49.4431, 1.0993],
    'LIMOGES': [45.8336, 1.2611],
    'Limoges': [45.8336, 1.2611],
    'CLERMONT-FERRAND': [45.7772, 3.0870],
    'Clermont-Ferrand': [45.7772, 3.0870],
    'BESANCON': [47.2380, 6.0243],
    'Besançon': [47.2380, 6.0243],
    'PERPIGNAN': [42.6886, 2.8948],
    'Perpignan': [42.6886, 2.8948],
    'AJACCIO': [41.9196, 8.7389],
    'Ajaccio': [41.9196, 8.7389],
    'Bastia': [42.7005, 9.4495],
    'BASTIA': [42.7005, 9.4495],
    # Région parisienne
    'BOBIGNY': [48.9077, 2.4530],
    'CRETEIL': [48.7903, 2.4552],
    'CRÉTEIL': [48.7903, 2.4552],
    'Nanterre': [48.8924, 2.2069],
    'NANTERRE': [48.8924, 2.2069],
    'Montreuil': [48.864, 2.4372],
    'MONTREUIL': [48.8641, 2.4372],
    'Versailles': [48.8014, 2.1301],
    'VERSAILLES': [48.8014, 2.1301],
    'CERGY': [49.0333, 2.0594],
    'Cergy': [49.0333, 2.0594],
    # Autres villes importantes
    'NIORT': [46.3239, -0.4594],
    'Niort': [46.3239, -0.4594],
    'BEAUVAIS': [49.4322, 2.0806],
    'Beauvais': [49.4322, 2.0806],
    'CHATEAUROUX': [46.8108, 1.6925],
    'Châteauroux': [46.8108, 1.6925],
    'LAON': [49.5637, 3.6258],
    'Laon': [49.5637, 3.6258],
    'TARBES': [43.2332, 0.0781],
    'Tarbes': [43.2332, 0.0781],
    'CHARTRES': [48.4439, 1.4845],
    'Chartres': [48.4439, 1.4845],
    'VILLEURBANNE': [45.7665, 4.8797],
    'Villeurbanne': [45.7665, 4.8797],
    'Bourg-en-Bresse': [46.2050, 5.2317],
    'BOURG-EN-BRESSE': [46.2050, 5.2317]
}

def getCityCoordinates(cityName):
    normalizedCity = cityName.strip()
    
    # Recherche exacte
    if normalizedCity in frenchCities:
        return frenchCities[normalizedCity]
    
    # Recherche insensible à la casse
    cityLower = normalizedCity.lower()
    for city, coords in frenchCities.items():
        if city.lower() == cityLower:
            return coords
    
    # Recherche partielle
    for city, coords in frenchCities.items():
        if city.lower() in cityLower or cityLower in city.lower():
            return coords
    
    return None

# Analyser les villes manquantes
locations = {}
missing_cities = set()

for job in jobs:
    lieu = job.get('lieu', 'NA')
    if lieu != 'NA':
        if lieu in locations:
            locations[lieu] += 1
        else:
            locations[lieu] = 1
            
        # Vérifier si la ville est trouvée
        if not getCityCoordinates(lieu):
            missing_cities.add(lieu)

print("🗺️ Villes manquantes dans la base de données:")
print(f"Total: {len(missing_cities)} villes")
print()

# Trier par nombre d'offres
missing_with_count = []
for city in missing_cities:
    missing_with_count.append((city, locations[city]))

missing_with_count.sort(key=lambda x: x[1], reverse=True)

print("Top 20 des villes manquantes:")
for city, count in missing_with_count[:20]:
    print(f"  {city}: {count} offres")

print()
print("Autres villes manquantes:")
for city, count in missing_with_count[20:]:
    if count >= 2:  # Afficher seulement celles avec 2+ offres
        print(f"  {city}: {count} offres")