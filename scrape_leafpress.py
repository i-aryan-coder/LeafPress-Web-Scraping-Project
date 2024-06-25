import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape the LeafPress website
def scrape_leafpress():
    url = "https://leafpress-final.webflow.io/"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data
    data = {
        "Tagline": [],
        "Description": [],
        "Services": [],
        "Contact Information": []
    }

    # Extract the tagline (using the title of the webpage as an example)
    tagline = soup.title.string if soup.title else 'N/A'

    # Extract the description
    description_tag = soup.find(class_='home-hero_subheading')
    description = description_tag.text if description_tag else 'N/A'

    # Extract services
    services_tags = soup.find_all(class_='exclusive-features_heading-h3')
    services = [service.text for service in services_tags] # Extract text from Tag objects
    for service in services:
        data["Services"].append(service)
        print(service)
    # Extract contact information
    contact_info_tags = soup.find_all('a', class_='footer_link-text')
    for link in contact_info_tags:
      if(link.text=='Linkedin' or link.text=='Twitter'):
        print(link.get('href'))
    # Fill data dictionary
    data["Tagline"].append(tagline)
    data["Description"].append(description)
    data["Services"].append(", ".join(services))  # Join the list of services into a single string
    data["Contact Information"].append("".join(link.get('href')))  # Join the list of contacts into a single string

    data_string = (
        f"Tagline: {data['Tagline']}\n\n"
        f"Description: {data['Description']}\n\n"
        f"Services: {', '.join(data['Services'])}\n\n"
        f"Contact Information: {', '.join(data['Contact Information'])}\n"
    )

    # Write the data to a text file
    with open('company_details.txt', 'w') as file:
        file.write(data_string)

    print("Data has been saved to company_details.txt")

if __name__ == "__main__":
    scrape_leafpress()
