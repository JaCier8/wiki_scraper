import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from classes.page import Page

"""
Integration test, for summary functionality
"""

def run_integration_test():
    filename = "test_html.html"

    expected_text = (
        "Smelting is the process of obtaining refined goods from raw materials by heating "
        "them in a furnace, blast furnace or smoker. "
        "When items are smelted in either type of furnace, "
        "experience is dropped. Like crafting, smelting uses recipes "
        "to determine what item is produced."
    )

    page = Page("Smelting", local_file=filename)

    actual_summary = page.summary.strip()
    expected_summary = expected_text.strip()

    if actual_summary != expected_summary:
        print(f"Summary different from expected: {expected_summary} \nActual: {actual_summary}")
        sys.exit(1)
    else:
        print(f"Summary equal to expected: {expected_summary} \nActual: {actual_summary}")

if __name__ == "__main__":
    run_integration_test()