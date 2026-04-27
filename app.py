import streamlit as st
import urllib.request
from bs4 import BeautifulSoup


def decode_secret_message(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    rows = soup.find_all('tr')
    
    char_data = []
    max_x = 0
    max_y = 0
    
    # Parse x coordinate, character, and y coordinate
    for row in rows[1:]: 
        cells = row.find_all('td')
        if len(cells) == 3:
            try:
                x = int(cells[0].get_text(strip=True))
                char = cells[1].get_text(strip=True)
                y = int(cells[2].get_text(strip=True))
                
                # Filter out the light background blocks so only the solid text blocks show
                if char != '░': 
                    char_data.append((x, y, char))
                
                if x > max_x: max_x = x
                if y > max_y: max_y = y
            except ValueError:
                continue 
                
    # Initialize the 2D grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Populate the grid
    for x, y, char in char_data:
        grid[y][x] = char
        
    # Convert the grid array into a single multiline string
    result_string = ""
    for row in grid:
        result_string += "".join(row) + "\n"
        
    return result_string


# --- Streamlit Frontend UI ---
st.set_page_config(page_title="Secret Message Decoder", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Google Doc Secret Decoder")
st.markdown("Paste the URL of a published Google Doc containing a 2D coordinate grid to reveal the hidden uppercase message!")

# Create an input box for the URL
url_input = st.text_input("Enter Google Doc URL:")

# Create a button to trigger the script
if st.button("Decode Message", type="primary"):
    if url_input:
        with st.spinner("Decoding the document..."):
            try:
                # Run the decoding function
                secret_message = decode_secret_message(url_input)
                
                # Display success and the message
                st.success("Message successfully decoded!")
                
                # We use st.text() or st.code() here to preserve the fixed-width/monospace spacing
                st.code(secret_message, language="text")
                
            except Exception as e:
                st.error(f"Failed to decode the document. Please check the URL. Error: {e}")
    else:
        st.warning("Please enter a URL before clicking decode.")
