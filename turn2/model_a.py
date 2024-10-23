import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_guidelines(base_url):
	all_guidelines = []
	next_page_url = base_url

	while next_page_url:
		try:
			response = requests.get(next_page_url)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			print(f"Error occurred: {e}")
			break

		soup = BeautifulSoup(response.text, 'html.parser')
		guideline_elements = soup.select('.guideline-item')

		for element in guideline_elements:
			title = element.select_one('.guideline-title').text.strip()
			description = element.select_one('.guideline-description').text.strip()
			source = element.select_one('.guideline-source').text.strip()
			all_guidelines.append({
				"Title": title,
				"Description": description,
				"Source": source
			})

		# Find the URL of the next page
		next_page_elem = soup.select_one('.pagination .next a')
		next_page_url = next_page_elem['href'] if next_page_elem else None

	return all_guidelines


if __name__ == "__main__":
	base_url = "http://example.com/pediatric-guidelines/"

	guidelines = scrape_guidelines(base_url)

	# Create a DataFrame to store the guidelines
	guideline_df = pd.DataFrame(guidelines)
	print("Guidelines Extracted:")
	print(guideline_df)

	guideline_df.to_csv("pediatric_clinical_guidelines.csv", index=False)
	print("Guidelines saved to CSV file!")
