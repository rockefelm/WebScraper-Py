from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.netloc.lower() + parsed.path.rstrip('/')

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1')
    return h1.get_text(strip=True) if h1 else ""

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('main')
    if main:
        p = main.find('p')
        if p:
            return p.get_text(strip=True)
    p = soup.find('p')
    return p.get_text(strip=True) if p else ""

