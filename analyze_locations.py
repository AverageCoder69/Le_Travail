import json

# Charger les jobs
with open('/Volumes/JeremyExternal/jeremyext/Documents/Le_Travail/jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

# Analyser les lieux
locations = {}
for job in jobs:
    lieu = job.get('lieu', 'NA')
    if lieu != 'NA':
        if lieu in locations:
            locations[lieu] += 1
        else:
            locations[lieu] = 1

# Afficher les villes les plus fréquentes
print('🗺️ Analyse des localisations:')
print(f'Total d\'offres: {len(jobs)}')
print(f'Offres avec localisation: {len([j for j in jobs if j.get("lieu") != "NA"])}')
print(f'Villes uniques: {len(locations)}')
print()
print('Top 15 des villes:')
sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)
for ville, count in sorted_locations[:15]:
    print(f'  {ville}: {count} offres')

print()
print('Quelques exemples de villes:')
for ville, count in sorted_locations[15:30]:
    print(f'  {ville}: {count} offres')