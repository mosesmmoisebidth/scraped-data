import json

# Load the links from the file
with open('scraped_links.txt', 'r') as f:
    links_data = json.load(f)

# List to store renumbered links in the desired format
renumbered_links = []

# Renumber the links
for index, link in enumerate(links_data, start=1):
    renumbered_links.append({f"link{index}": link['link']})

# Save the renumbered links back to the file in the specified format
with open('scraped_links.txt', 'w') as f:
    json.dump(renumbered_links, f, indent=4)

print("Links have been renumbered and saved in the specified format.")
