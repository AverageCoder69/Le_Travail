# Le Travail - Structure du Projet

## 🎯 Système Principal (Recommandé)

**Interface Unifiée - 3450+ offres**
- `run_fusion.py` - **Script de démarrage principal**
- `app_fusion.py` - Serveur Flask unifié  
- `index_fusion.html` - Interface complète avec filtres avancés
- `scrapper_fusion_fast.py` - Scraper optimisé (12 secondes)
- `jobs_fusion.json` - Base de données unifiée

**URL:** http://localhost:5003

## 📊 Sources de Données

**Sécurité Sociale** (~1486 offres)
- `scrapper.py` - Scraper Sécurité Sociale
- `jobs.json` - Données Sécurité Sociale

**Crédit Agricole** (~1964 offres, 18 employeurs)
- `scrapper_ca_v2.py` - Scraper Crédit Agricole optimisé  
- `jobs_ca.json` - Données Crédit Agricole

## 🔧 Systèmes Séparés (Optionnels)

**Sécurité Sociale Seule**
- `run.py` → `app.py` → `index.html`
- Port 5001

**Crédit Agricole Seul**  
- `run_ca.py` → `app_ca.py` → `index_ca.html`
- Port 5002

## 📁 Autres Fichiers

- `carte.html` - Carte interactive (legacy)
- `requirements.txt` - Dépendances Python
- `README.md` - Documentation utilisateur
- `LICENSE` - Licence du projet

## 🚀 Utilisation Recommandée

```bash
# Système complet unifié (recommandé)
python run_fusion.py

# Systèmes séparés (optionnels)
python run.py        # Sécurité Sociale seule
python run_ca.py     # Crédit Agricole seul
```

## ✨ Fonctionnalités Principales

- **3450+ offres** fusionnées (Sécu + CA)
- **Employeurs réels** du Groupe Crédit Agricole
- **Villes organisées** (🇫🇷 France / 🌍 International)  
- **Filtres avancés** (source, employeur, secteur, lieu)
- **Scraping ultra-rapide** (12 secondes vs 20 minutes)
- **Interface responsive** et moderne
- **API REST** complète (/jobs, /stats, /refresh)