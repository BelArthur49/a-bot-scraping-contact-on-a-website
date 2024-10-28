import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://www.soho.fitness/"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a dictionary to store the contact information
    contact_info = {}

    # Extracting email
    email = soup.find('a', href=lambda href: href and "mailto:" in href)
    if email:
        contact_info['Email'] = email.get_text(strip=True)

    # Extracting phone number (check for "tel:" in href attribute)
    phone = soup.find('a', href=lambda href: href and "tel:" in href)
    if phone:
        contact_info['Phone'] = phone.get_text(strip=True)

    # Extracting address (manually search for common address tags like <address> or <p>)
    address = soup.find('address')
    if not address:
        # If <address> tag is not found, look for possible address in <p> tags
        address = soup.find('p', string=lambda text: text and any(word in text.lower() for word in ['street', 'st.', 'ave', 'road', 'rd', 'suite']))
    
    if address:
        contact_info['Address'] = address.get_text(strip=True)

    # Print the extracted contact information
    print("Contact Information:")
    for key, value in contact_info.items():
        print(f"{key}: {value}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
