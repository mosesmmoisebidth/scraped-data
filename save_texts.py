import requests
from bs4 import BeautifulSoup
import json
import re

# Load links from a .txt file
path_to_links = "imvaho_nshya_archives/cleaned_extracted_ubuzima_links.txt"
with open(path_to_links, 'r') as f:
    links_data = json.load(f)

# Dictionary to store extracted texts
extracted_texts = {}

def extract_text_from_div(div):
    """Recursively extract text from a given div."""
    # Check if the div has <p> tags
    paragraphs = div.find_all('p')
    if not paragraphs:
        return ""

    # Collect all text from <p> and their inner tags
    text_content = []
    for p in paragraphs:
        # Use .get_text() to extract text from <p> and all its children
        text_content.append(p.get_text(strip=True))
    return ' '.join(text_content)

def clean_text(text):
    """Clean up the text by removing unwanted characters."""
    # Replace unwanted characters (e.g., �) with an empty string or a space
    text = re.sub(r'[�]', '', text)  # Remove the specific character
    # You can add more replacements if needed
    # Remove any other unwanted characters, if necessary
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Replace non-ASCII characters with a space
    return text.strip()

# Iterate through each link object in the list
for link_obj in links_data:
    for key, url in link_obj.items():
        try:
            # Fetch webpage content
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Find all divs with class 'news-para'
                news_para_divs = soup.find_all('div', class_='news-para')
                print("the news_para_divs are: {}".format(news_para_divs))
                
                # Initialize extracted text for the current link
                extracted_text = ""

                # Iterate through all found news-para divs
                for news_para_div in news_para_divs:
                    # Extract text from each news-para div
                    extracted_text += extract_text_from_div(news_para_div) + " "
                
                # Clean the collected text
                cleaned_text = clean_text(extracted_text)
                print("the cleaned_text is: {}".format(cleaned_text))

                # Save the cleaned text
                extracted_texts[key] = cleaned_text if cleaned_text else "No relevant text found."

            else:
                extracted_texts[key] = f"Failed to retrieve content. Status code: {response.status_code}"
    
        except Exception as e:
            extracted_texts[key] = f"Error processing URL: {str(e)}"

# Save the extracted_texts dictionary to a .txt file
with open('extracted_texts_ubuzima.txt', 'w') as f:
    for key, text in extracted_texts.items():
        f.write(f"{key}: {text}\n")

print("Extraction completed and saved to 'extracted_texts.txt'.")
