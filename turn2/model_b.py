import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_guidelines(base_url):
    guidelines = []
    page_num = 1
    while True:
        url = f'{base_url}?page={page_num}'
        print(f"Scraping guidelines from {url}")
        response = requests.get(url)
        if response.status_code == 404:
            # If the page doesn't exist, we've reached the last page
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        guideline_elements = soup.select('.guideline-item')
        for element in guideline_elements:
            title = element.select_one('.guideline-title').text.strip()
            description = element.select_one('.guideline-description').text.strip()
            source = element.select_one('.guideline-source').text.strip()
            guidelines.append({
                "Title": title,
                "Description": description,
                "Source": source
            })
        page_num += 1
    return guidelines


if __name__ == "__main__":
    base_url = "http://example.com/pediatric-guidelines/"  # Replace with the actual base URL
    all_guidelines = scrape_guidelines(base_url)

    guideline_df = pd.DataFrame(all_guidelines)
    print("Guidelines Extracted:")
    print(guideline_df)

    guideline_df.to_csv("pediatric_clinical_guidelines.csv", index=False)
    print("Guidelines saved to CSV file!")
