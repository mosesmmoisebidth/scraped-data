import requests
from bs4 import BeautifulSoup
import json

# Base URL for the first page (without pagination)
first_url = "https://imvahonshya.co.rw/category/amakuru/"

# Base URL for pagination (from page 2 onward)
base_url = "https://imvahonshya.co.rw/category/amakuru/page/"

# List to store the extracted links in the desired format
all_links = []

# Function to extract links from a given URL
def extract_links(url, link_counter):
    response = requests.get(url, verify=False)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all divs with the class "news-card-info"
        divs = soup.find_all('div', class_='news-card-info')

        for div in divs:
            # Find the h3 tag within the div
            h3_tag = div.find('h3')
            
            if h3_tag:
                # Find the <a> tag inside the <h3> and get the href attribute
                a_tag = h3_tag.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    link = a_tag['href']
                    # Store the link in the dictionary format
                    all_links.append({f"link{link_counter}": link})
                    link_counter += 1
    else:
        print(f"Failed to retrieve page {url}. Status code: {response.status_code}")
    
    return link_counter

# Counter for tracking the link number
link_counter = 1

# First, extract links from the main page (without pagination)
link_counter = extract_links(first_url, link_counter)

# Then, loop over all paginated pages (from page 1 to 37)
for page_num in range(2, 196):
    # Construct the URL for each paginated page
    url = f"{base_url}{page_num}"
    
    # Extract links from each paginated page
    link_counter = extract_links(url, link_counter)

# Remove duplicates by creating a dictionary with the link as the key
unique_links = {}
for link_dict in all_links:
    for key, value in link_dict.items():
        unique_links[value] = key  # Use link as the key, keeping the first occurrence of the link

# Convert the unique links back to the desired format
cleaned_links = [{unique_links[link]: link} for link in unique_links]

# Save the final list of unique links to a text file
with open('cleaned_extracted_links.txt', 'w') as file:
    json.dump(cleaned_links, file, indent=4)

# Print a message confirming the saving process
print("Duplicates have been removed and links saved to cleaned_extracted_links.txt")
