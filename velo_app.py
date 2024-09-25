import streamlit as st
import requests
import pandas as pd

# Function to get data from the scraper API running on your VPS
def get_data_from_scraper_api():
    api_url = "http://198.211.96.74:5000/scrape"  # Use your VPS IP address
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch data from the API.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
        return []

# Function to display the final rankings
def display_ranked_data(ranked_data):
    if ranked_data:
        st.subheader("Final Ranked Assets")
        ranked_df = pd.DataFrame(ranked_data, columns=["Asset", "Rank"])
        st.table(ranked_df)  # Display rankings as a table

        # Show bar chart of rankings
        st.subheader("Asset Rankings Visualization")
        st.bar_chart(ranked_df.set_index("Asset"))
    else:
        st.error("No data available")

# Streamlit UI
st.title("🏆 Crypto Leaderboard 🏆")

# Button to trigger the scraping process
if st.button('Find the Leaders'):
    st.write("Checking for the best of the best...")
    ranked_data = get_data_from_scraper_api()
    display_ranked_data(ranked_data)
