import pandas as pd
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def main():
    # 1. Setup Selenium Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    results = []

    try:
        # 2. Load the web page
        url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
        print(f"Loading {url}...")
        driver.get(url)

        # Wait for content to load
        time.sleep(5)

        # 3. Find all 'li' elements for search results
        print("Finding book entries...")
        book_elements = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
        
        print(f"Found {len(book_elements)} books. Extracting data...")

        # Main loop: Iterate through the list of li entries
        for book in book_elements:
            try:
                # --- Get Title ---
                title_element = book.find_element(By.CLASS_NAME, "title-content")
                title_text = title_element.text

                # --- Get Authors ---
                author_elements = book.find_elements(By.CLASS_NAME, "author-link")
                author_names = [auth.text for auth in author_elements]
                author_text = "; ".join(author_names)

                # --- Get Format and Year ---
                format_div = book.find_element(By.CLASS_NAME, "cp-format-info")
                format_span = format_div.find_element(By.CLASS_NAME, "display-info-primary")
                format_text = format_span.text

                # Create the dictionary
                book_dict = {
                    "Title": title_text,
                    "Author": author_text,
                    "Format-Year": format_text
                }

                results.append(book_dict)

            except Exception as e:
                print(f"Skipping an item due to error: {e}")
                continue

        # 4. Create DataFrame
        df = pd.DataFrame(results)
        
        # Print to console
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print("\n--- Search Results ---")
        print(df)

        # --- TASK 4: Write to Files ---
        
        # Write to CSV
        print("\nWriting to get_books.csv...")
        df.to_csv("get_books.csv", index=False)
        
        # Write to JSON
        print("Writing to get_books.json...")
        with open("get_books.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        print("Done!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()