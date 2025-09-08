import unittest
from crawl import (
    normalize_url, 
    get_h1_from_html, 
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test2_normalize_url(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test3_normalize_url(self):
        input_url = "http://blog.bOOt.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test4_normalize_url(self):
        input_url = "http://BlOg.BoOt.DeV/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_get_h1(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)
    
    def test_get_h1_no_h1(self):
        input_body = "<html><body><h2>No H1 here</h2></body></html>"
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = "<html><body><h1>No paragraph here</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
        
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = "<html><body><p>Only paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "Only paragraph."
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href=/path><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/path"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_and_absolute_mixed(self):
        input_url = "https://blog.bood.dev"
        input_body = ('<html><body>'
                      '<a href=/path><span>Boot.dev</span></a>'
                      '<a href="https://blog.boot.dev/other"><span>Boot.dev'
                      '</span></a></body></html>')
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://blog.bood.dev/path",
            "https://blog.boot.dev/other"
        ]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_invalid(self): 
        input_url = "https://blog.boot.dev"
        input_body = ("<html><body>"
            "<a href='invalid'><span>Boot.dev</span>"
            "</a></body></html>")
        actual = "Invalid URL found: invalid"
        with self.assertRaises(ValueError) as cm:
            get_urls_from_html(input_body, input_url)
        self.assertEqual(str(cm.exception), actual)

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = ('<html><body>'
                      '<img src="https://blog.boot.dev/logo.png" alt="Logo">'
                      '</body></html>')
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute_and_relative_mixed(self):
        input_url = "https://blog.boot.dev"
        input_body = ('<html><body>'
                      '<img src="/logo.png" alt="logo">'
                      '<img src="https://blog.boot.dev/banner.png" alt="banner">'
                      '</body></html>')
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://blog.boot.dev/logo.png",
            "https://blog.boot.dev/banner.png"
        ]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_invalid(self):
        input_url = "https://blog.boot.dev"
        input_body = ('<html><body>'
                      '<img src="invalid" alt="invalid">'
                      '</body></html>')
        expected = "Invalid image URL found: invalid"
        with self.assertRaises(ValueError) as cm:
            get_images_from_html(input_body, input_url)
        self.assertEqual(str(cm.exception), expected)


    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_h1_no_paragraph_no_links_no_images(self):
        input_url = "https://blog.boot.dev"
        input_body = "<html><body></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": input_url,
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple_links_and_images(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Title</h1>
            <p>Paragraph</p>
            <a href="/link1">Link 1</a>
            <a href="https://external.com/page">External</a>
            <img src="/img1.jpg" alt="Img1">
            <img src="https://external.com/img2.jpg" alt="Img2">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": input_url,
            "h1": "Title",
            "first_paragraph": "Paragraph",
            "outgoing_links": [
                "https://blog.boot.dev/link1",
                "https://external.com/page"
            ],
            "image_urls": [
                "https://blog.boot.dev/img1.jpg",
                "https://external.com/img2.jpg"
            ]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_main_paragraph_priority(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <main><p>Main paragraph.</p></main>
            <p>Other paragraph.</p>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": input_url,
            "h1": "",
            "first_paragraph": "Main paragraph.",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_invalid_link(self):
        input_url = "https://blog.boot.dev"
        input_body = "<html><body><a href='invalid'>Bad Link</a></body></html>"
        with self.assertRaises(ValueError) as cm:
            extract_page_data(input_body, input_url)
        self.assertEqual(str(cm.exception), "Invalid URL found: invalid")

    def test_extract_page_data_invalid_image(self):
        input_url = "https://blog.boot.dev"
        input_body = "<html><body><img src='invalid' alt='bad'></body></html>"
        with self.assertRaises(ValueError) as cm:
            extract_page_data(input_body, input_url)
        self.assertEqual(str(cm.exception), "Invalid image URL found: invalid")

    def test_extract_page_data_empty_html(self):
        input_url = "https://blog.boot.dev"
        input_body = ""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": input_url,
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_duplicate_tags(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>First Title</h1>
            <h1>Second Title</h1>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <img src="/img1.jpg" alt="Img1">
            <img src="/img2.jpg" alt="Img2">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": input_url,
            "h1": "First Title",
            "first_paragraph": "First paragraph.",
            "outgoing_links": [
                "https://blog.boot.dev/link1",
                "https://blog.boot.dev/link2"
            ],
            "image_urls": [
                "https://blog.boot.dev/img1.jpg",
                "https://blog.boot.dev/img2.jpg"
            ]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_unusual_but_valid(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1></h1>
            <main></main>
            <p></p>
            <a href="/link"></a>
            <img src="/img.jpg">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": input_url,
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": ["https://blog.boot.dev/link"],
            "image_urls": ["https://blog.boot.dev/img.jpg"]
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()