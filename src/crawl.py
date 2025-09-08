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

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    url = []
    a = soup.find_all('a', href=True)
    for link in a:
        href = link['href']
        if href.startswith('/'):
            href = base_url + href
        elif not href.startswith('http'):
            print(f"Invalid URL found: {href}")
            raise ValueError(f"Invalid URL found: {href}")
        url.append(href)
    return url

def get_images_from_html(html, base_url):
    
        

