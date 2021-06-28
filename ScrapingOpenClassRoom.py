from bs4 import BeautifulSoup #
import requests 


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

        result_data['upc'] = soup.find('table', class_=["table-striped"]).find("tr").find("td").text
        result_data['url_page'] = url
        result_data['type'] = soup.find('table', class_=["table-striped"]).findAll("tr")[1].find("td").text
        result_data['prix_ht'] = soup.find('table', class_=["table-striped"]).findAll("tr")[2].find("td").text
        result_data['prix_ttc'] = soup.find('table', class_=["table-striped"]).findAll("tr")[3].find("td").text
        result_data['tax'] = soup.find('table', class_=["table-striped"]).findAll("tr")[4].find("td").text
        result_data['stock'] = soup.find('table', class_=["table-striped"]).findAll("tr")[5].find("td").text
        result_data['nb_revues'] = soup.find('table', class_=["table-striped"]).findAll("tr")[6].find("td").text
        try:
            result_data['description'] = soup.find('div', id=["product_description"]).find_next_sibling("p").text
        except AttributeError:
            print("Pas de description pour ", url)
            result_data['description'] = None
        result_data['titre'] = soup.find('div', class_=["product_main"]).find("h1").text
        result_data['categorie'] = (soup.find('ul', class_=["breadcrumb"])
                                        .findAll("li")[2]
                                        .text
                                        .strip())
        result_data['url_img'] = soup.find('img').attrs['src'].replace('../../', "https://books.toscrape.com/")
        result_data['user_rating'] = soup.find('p', class_=("star-rating")).attrs['class'][-1]
     
    return result_data

