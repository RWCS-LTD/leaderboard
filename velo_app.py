import streamlit as st
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Initialize WebDriver for Chrome in headless mode
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Required if running as root on Linux
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    driver = webdriver.Chrome(options=options)
    return driver

# Function to select the timeframe from dropdown using clicks down
def select_timeframe(driver, clicks_down):
    dropdown_xpath = '//*[@id="spaghettiChart-panel"]/div[1]/div[2]/div[2]/button'
    dropdown_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
    dropdown_menu.click()

    actions = ActionChains(driver)
    for _ in range(clicks_down):
        actions.send_keys('\ue015').perform()  # Simulate the down arrow key
        time.sleep(1)
    actions.send_keys('\ue007').perform()  # Press Enter to select the option
    time.sleep(5)

# Function to scrape only the first 10 assets and filter out non-asset terms
def scrape_top_gainers(driver):
    chart_xpath = '//*[@id="spaghettiChart-panel"]/div[2]'
    try:
        chart = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, chart_xpath)))
        gainers = chart.text.splitlines()
        valid_gainers = [line for line in gainers[:10] if 'Price' not in line and not line.isdigit()]  # Filter out non-assets
        return valid_gainers
    except Exception as e:
        st.write(f"Error loading chart: {e}")
        return []

# Scrape data for 1W, 4H, 1D, and 1M
def scrape_data(driver):
    url = "https://velo.xyz/market"
    driver.get(url)
    
    timeframes_data = {}

    # Scraping 1W (default, no dropdown interaction)
    time.sleep(5)  # Allow time for the page to fully load 1W
    timeframes_data['1W'] = scrape_top_gainers(driver)
    st.write("1W Top Gainers:", timeframes_data['1W'])  # Display top gainers for 1W timeframe

    # Scraping 4H (2 clicks down)
    select_timeframe(driver, 2)
    timeframes_data['4H'] = scrape_top_gainers(driver)
    st.write("4H Top Gainers:", timeframes_data['4H'])  # Display top gainers for 4H timeframe

    # Scraping 1D (3 clicks down)
    select_timeframe(driver, 3)
    timeframes_data['1D'] = scrape_top_gainers(driver)
    st.write("1D Top Gainers:", timeframes_data['1D'])  # Display top gainers for 1D timeframe

    # Scraping 2W (5 clicks down)
    select_timeframe(driver, 5)
    timeframes_data['2W'] = scrape_top_gainers(driver)
    st.write("2W Top Gainers:", timeframes_data['2W'])  # Display top gainers for 2W timeframe

    return timeframes_data

# Rank assets by their cumulative rank across timeframes and assign rank positions
def rank_assets(timeframes_data):
    asset_ranks = {}

    # Track the ranks of assets across different timeframes
    for timeframe, gainers in timeframes_data.items():
        for rank, asset in enumerate(gainers, start=1):
            if asset not in asset_ranks:
                asset_ranks[asset] = {'count': 0, 'total_rank': 0}

            asset_ranks[asset]['count'] += 1
            asset_ranks[asset]['total_rank'] += rank

    # Split assets into two categories: exactly 3-4 timeframes, and exactly 2 timeframes
    ranked_assets_3_4 = [(asset, data['count'], data['total_rank'] / data['count'])
                         for asset, data in asset_ranks.items() if 3 <= data['count'] <= 4]
    ranked_assets_2 = [(asset, data['count'], data['total_rank'] / data['count'])
                       for asset, data in asset_ranks.items() if data['count'] == 2]

    # Sort by average rank
    ranked_assets_3_4_sorted = sorted(ranked_assets_3_4, key=lambda x: x[2])
    ranked_assets_2_sorted = sorted(ranked_assets_2, key=lambda x: x[2])

    # Combine both rankings into a single list
    merged_ranking = ranked_assets_3_4_sorted + ranked_assets_2_sorted

    # Assign a unique rank to each asset across both lists
    merged_ranked_assets_with_positions = [(asset[0], i + 1) for i, asset in enumerate(merged_ranking)]

    return merged_ranked_assets_with_positions

# Main app functionality
def main():
    st.title("📈⭐️ Crypto Leaderboard ⭐️📈")

    if st.button("Rank 🏆 Button"):
        driver = setup_driver()

        # Scrape data
        timeframes_data = scrape_data(driver)
        merged_ranked_assets = rank_assets(timeframes_data)

        st.subheader("Top Performing Assets🚀🔥💎 ")
        for asset, rank in merged_ranked_assets:
            st.write(f"{rank}. {asset}")

        driver.quit()

if __name__ == "__main__":
    main()
