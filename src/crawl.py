from urllib.parse import urlparse
from bs4 import BeautifulSoup # pyright: ignore[reportMissingModuleSource]

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
            raise ValueError(f"Invalid URL found: {href}")
        url.append(href)
    return url

def get_images_from_html(html, base_url):
    images = []
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img', src=True)
    for img in img_tags:
        src = img['src']
        if src.startswith('/'):
            src = base_url + src
        elif not src.startswith('http'):
            raise ValueError(f"Invalid image URL found: {src}")
        images.append(src)
    return images

def extract_page_data(html, page_url):
    title = get_h1_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    urls = get_urls_from_html(html, page_url)
    images = get_images_from_html(html, page_url)
    return {
        "url": page_url,
        "h1": title,
        "first_paragraph": first_paragraph,
        "outgoing_links": urls,
        "image_urls": images
    }
        

