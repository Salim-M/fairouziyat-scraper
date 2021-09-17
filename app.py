import requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from colorama import init, Fore

# init colorama
init()

BASE_URL = 'https://fairouziyat.com'

def scrape_main_page():
    print(Fore.YELLOW + '[*] Scraping the \'lyrics\' page ...')
    page = requests.get(BASE_URL + '/lyrics')
    soup = BeautifulSoup(page.content, 'html.parser')

    ul = soup.find('ul', class_='pagination')
    links = [li.a['href'] for li in ul.findAll('li')]
    
    print(Fore.GREEN + '[*] Found ' + str(len(links)) + ' pages')
    scrape_alphabet_pages(links)

def scrape_alphabet_pages(links):
    for index, link in enumerate(links):
        print(Fore.YELLOW + '[*] Scraping alphabet page ' + str(index + 1) + ' ...')
        page = requests.get(BASE_URL + link)
        soup = BeautifulSoup(page.content, 'html.parser')

        ul = soup.find('h2').findNext('ul')
        links = [li.h3.a['href'] for li in ul.findAll('li')]

        print(Fore.GREEN + '[*] Found ' + str(len(links)) + ' songs')
        scrape_song_pages(links)

def scrape_song_pages(links):
    for index, link in enumerate(links):
        print(Fore.YELLOW + '[*] Scraping song page ' + str(index + 1) + ' ...')
        page = requests.get(BASE_URL + link)
        soup = BeautifulSoup(page.content, 'html.parser')

        source = soup.find('source', {'type': 'audio/mp4'})
        if source:
            print(Fore.GREEN + '[*] Found song url, saving ...')

            link = urllib.parse.quote(source['src'],safe=':/') # <- here
            filename = source['src'].split('/')[-1]

            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(link, filename)

            print(Fore.GREEN + '[*] Done !')

scrape_main_page()