import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    results = []

    # List of substrings
    target_vulns = [
        "Broken Access Control",
        "Cryptographic Failures",
        "Injection",
        "Insecure Design",
        "Security Misconfiguration",
        "Vulnerable and Outdated Components",
        "Identification and Authentication Failures",
        "Software and Data Integrity Failures",
        "Security Logging and Monitoring Failures",
        "Server-Side Request Forgery"
    ]

    try:
        # 1. Use Correct URL (The List Page)
        url = "https://owasp.org/Top10/"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(5)

        # 2. Get all links
        print("Scanning all links on the page...")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        
        seen_titles = set()

        for link in all_links:
            try:
                # textContent to get hidden/nested text
                # clean  up
                raw_text = link.get_attribute("textContent")
                if not raw_text:
                    continue
                
                text_clean = " ".join(raw_text.split())
                href = link.get_attribute("href")

                # 3. Check target vulnerability inside this link text
                for vuln in target_vulns:
                    # Case-insensitive check
                    if vuln.lower() in text_clean.lower():
                        
                        # Use clean text as title 
                        if text_clean not in seen_titles:
                            seen_titles.add(text_clean)
                            
                            entry = {
                                "Vulnerability Title": text_clean,
                                "Link": href
                            }
                            results.append(entry)
                            print(f" [MATCH] {vuln}")
                        break 

            except Exception:
                continue

        # 4. Write CSV
        if results:
            print(f"\nSuccess! Found {len(results)} items.")
            
            csv_filename = "owasp_top_10.csv"
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Vulnerability Title", "Link"])
                writer.writeheader()
                writer.writerows(results)
            print(f"Saved to {csv_filename}")
        else:
            print("\nStill 0 results. This is very strange.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()