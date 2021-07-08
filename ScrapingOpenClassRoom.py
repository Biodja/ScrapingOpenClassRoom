from bs4 import BeautifulSoup # bibliothèque d'analyse syntaxique de documents html et xml (produit un arbre syntaxique pour chercher et modifier les éléments
import requests # permet de faire des requetes html
import concurrent
import concurrent.futures #lancer des taches en parrallèle avec le multi threading
import pandas as pd # permet la manipulation et l'analyse de donnée
import os


SESSION = requests.Session()



def trouver_nb_pages_categorie(url="https://books.toscrape.com/catalogue/category/books_1/index.html"):

    response = SESSION.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'lxml')
        nb_pages = soup.find ('ul', class_= ['pager']).find('li', class_='current').text.strip()[-2:]
        nb_pages = int(nb_pages)
        return nb_pages

# trouver les lien des categories


def trouver_liens_categorie(numeros_pages=[1],
                            format_url='https://books.toscrape.com/catalogue/page-{}.html'):
    """
    Permet de trouver tout les liens des pages d'une categories a scrapper.
    numeros_pages: liste des numéros des pages à scraper
    format_url: lien à formater correspondant a une categorie du catalogue
    """
    links = []
    for numero_page in numeros_pages: 
        url = format_url.format(numero_page) 
        response = SESSION.get(url)
        if response.ok:
            print('Page: ' + str(numero_page))
            soup = BeautifulSoup(response.text, 'lxml')
            articles: list = soup.findAll('article')
            for article in articles:
                a = article.find('a')
                link = a['href']
                links.append('https://books.toscrape.com/catalogue/' + link)
            
    print("Nombres de liens reçu",len(links))
    return links

# parsing de chaque page du catalogue 

def parser_livre(url: str="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", 
                      ) -> dict:
    """
    Ceci est la fonction qui scrape la page du livre à l'url indiquée. Elle retourne un dict contenant les données récupérées.

    Par exemple pour le livre A Light in the Attic :
    > print(parser_livre("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"))
    > {"titre": "A Light in the Attic", ...}
    """
    response = SESSION.get(url)
    result_data = {}
    if response.ok:
        soup = BeautifulSoup(response.content, 'lxml') 
        result_data['universal_product_code(upc)'] = soup.find('table', class_=["table-striped"]).find("tr").find("td").text
        result_data['product_page_url'] = url
        result_data['price_excluding_tax'] = soup.find('table', class_=["table-striped"]).findAll("tr")[2].find("td").text
        result_data['price_including_tax'] = soup.find('table', class_=["table-striped"]).findAll("tr")[3].find("td").text
        result_data['number_available'] = soup.find('table', class_=["table-striped"]).findAll("tr")[5].find("td").text
        try:
            result_data['product_description'] = soup.find('div', id=["product_description"]).find_next_sibling("p").text
        except AttributeError:
            print("Pas de description pour ", url)
            result_data['product_description'] = None
        result_data['title'] = soup.find('div', class_=["product_main"]).find("h1").text
        result_data['category'] = (soup.find('ul', class_=["breadcrumb"])
                                        .findAll("li")[2]
                                        .text
                                        .strip())
        result_data['image_url'] = soup.find('img').attrs['src'].replace('../../', "https://books.toscrape.com/")
        result_data['review_rating'] = soup.find('p', class_=("star-rating")).attrs['class'][-1]
    
    return result_data

# création d'une fonctionalité qui permet de demander a l'utilisateurs si il veut garder ou ecraser son fichier text contenant les liens reçu


if __name__ == "__main__":
    lien_recu = input('Voulez vous réutillisé les URLS du fichier ? O/N ')
    if lien_recu.lower() == 'o':
        with open('urls2.txt', "r") as file:
            links = file.readlines()
    else:
        links = trouver_liens_categorie(range(1, trouver_nb_pages_categorie() + 1))
        with open('urls2.txt', 'w') as file:
            for link in links:
                file.write(link + "\n")
    list_de_donnee = []

    nb_liens = len(links)
    print("Nombre de liens", nb_liens)

    ### Nouveau code avec threading
    
    import time
    debut = time.time()
    print("début")
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        futures = [executor.submit(parser_livre, link.strip()) for link in links]
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            list_de_donnee.append(future.result())
            print((i + 1) * 100 // nb_liens, "%", end="\r", flush=True)
    print("fin", time.time() - debut)
    
    ### Ancien code séquential
    """
    import time
    debut = time.time()
    print("début")
    for i, link in enumerate(links):
        print((i + 1) * 100 // nb_liens, "%", end="\r", flush=True)
        link = link.strip()
        list_de_donnee.append(parser_livre(link))
    print("fin", time.time() - debut)
    """
    
        
    df = pd.DataFrame.from_dict(list_de_donnee)

    # nettoyage des données
  
    df["number_available"] = df["number_available"].str.split("(").str[-1].str.split().str[0].astype(int)
     
    
    
    df["review_rating"] = df["review_rating"].str.replace("One","1")
    df["review_rating"] = df["review_rating"].str.replace("Two","2")
    df["review_rating"] = df["review_rating"].str.replace("Three","3")
    df["review_rating"] = df["review_rating"].str.replace("Four","4")
    df["review_rating"] = df["review_rating"].str.replace("Five","5")
    
    df["review_rating"] = df["review_rating"].astype(int)


    grouped = df.groupby("category")

    try:
        os.mkdir("data")
    except:
        pass

    for nom_categorie, df_categorie in grouped:
        df_categorie.to_csv("data/{}.csv".format(nom_categorie), index=False)
        

    try:
        os.mkdir("image")
    except:
        pass

    # Dernières modifications
    print("Données dupliquées"),
    print(df[df.duplicated(subset=["title"])])
    nb_images = 0

    def download_image(titre, url_img):
        titre = titre.replace("/", "_")
        with open (f"image/{titre}.jpg", "wb") as f:
            f.write(SESSION.get(url_img).content)

    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        futures = [executor.submit(download_image, titre, url_img)
                   for _, (titre, url_img) in df[["title", "image_url"]].iterrows()]
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            future.result()
            nb_images += 1
            print((i+1) * 100 // nb_liens, "%", end="\r", flush=True)
    print(f"{nb_images} images effectivement téléchargées")

print("Scraping du site termine")
