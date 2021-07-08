# Projet 2 ScrapingOpenClassRoom

Ce programme à été crée pour le projet 2, et il sert à récupérer les données d'un site de livre
en les classant par thème et en téléchargeant les images.

***
## DEPUIS UN ENVIRONEMENT VIRTUEL

1. Depuis le terminal lancer la commande "python3 -m venv env" pour créer un nouvelle environnement virtuel
puis tapez "source env/bin/activate"

2. Ensuite depuis votre environnement virtuel installer le fichier requirements.txt inclus dans le dossier avec la
commande "pip install -r requirements.txt"

3. enfin lancer la commande "python3 ScrapingOpenClassRoom.py" pour lancer le programme.

***
## LANCEZ LE PROGRAMME

1. Ouvrez votre terminal et tapez cette commande "$ pip install -r requirements.txt"

2. Ensuite, tapez la commande "$ Python3 ScrapingOpenClassRoom.py"

3. repondez "N" a la question "Voulez vous réutillisé les URLS du fichier ?

4. enfin, il va aller chercher les images de chaque livre et les stockés dans un dossier "image" pour les images , et les données dans un dossier "data" qui contient les fichiers csv pour chaque catégorie de livre.

***
## DESCRIPTION DU CODE

En s'exécutant le code va d'abord trouver le nombre total de pages à
scraper, puis il va aller chercher les liens de chaque categorie et envoyer les liens des pages
dans un dictionnaire.

ENJOY
