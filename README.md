# Le Travail

`Le Travail` est une application visant à regrouper les offres d'emploi des entreprises françaises en un seul et même endroit.

Ce projet est actuellement en **phase Alpha**. Seules les offres de **l'Assurance Maladie (la Sécu recrute)** et du groupe **Crédit Agricole** sont pour le moment intégrées. De nouvelles sources seront ajoutées au fur et à mesure.

## Stack Technique

*   **Langage :** Python (versions 3.7 à 3.12)
*   **Framework Web :** Flask (v2.3.3)
*   **Dépendance système :** `wget`

## Installation et Lancement

**Prérequis :**
*   Un environnement de type Unix (Linux, macOS).
*   Python (<3.13) et pip installés.
*   `wget` doit être installé sur votre système. (ex: `sudo apt-get install wget` sur Debian/Ubuntu).

**Étapes :**

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/AverageCoder69/Le_travail.git
    cd Le_Travail
    ```

2.  **(Recommandé) Créez et activez un environnement virtuel :**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Installez les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note : Assurez-vous d'avoir un fichier `requirements.txt` contenant au minimum `Flask==2.3.3`)*

4.  **Lancez l'application :**
    ```bash
    python run_fusion.py
    ```

Le serveur sera accessible localement à l'adresse : `http://127.0.0.1:5003`.
