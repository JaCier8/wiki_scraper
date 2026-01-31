# Minecraft Wiki Scraper & Language Analyzer

## Overview
This project is a Python-based tool designed to scrape content from the Minecraft Wiki.
Beyond simple scraping, the application performs advanced text analysis, including extracting data tables,
calculating relative word frequencies, and determining Language Confidence Scores
to identify the language of a given text based on words counting.

## Features

* **Wiki Scraping:** Fetches content from live URLs or local HTML files (offline mode).
* **Table Extraction:** Parses HTML tables into Pandas DataFrames.
* **Word Frequency Analysis:** Compares word usage on Wiki pages against standard English usage frequency.
* **Language Detection:** Implements a "Confidence Score" algorithm to calculate how well a text fits English, German, or Polish based on Top-$k$ frequency lists.
* **Visualization:** Generates bar charts comparing Wiki statistics with natural language statistics using Matplotlib.

How to use every feature is available with 
```bash
python ./wiki_scraper --help
```

## Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/JaCier8/wiki_scraper.git](https://github.com/JaCier8/wiki_scraper.git)
    cd wiki_scraper
    ```

2.  **Create and activate a virtual environment (recommended):**
    * *Linux/macOS:*
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    * *Windows:*
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

3.  **Install dependencies:**
    This project uses a `requirements.txt` file to manage dependencies.
    ```bash
    pip install -r requirements.txt
    ```

