import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.page import Page

"""
Tests table getting function from page
"""

class TestTableParsing(unittest.TestCase):

    def setUp(self):
        self.test_filename = "temp_table_page.html"

        local_html = """
        <html>
            <body>
                <h2>First</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Diamond</td>
                            <td>1-2</td>
                        </tr>
                    </tbody>
                </table>

                <h2>Second</h2>
                <table>
                    <tr>
                        <td>Material</td>
                        <td>Shape</td>
                    </tr>
                    <tr>
                        <td>Wood</td>
                        <td>Block</td>
                    </tr>
                    <tr>
                        <td>Stick</td>
                        <td>Line</td>
                    </tr>
                </table>
            </body>
        </html>
        """

        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write(local_html)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_table_extraction(self):
        page = Page("TablePage", local_file=self.test_filename)

        tables = page.get_tables()

        self.assertEqual(len(tables), 2, "Two tables should be returned")

        df1 = tables[0]

        val1 = df1.iloc[0, 0]
        self.assertEqual(val1, "Diamond", "First table should include Diamond")

    def test_header_parsing_option(self):
        page = Page("TablePage", local_file=self.test_filename)

        tables = page.get_tables(first_row_is_header=True)

        df2 = tables[1]

        self.assertIn("Material", df2.columns, "First column header should be Material")


if __name__ == '__main__':
    unittest.main()