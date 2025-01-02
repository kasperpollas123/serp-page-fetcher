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
        
        # Add headers for compression
        headers = {
            "Accept-Encoding": "gzip, deflate"
        }
        
        # Send a GET request to the Google SERP URL through the proxy
        response = requests.get(url, proxies=proxies, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Verify if the response is compressed
            content_encoding = response.headers.get("Content-Encoding", "None")
            st.write(f"**Content-Encoding:** {content_encoding}")
            
            # Use the raw response (proxy has already decompressed it)
            response_text = response.text
            
            # Compare the size of the raw response and decompressed response
            raw_size = len(response.content)  # Size of the raw response (compressed)
            decompressed_size = len(response_text)  # Size of the decompressed response
            st.write(f"**Raw Response Size (Compressed):** {raw_size} bytes")
            st.write(f"**Decompressed Response Size:** {decompressed_size} bytes")
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response_text, 'html.parser')
            
            # List to store results
            results = []
            
            # Find all search result containers
            for result in soup.find_all('div', class_='Gx5Zad xpd EtOod pkphOe'):
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
