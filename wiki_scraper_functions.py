import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import time

from wordfreq import word_frequency, top_n_list

from classes import page
import pandas as pd

def get_summary(page):
    print(page.summary)

def nth_table(n, page, csv_name,first_row_is_header=False):
    df_list = page.get_tables(first_row_is_header=first_row_is_header)
    if len(df_list) < n:
        print(n, "is exceeding number of tables on site")

    df = df_list[n-1]
    df.to_csv("csv_name.csv")
    print(df)


def read_word_counts() -> Counter:
    if os.path.exists('word_counts.json'):
        with open('word_counts.json', 'r', encoding='utf-8') as f:
            old_json = json.load(f)
            old_counter = Counter(old_json)
    else:
        old_counter = Counter()
    return old_counter;

def dfs(current_page, target_depth, current_depth, wait, already_found_links):
    word_counter(current_page)
    if current_depth < target_depth:
        page_links = current_page.get_links()

        page_links -= already_found_links
        already_found_links.update(page_links)

        for link in page_links:
            new_page = page.Page(link)
            time.sleep(wait)
            dfs(new_page, target_depth,
                current_depth + 1, wait,
                already_found_links)

def word_counter(page):

    # Get counter from page class
    counter = page.get_counter()

    # Finding if word_counter already exists, and we create or modify one
    old_counter = read_word_counts()

    old_counter.update(counter)

    with open('word_counts.json', 'w', encoding='utf-8') as f:
        json.dump(old_counter, f, ensure_ascii=False, indent=4)

def analyze_ferquency(by_wiki, n, file_name=None):

    counter = read_word_counts()
    if counter.total() == 0: print("word_counts.json hasn't been initialized yet")


    # Normalizing counter by dividing by sum of all word
    # (the, a, and) seems to be matched better
    normalized_counter = {}
    for k, v in counter.items():
        normalized_counter[k] = v / counter.total()

    if by_wiki:
        df = pd.DataFrame.from_dict(normalized_counter, orient='index', columns=['Wiki Frequency'])
        df = df.sort_values(by='Wiki Frequency', ascending=False)
        df['Language Frequency'] = df.index.map(lambda word: word_frequency(word, 'en'))
        df.index.name = 'Word'
    else:
        df = pd.DataFrame(top_n_list('en', n), columns=['Word'])
        df.set_index('Word', inplace=True)
        df['Language Frequency'] = df.index.map(lambda word: word_frequency(word, 'en'))
        df['Wiki Frequency'] = df.index.map(lambda word: normalized_counter.get(word, 0))

    pd.options.display.float_format = '{:.6f}'.format
    df = df[['Wiki Frequency', 'Language Frequency']]
    print(df.head(n))
    if file_name is not None:
        frequency_plot(df.head(n), file_name)

def frequency_plot(df, file_name, by_wiki = False):
    ax = df.plot(kind='bar', figsize=(16, 9), width=0.8)

    if by_wiki:
        plt.title("Frequency of some word on "
                  "Minecraft Wiki ordered by appearing on Wiki")
    else:
        plt.title("Frequency of some word on "
                  "Minecraft Wiki ordered by appearing in Spoken language")

    plt.ylabel("Frequency (0,1)")
    plt.xlabel("Word")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.legend()

    plt.savefig(file_name, bbox_inches='tight')

def auto_count(starting_page, wait, depth):
    already_found_links = set()
    start = page.Page(starting_page)
    dfs(start, depth, 0, wait, already_found_links)
