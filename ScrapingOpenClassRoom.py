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

