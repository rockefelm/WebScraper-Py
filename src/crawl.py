from urllib.parse import urlparse, urlunparse, quote, unquote

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.netloc.lower() + parsed.path.rstrip('/')