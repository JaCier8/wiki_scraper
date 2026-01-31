import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.page import Page

"""
Testing if we ignore unwanted sections 
"""


class TestContentCleaning(unittest.TestCase):

    def setUp(self):
        self.test_filename = "temp_dirty_page.html"

        local_html = """
                <html>
                    <body>
                        <div class="mw-parser-output">

                            <p>Main article, most interesting for us</p>

                            <span class="mw-editsection">
                                <a href="/edit">EDIT</a>
                            </span>

                            <div id="References">
                                <ol>
                                    <li>Notch words.</li>
                                </ol>
                            </div>

                            <div id="mw-navigation">
                                <h2>NAVIGATION menu</h2>
                            </div>

                        </div>
                    </body>
                </html>
                """

        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write(local_html)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_removing_unwanted_sections(self):

        page = Page("DirtyPage", local_file=self.test_filename)

        counter = page.get_counter()

        self.assertIn('main', counter, "Scraped from main")
        self.assertIn('most', counter, "Scraped from main")

        self.assertNotIn('edit', counter, "We should remove 'mw-editsection' section")
        self.assertNotIn('references', counter, "refernces shouldn't be taken in consideration")
        self.assertNotIn('navigation', counter, "We should remove 'mw-navigation' section")

if __name__ == '__main__':
    unittest.main()