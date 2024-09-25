import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Streamlit application title
st.title('Crypto Asset Scraper and Ranker')

# Function to scrape data using BeautifulSoup and requests
def scrape_data():
    url = "https://example-crypto-website.com/market"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Sample logic to extract top gainers (Modify selectors as per website structure)
        assets = []
        rows = soup.select('div.asset-row')  # Adjust selector based on the actual page
        for row in rows[:10]:
            asset_name = row.select_one('.asset-name').text.strip()
            assets.append(asset_name)
        
        return assets
    else:
        st.error("Failed to retrieve data.")
        return []

# Rank assets (Example with basic logic)
def rank_assets(assets):
    # For simplicity, assign random ranks (You can add your own ranking logic here)
    ranked_assets = [(asset, rank + 1) for rank, asset in enumerate(assets)]
    return ranked_assets

# Function to display data nicely in the app
def display_data(assets, ranked_assets):
    st.subheader("Scraped Data (Top Gainers)")
    st.table(pd.DataFrame(assets, columns=["Top Gainers"]))

    st.subheader("Ranked Assets")
    ranked_df = pd.DataFrame(ranked_assets, columns=["Asset", "Rank"])
    st.table(ranked_df)

    st.subheader("Asset Ranking Visualization")
    st.bar_chart(ranked_df.set_index("Asset"))

# Streamlit UI to run the scraper
if st.button('Run Scraper'):
    st.write('Starting the scraping process...')
    
    # Scrape data
    assets = scrape_data()

    if assets:
        # Rank assets and display
        ranked_assets = rank_assets(assets)
        display_data(assets, ranked_assets)
else:
    st.write('Click the button to run the scraper.')
