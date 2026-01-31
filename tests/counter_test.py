import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.page import Page

"""
Testing parsing words for word_counter function
"""

class TestWordCounter(unittest.TestCase):

    def setUp(self):
        # Making an HTML file to test our text parsing before counting words
        self.test_filename = "temp_test_counter.html"

        local_html = """
        <html>
            <body>
                <div class="mw-parser-output">
                    <p>
                        TEXT, text!, TExt1 
                        other
                        12345
                    </p>
                </div>
            </body>
        </html>
        """

        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write(local_html)

    def tearDown(self):
        # Deleting fake html file afterwards
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_counting_normalization(self):
        # Local page
        page = Page("TestPage", local_file=self.test_filename)

        # Getting counter from page class
        counter = page.get_counter()

        self.assertEqual(counter['text'], 3,
                         "'text' Should appear 3 times.")
        self.assertEqual(counter['other'], 1,
                        "'other' Should appear 1 time.")
        self.assertNotIn('text!', counter,
                         "Non letters should be removed.")
        self.assertNotIn('12345', counter, "Number should be removed as well")


if __name__ == '__main__':
    unittest.main()