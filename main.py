import json
import os
from collections import Counter

from classes import page
import pandas as pd

def get_summary(page):
    print(page.summary)

def nth_table(n, page, csv_name,first_row_is_header=False):
    df_list = page.get_tables()
    if len(df_list) < n:
        print(n, "is exceeding number of tables on site")

    df = df_list[n-1]
    df.to_csv("csv_name.csv")

    # If someone wanted for whole records not words then comment split and explode!!
    # Smelting is a cool test

    #TODO maybe do something with parenthesis example: (1, smelting)
    words = (
        pd.Series(df.values.flatten()) # Flattening whole data frame to 1 column with everything
        .str.split() # Splitting records from sentences words to words
        .explode()  # Making each word q unique record in our list
        .value_counts() # Ready to use pandas func to count words
        .reset_index() # Reindexing
    )

    words.columns = ["Word", "Count"]

    print(words)

def word_counter(page):

    # Get counter from page class
    counter = page.get_counter()

    # Finding if word_counter already exists, and we create or modify one
    if os.path.exists('word_counts.json'):
        with open('word_counts.json', 'r', encoding='utf-8') as f:
            old_json = json.load(f)
            old_counter = Counter(old_json)
    else:
        old_counter = Counter()

    old_counter.update(counter)

    with open('word_counts.json', 'w', encoding='utf-8') as f:
        json.dump(old_counter, f, ensure_ascii=False, indent=4)




page = page.Page("enchantingdawjdaiwo")


get_summary(page)
nth_table(1,page, "nth_table_test",True)
word_counter(page)
