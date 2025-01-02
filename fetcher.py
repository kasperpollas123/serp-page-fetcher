import streamlit as st
import requests
from bs4 import BeautifulSoup

# Oxylabs residential proxy endpoint
PROXY_ENDPOINT = "https://customer-kasperpollas_EImZC-cc-us:L6mFKak8Uz286dC+@pr.oxylabs.io:7777"

# Function to fetch and parse Google SERP
def fetch_google_serp(url):
    try:
        # Set up the proxy
        proxies = {
            "http": PROXY_ENDPOINT,
            "https": PROXY_ENDPOINT,
        }
        
        # Send a GET request to the Google SERP URL through the proxy
        response = requests.get(url, proxies=proxies)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup with the lxml parser
            soup = BeautifulSoup(response.text, 'lxml')
            
            # List to store results
            results = []
            
            # Find all search result containers
            for result in soup.find_all('div', class_='Gx5Zad xpd EtOod pkphOe'):
                # Skip ads (check for ad-related classes or attributes)
                if "ads" in result.get("class", []):  # Example: Skip elements with "ads" in their class list
                    continue
                
                # Extract the title
                title_element = result.find('h3') or result.find('h2')
                title = title_element.get_text() if title_element else "No Title Found"
                
                # Extract the description
                description_element = result.find('div', class_='BNeawe s3v9rd AP7Wnd') or \
                                     result.find('div', class_='v9i61e') or \
                                     result.find('div', class_='BNeawe UPmit AP7Wnd lRVwie')
                description = description_element.get_text() if description_element else "No Description Found"
                
                # Append the result as a dictionary
                results.append({
                    "title": title,
                    "description": description
                })
            
            return results
        else:
            return f"Error: Unable to fetch the page. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("Google SERP Fetcher")

# Input field for the Google SERP URL
serp_url = st.text_input("Enter Google SERP URL (e.g., https://www.google.com/search?q=dog):")

# Button to trigger the fetch
if st.button("Fetch SERP"):
    if serp_url:
        # Fetch the SERP content
        results = fetch_google_serp(serp_url)
        
        # Display the results
        if isinstance(results, list):
            st.subheader("Search Results:")
            for i, result in enumerate(results, start=1):
                st.write(f"**Result {i}**")
                st.write(f"**Title:** {result['title']}")
                st.write(f"**Description:** {result['description']}")
                st.write("---")
        else:
            st.error(results)  # Display error message if any
    else:
        st.warning("Please enter a valid Google SERP URL.")
