import unittest
import os
import sys

# Dodajemy katalog nadrzędny do ścieżki
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.page import Page


class TestLinkFiltering(unittest.TestCase):

    def setUp(self):
        # Creating HTML file with valid and non-valid links.
        self.test_filename = "temp_test_links.html"

        fake_html = """
        <html>
            <body>
                <div class="mw-parser-output">
                    <p>
                        <a href="/w/Diamond"></a>
                        <a href="/w/Gold_Ingot"></a>
                        
                        <a href="/w/File:Diamond_Image.png"></a>
                        <a href="/w/Special:Random"></a>
                        <a href="/w/Talk:Diamond"></a>
                        <a href="https://google.com"></a>
                        <a Not a link></a>
                    </p>
                </div>
            </body>
        </html>
        """

        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write(fake_html)

    def tearDown(self):
        # Deleting file afterwards
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_link_filtering_logic(self):
        # Creatinng Page class
        page = Page("TestPage", local_file=self.test_filename)

        # Getting links
        links = page.get_links()


        self.assertIn("/w/Diamond", links, "This link should be considered.")
        self.assertIn("/w/Gold_Ingot", links, "This link should be considered.")

        self.assertNotIn("/w/File:Diamond_Image.png", links, "File: should be ignored.")
        self.assertNotIn("/w/Special:Random", links, "Special: should be ignored.")
        self.assertNotIn("/w/Talk:Diamond", links, "Talk: should be ignored.")
        self.assertNotIn("https://google.com", links, "Links outside of wiki should be ignored.")
        self.assertNotIn("Not a link", links, "Not href lines should be ignored.")


if __name__ == '__main__':
    unittest.main()