import sys
import pandas as pd

from bs4 import BeautifulSoup
import requests

# Class containing one scraped page
class Page:
    def __init__(self, sub_page :str):
        self.url = 'https://minecraft.wiki/' + sub_page

        response = requests.get(self.url)
        if response.status_code != 200:
            print("Failed downloading site with error: ", response.status_code)
            sys.exit(1)
        soup = BeautifulSoup(response.content, "html.parser")

        # Doesnt work for cobblestone ;(
        self.summary = soup.p.get_text()

    def getTables(self, first_row_is_header=False)->list:
        if first_row_is_header:
            tables = pd.read_html(self.url, header=0)
        else:
            tables = pd.read_html(self.url)
        return tables

