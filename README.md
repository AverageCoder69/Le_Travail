# Le Travail - Alpha 0.0.1

Interface web interactive pour explorer les offres d'emploi de la Sécurité Sociale française.

## 🚀 Démarrage rapide

### Prérequis
- Python 3.7+
- wget (pour le scraping)

### Installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd Le_Travail
```

2. **Installer les dépendances Python**
```bash
pip install -r requirements.txt
```

3. **Installer wget** (si nécessaire)
- **macOS**: `brew install wget`
- **Ubuntu**: `sudo apt install wget`
- **Windows**: [Télécharger wget](https://eternallybored.org/misc/wget/)

4. **Lancer l'application**
```bash
python run.py
```

## 📱 Interface

Une fois lancé, accédez à :
- **Interface principale**: http://localhost:5001
- **Carte interactive**: http://localhost:5001/carte

## ✨ Fonctionnalités

### 📋 Interface Liste
- **1400+ offres d'emploi** de la Sécurité Sociale
- **Filtres dynamiques** : ville, contrat, salaire
- **Recherche en temps réel**
- **Actualisation automatique** des données

### 🗺️ Carte Interactive (Alpha)
- **Géolocalisation** des offres sur une carte de France
- **Markers colorés** selon le nombre d'offres par ville
- **Popups détaillés** avec informations complètes
- **150+ villes** françaises reconnues

## 🔧 API

- `GET /jobs` - Récupérer toutes les offres
- `GET /stats` - Statistiques des offres
- `GET /refresh` - Actualiser les données

## 📊 Données

Les offres incluent :
- Titre du poste
- Employeur
- Localisation
- Type de contrat (CDI, CDD, Stage...)
- Salaire (si disponible)
- Dates de publication et limite
- Niveau requis
- Référence

## 🛠️ Développement

### Structure des fichiers
```
Le_Travail/
├── run.py              # Script de démarrage
├── app.py              # Serveur Flask
├── scrapper.py         # Scraping des données
├── index.html          # Interface principale
├── carte.html          # Carte interactive
├── jobs.json           # Données des offres
└── requirements.txt    # Dépendances Python
```

### Scraping manuel
```bash
python scrapper.py
```

## 📝 Notes

- **Version Alpha** : Fonctionnalités en développement
- **Source** : https://www.lasecurecrute.fr
- **Mise à jour** : Manuelle ou via l'interface web

## 🐛 Support

En cas de problème :
1. Vérifiez que wget est installé
2. Vérifiez les dépendances Python
3. Consultez les logs dans le terminal