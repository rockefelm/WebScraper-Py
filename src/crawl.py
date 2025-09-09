from urllib.parse import urlparse
from bs4 import BeautifulSoup # pyright: ignore[reportMissingModuleSource]
import requests

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

def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    base_url_obj = urlparse(base_url)
    current_url_obj = urlparse(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return page_data

    normalized_url = normalize_url(current_url)

    if normalized_url in page_data:
        return page_data

    print(f"crawling {current_url}")
    html = safe_get_html(current_url)
    if html is None:
        return page_data

    page_info = extract_page_data(html, current_url)
    page_data[normalized_url] = page_info

    next_urls = get_urls_from_html(html, base_url)
    for next_url in next_urls:
        page_data = crawl_page(base_url, next_url, page_data)

    return page_data


def get_html(url):
    try:
        response = requests.get(url)
    except Exception as e:
        raise Exception(f"network error while fetching {url}: {e}")

    if response.status_code > 399:
        raise Exception(f"got HTTP error: {response.status_code} {response.reason}")

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(f"got non-HTML response: {content_type}")

    return response.text


def safe_get_html(url):
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None
        

