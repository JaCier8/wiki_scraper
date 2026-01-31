import string
import sys
from collections import Counter
from io import StringIO

import pandas as pd

from bs4 import BeautifulSoup
import requests

# Class containing one scraped page
class Page:
    def __init__(self, sub_page, local_file=None):
        # Scraping from web
        if not local_file:
            self.url = 'https://minecraft.wiki/' + sub_page

            response = requests.get(self.url)
            if response.status_code != 200:
                print("Failed downloading site with error: ", response.status_code, self.url)
            self.soup = BeautifulSoup(response.content, "html.parser")
        # Scraping from local html file
        else:
            self.url = f"file://{local_file}"
            with open(local_file, 'r', encoding='utf-8') as f:
                self.soup = BeautifulSoup(f , "html.parser")

        if self.soup.p:
            self.summary = self.soup.p.get_text()
        else:
            print(f"Warning: No summary found for {self.url}")

    def get_tables(self, first_row_is_header=False, local_file=None)->list:

        html_content = StringIO(str(self.soup))

        if first_row_is_header:
            tables = pd.read_html(html_content, header=0)
        else:
            tables = pd.read_html(html_content)

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
            else: return None

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

        excluded_prefixes = (
            '/w/Special:',
            '/w/File:',
            '/w/Talk:',
            '/w/User:',
            '/w/Category:',
            '/w/Template:',
            '/w/Help:',
            '/w/Minecraft_Wiki:')

        found_links = set()

        for link in self.soup.find_all('a'):

            href = link.get('href')

            if href and href.startswith('/w/') and not href.startswith(excluded_prefixes):
                found_links.add(href)

        return found_links


