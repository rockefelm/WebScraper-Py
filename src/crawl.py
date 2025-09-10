from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import asyncio
import aiohttp 

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
    urls = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.startswith(('http', '/')):
            raise ValueError(f"Invalid URL found: {href}")
        urls.append(urljoin(base_url, href))
    return urls

def get_images_from_html(html, base_url):
    images = []
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img', src=True):
        src = img['src']
        if not src.startswith(('http', '/')):
            raise ValueError(f"Invalid image URL found: {src}")
        images.append(urljoin(base_url, src))
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
    
class AsyncCrawler:

    def __init__(self, base_url, page_data):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = page_data
        self.lock = asyncio.Lock()
        self.max_concurrency = 5
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            self.page_data[normalized_url] = {}  # placeholder
            return True

    async def get_html(self, url):
        try:
            async with self.session.get(url) as response:
                if response.status > 399:
                    raise Exception(f"got HTTP error: {response.status} {response.reason}")
                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    raise Exception(f"got non-HTML response: {content_type}")
                return await response.text()
        except Exception as e:
            raise Exception(f"network error while fetching {url}: {e}")
    
    async def safe_get_html(self, url):
        try:
            return await self.get_html(url)
        except Exception as e:
            print(f"{e}")
            return None
      

    async def crawl_page(self, current_url=None):
        if current_url is None:
            current_url = self.base_url
        
        parsed_base = urlparse(self.base_url)
        parsed_current = urlparse(current_url)
        if parsed_current.netloc != parsed_base.netloc:
            return

        normalized_url = normalize_url(current_url)
        if not await self.add_page_visit(normalized_url):
            return

        print(f"crawling {current_url}")
        async with self.semaphore:
            html = await self.safe_get_html(current_url)
            if html is None:
                # cleanup placeholder on failure
                async with self.lock:
                    self.page_data.pop(normalized_url, None)
                return 
            page_info = extract_page_data(html, current_url)

        async with self.lock:
            self.page_data[normalized_url] = page_info

        children = [next_url for next_url in page_info['outgoing_links'] if not next_url.endswith('.xml')]
        tasks = [asyncio.create_task(self.crawl_page(next_url))
                 for next_url in children]
        if tasks:
            await asyncio.gather(*tasks)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url, {}) as crawler:
        return await crawler.crawl()       
