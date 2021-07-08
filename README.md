# Projet 2 ScrapingOpenClassRoom

Ce programme à été crée pour le projet 2, et il sert à récupérer les données d'un site de livre
en les classant par thème et en téléchargeant les images.

***
## INSTALLATION DANS UN ENVIRONEMENT VIRTUEL

1. Depuis le terminal lancer la commande "python3 -m venv env" pour créer un nouvelle environnement virtuel
puis tapez "source env/bin/activate"

2. depuis votre environnement virtuel tapez "git clone https://github.com/Biodja/ScrapingOpenClassRoom.git"


3. lancer la commande "pip install -r requirements.txt" pour installer les dépendances .

***
## LANCEZ LE PROGRAMME

4. Tapez la commande "$ Python3 ScrapingOpenClassRoom.py"

5. Repondez "N" a la question "Voulez vous réutillisé les URLS du fichier ?

6. Il va aller chercher les images de chaque livre et les stockés dans un dossier "image" pour les images , et les données dans un dossier "data" qui contient les fichiers csv pour chaque catégorie de livre.

***
## DESCRIPTION DU CODE

En s'exécutant le code va d'abord trouver le nombre total de pages à
scraper, puis il va aller chercher les liens de chaque categorie et envoyer les liens des pages
dans un dictionnaire.

**ENJOY**
