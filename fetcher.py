import streamlit as st
import requests

# Oxylabs residential proxy endpoint
PROXY_ENDPOINT = "https://customer-kasperpollas_EImZC-cc-us:L6mFKak8Uz286dC+@pr.oxylabs.io:7777"

# Function to fetch Google SERP using the proxy
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
            return response.text
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
        serp_content = fetch_google_serp(serp_url)
        
        # Display the SERP content
        st.text_area("SERP Content", serp_content, height=300)
    else:
        st.warning("Please enter a valid Google SERP URL.")
