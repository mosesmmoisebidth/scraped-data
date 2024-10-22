import requests
from bs4 import BeautifulSoup
import json

# Website URL to scrape
url = 'https://rw.amateka.net/'

# Send GET request to fetch the webpage
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, 'html.parser')

# Dictionary to store links
scraped_links = []

# Function to extract links from <a> tags within a given <aside> id
def extract_links_from_aside(aside_id):
    aside = soup.find('aside', id=aside_id)
    if aside:
        a_tags = aside.find_all('a')
        for a in a_tags:
            href = a.get('href')
            if href:
                scraped_links.append({"link": href})

# Extract links from the <aside> tag with id "recent-posts-2"
extract_links_from_aside("recent-posts-2")

# Extract links from the <aside> tag with id "pages-2"
extract_links_from_aside("pages-2")

# Save the scraped links to a .txt file in the desired format
with open('scraped_links.txt', 'w') as f:
    json.dump(scraped_links, f, indent=4)

print("Scraping completed and saved to 'scraped_links.txt'.")
