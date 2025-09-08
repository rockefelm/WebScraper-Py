import unittest
from crawl import (
    normalize_url, 
    get_h1_from_html, 
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html
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
                      '<img src="https://blog.boot.dev/banner.png alt="banner">'
                      '</body></html>')
        actual = get_images_from_html(input_bopy, input_url)
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
        
if __name__ == "__main__":
    unittest.main()