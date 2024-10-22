import requests
from bs4 import BeautifulSoup
import json
import re

# Load saved links from the file
with open('scraped_links.txt', 'r') as f:
    links_data = json.load(f)

# Dictionary to store extracted texts
extracted_texts = {}

def extract_text_from_div(div):
    """Recursively extract all text from any tag within the div."""
    text_content = []
    paragraphs = div.find_all('p')
    if not paragraphs:
        return ""
    for p in paragraphs:
        # Use .get_text() to extract text from <p> and all its children
        text_content.append(p.get_text(strip=True))
    return ' '.join(text_content)

def clean_text(text):
    """Clean up the text by removing unwanted characters like &nbsp; and numbers."""
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[�]', '', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

# Iterate through each link and extract information
for link_obj in links_data:
    for key, url in link_obj.items():
        try:
            # Fetch the webpage content
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find the div with class "post-content"
                post_content_div = soup.find('div', class_='post-content')
                
                if post_content_div:
                    # Now look for the div with class "entry-content" inside the "post-content" div
                    entry_content_div = post_content_div.find('div', class_='entry-content')
                    if entry_content_div:
                        # Extract all text from within the div
                        extracted_text = extract_text_from_div(entry_content_div)
                        cleaned_text = clean_text(extracted_text)
                        print("the final cleaned text is: {}".format(cleaned_text))
                        extracted_texts[key] = cleaned_text if cleaned_text else "No content found"
                    else:
                        extracted_texts[key] = "No 'entry-content' div found inside 'post-content'."
                else:
                    extracted_texts[key] = "No 'post-content' div found."

            else:
                extracted_texts[key] = f"Failed to retrieve content. Status code: {response.status_code}"

        except Exception as e:
            extracted_texts[key] = f"Error processing URL: {str(e)}"

# Save the extracted texts to a file
with open('extracted_texts.txt', 'w') as f:
    for key, text in extracted_texts.items():
        f.write(f"{key}: {text}\n")

print("Extraction completed and saved to 'extracted_texts.txt'.")
