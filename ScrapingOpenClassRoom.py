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
# trouver les lien des
def trouver_liens_categorie(numeros_pages=[1],
                            format_url='https://books.toscrape.com/catalogue/page-{}.html'):
    """
    Permet de trouver tout les liens des pages de categories a scrapper.
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
