# Import standard libraries
import json
import os
import sys
import time
import requests
from pathlib import Path

# Import local modules
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Define file and project paths
current_file_path = Path(__file__).resolve()
project_directory = current_file_path.parent.parent
sys.path.append(str(project_directory))

# API keys retrieval
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AV_API_KEY = os.getenv('AV_API_KEY')

def fetch_model_by_name(model_identifier, key):
    """Retrieve a chat model using the model's name and API key."""
    if model_identifier == "openai":
        return ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo")

def convert_to_float(val):
    """Convert a value to float, or return 'N/A' if not possible."""
    return float(val) if val not in [None, "None"] else "N/A"

def generate_insights(insight_name, type_of_data, data, prompt_description, api_key):
    """Generate insights from given data using a specified model."""
    with open("back_end/utilities/prompts/company_insights.prompt", "r") as f:
        template = f.read()
    prompt = PromptTemplate(
        template=template,
        input_variables=["insight_name", "type_of_data", "data", "prompt_description"]
    )

    model = fetch_model_by_name("openai", api_key)
    data = json.dumps(data)
    formatted_input = prompt.format(insight_name=insight_name, type_of_data=type_of_data, data=data, prompt_description=prompt_description)
    return model.predict(formatted_input)

def round_value(value, places=2):
    """Round a value to a given number of decimal places."""
    return round(float(value), places) if isinstance(value, (int, float, str)) and value.replace(".", "", 1).isdigit() else value

def currency_formatting(amount):
    """Format an amount into a readable currency format."""
    if amount == "N/A":
        return amount
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f} billion"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f} million"
    else:
        return f"${amount:.2f}"

def fetch_total_revenue(stock_symbol):
    """Fetch the total revenue for a given stock symbol."""
    time.sleep(3)
    api_url = "https://www.alphavantage.co/query"
    query_params = {
        "function": "INCOME_STATEMENT",
        "symbol": stock_symbol,
        "apikey": AV_API_KEY
    }
    request_response = requests.get(api_url, params=query_params)
    response_data = request_response.json()
    return convert_to_float(response_data["annualReports"][0]["totalRevenue"])

def fetch_total_debt(stock_symbol):
    """Retrieve the total debt for a specified stock symbol."""
    time.sleep(3)
    api_endpoint = "https://www.alphavantage.co/query"
    parameters = {
        "function": "BALANCE_SHEET",
        "symbol": stock_symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(api_endpoint, params=parameters)
    data = response.json()
    short_term_debt = convert_to_float(data["annualReports"][0]["shortTermDebt"])
    time.sleep(3)
    long_term_debt = convert_to_float(data["annualReports"][0]["longTermDebt"])

    return "N/A" if short_term_debt == "N/A" or long_term_debt == "N/A" else short_term_debt + long_term_debt
