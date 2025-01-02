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
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the title of the page
            title = soup.title.string if soup.title else "No Title Found"
            
            # Extract descriptions (meta descriptions or snippets from search results)
            descriptions = []
            # Google SERP descriptions are often in <div> tags with specific classes
            for desc in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
                descriptions.append(desc.get_text())
            
            return title, descriptions
        else:
            return f"Error: Unable to fetch the page. Status code: {response.status_code}", []
    except Exception as e:
        return f"An error occurred: {e}", []

# Streamlit UI
st.title("Google SERP Fetcher")

# Input field for the Google SERP URL
serp_url = st.text_input("Enter Google SERP URL (e.g., https://www.google.com/search?q=dog):")

# Button to trigger the fetch
if st.button("Fetch SERP"):
    if serp_url:
        # Fetch the SERP content
        title, descriptions = fetch_google_serp(serp_url)
        
        # Display the title
        st.subheader("Title:")
        st.write(title)
        
        # Display the descriptions
        st.subheader("Descriptions:")
        for desc in descriptions:
            st.write(desc)
    else:
        st.warning("Please enter a valid Google SERP URL.")
