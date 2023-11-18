import sys
from pathlib import Path
import csv
import requests
import streamlit as st

# Define paths
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

# API Token
API_TOKEN = st.secrets["eod_api_key"]

def get_ticker_symbol(company_name):
    """Fetch ticker symbol for the given company name from CSV file."""
    with open("data/ticker_symbols/ticker_symbols.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == company_name:
                return row['Code']
    return None

def get_all_company_names():
    """Retrieve all company names listed as 'Common Stock' from CSV file."""
    company_names = []
    with open("data/ticker_symbols/ticker_symbols.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Type'] == "Common Stock":
                company_names.append(row['Name'])
    return tuple(company_names)

def get_symbols_for_exchange(exchange_code, api_token):
    """Fetch symbols for a given exchange using EOD Historical Data API."""
    base_url = "https://eodhd.com/api/exchange-symbol-list/"
    url = f"{base_url}{exchange_code}/"
    params = {
        "api_token": api_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            # Handle unexpected response format
            print("Received unexpected response:")
            print(response.text)
            with open("data/ticker_symbols/ticker_symbols.txt", "w") as f:
                f.write(response.text)
            with open("data/ticker_symbols/ticker_symbols.csv", "w") as f:
                f.write(response.text)
            return None
    else:
        response.raise_for_status()

if __name__ == "__main__":
    # Test fetching symbols for specified exchanges
    EXCHANGE_CODES = ['NYSE', 'NASDAQ']
    for code in EXCHANGE_CODES:
        try:
            data = get_symbols_for_exchange(code, API_TOKEN)
            print(data)
        except requests.RequestException as e:
            print(f"Error occurred: {e}")
