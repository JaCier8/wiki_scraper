from classes import page
import pandas as pd

def get_summary(page):
    print(page.summary)

def nth_table(n, page, csv_name,first_row_is_header=False):
    df_list = page.getTables()
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




page = page.Page("smelting")


get_summary(page)
nth_table(1,page, "nth_table_test",True)
