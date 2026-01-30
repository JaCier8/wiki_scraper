import string
import sys
from collections import Counter

import pandas as pd

from bs4 import BeautifulSoup
import requests

# Class containing one scraped page
class Page:
    def __init__(self, sub_page :str):
        self.url = 'https://minecraft.wiki/' + sub_page

        response = requests.get(self.url)
        if response.status_code != 200:
            print("Failed downloading site with error: ", response.status_code, self.url)
            sys.exit(1)
        self.soup = BeautifulSoup(response.content, "html.parser")

        # Doesnt work for cobblestone ;(
        self.summary = self.soup.p.get_text()

    def get_tables(self, first_row_is_header=False)->list:
        if first_row_is_header:
            tables = pd.read_html(self.url, header=0)
        else:
            tables = pd.read_html(self.url)
        return tables

    def get_counter(self):
        # Parsing text from HTML
        divs = self.soup.find('div', class_='mw-parser-output')

        # Delete chosen headers from HTML
        header_to_del = ['Navigation', 'References', 'mw-navigation']
        for header_name in header_to_del:
            if divs:
                header = divs.find(id=header_name)

            if header:
                header.decompose()

        # Delete chosen classes from HTML
        classes_to_del = ['mw-references-wrap', 'mw-editsection']
        for class_name in classes_to_del:
            classes = divs.find_all(class_=class_name)
            for clas in classes:
                clas.decompose()

        # Plain text from parsed HTML
        text = divs.get_text()

        # Making everything lowercase to eliminate double counting
        text = text.lower()

        # Standard signs plus some find by tests
        to_del_signs = string.punctuation + string.digits + '×' + '–' + '⁄' + '\u200c'

        for sign in to_del_signs:
            text = text.replace(sign, ' ')

        words_list = text.split()

        return Counter(words_list)

    def get_links(self):


        # TODO filtracja special
        found_links = {
            link.get('href')
            for link in self.soup.find_all('a')
            if link.get('href', '').startswith('/w/')
        }

        return found_links


