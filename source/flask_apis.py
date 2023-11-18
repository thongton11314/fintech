# Define paths, get files from current root
import sys, os
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

# Flask APIs
from flask import Flask, request, jsonify
from flask_cors import CORS
from source.back_end.company.company_information_factory import CompanyInformationFactory
from source.back_end.top_gainer.top_gainer import TopGainer

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
AV_API_KEY = os.environ.get('AV_API_KEY')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/company_overview', methods=['POST'])
def get_company_overview():
    # Obtain JSON data from the request
    data = request.get_json()

    # Extract the 'symbol' value from the data
    symbol = data.get('symbol')

    # Check if 'symbol' is provided; if not, return an error
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400  # HTTP status code 400 for 'Bad Request'

    # Create a company information object and get the company overview
    overview_data = CompanyInformationFactory.create_overview(symbol=symbol).get_company_overview()

    # Check if the company overview retrieval was successful; if not, return an error
    if overview_data is None:
        return jsonify({'error': 'Unable to retrieve company overview'}), 500  # HTTP status code 500 for 'Internal Server Error'

    # If successful, return the company overview data as JSON
    return jsonify(overview_data)


@app.route('/income_statement', methods=['POST'])
def get_income_statement():
    # Extracting the JSON data from the request
    data = request.get_json()

    # Extracting the 'symbol' and 'fields_to_include' values from the data
    symbol = data.get('symbol')
    fields_to_include = data.get(
        'fields_to_include',
        [
            'revenue_health',
            'operational_efficiency',
            'r_and_d_focus',
            'debt_management',
            'profit_retention'
        ]  # Assuming 'fields_to_include' is optional with a default value
    )

    # Checking if 'symbol' is provided; if not, returning an error
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400  # HTTP status code 400 for 'Bad Request'

    # Creating a company information object and getting the income statement data
    income_statement_data = CompanyInformationFactory.create_income_statement(symbol=symbol).get_income_statement(fields_to_include, OPENAI_API_KEY)

    # Checking if the income statement data retrieval was successful; if not, returning an error
    if income_statement_data is None:
        return jsonify({'error': 'Unable to retrieve income statement data'}), 500  # HTTP status code 500 for 'Internal Server Error'

    # If successful, returning the income statement data as JSON
    return jsonify(income_statement_data)


@app.route('/balance_sheet', methods=['POST'])
def get_balance_sheet():
    # Extracting the JSON data from the request
    data = request.get_json()

    # Extracting the 'symbol' value from the data
    symbol = data.get('symbol')

    # Extracting or assigning default values for 'fields_to_include' from the data
    fields_to_include = data.get(
        'fields_to_include',
        [
            'liquidity_position',
            'assets_efficiency',
            'capital_structure',
            'inventory_management',
            'overall_solvency',
            'operational_efficiency',
        ]
    )

    # Checking if 'symbol' is provided; if not, returning an error
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400  # HTTP status code 400 for 'Bad Request'

    # Creating a company information object and getting the balance sheet data
    balance_sheet_data = CompanyInformationFactory.create_balance_sheet(symbol=symbol).get_balance_sheet(fields_to_include, OPENAI_API_KEY)

    # Checking if the balance sheet data retrieval was successful; if not, returning an error
    if balance_sheet_data is None:
        return jsonify({'error': 'Unable to retrieve balance sheet data'}), 500  # HTTP status code 500 for 'Internal Server Error'

    # If successful, returning the balance sheet data as JSON
    return jsonify(balance_sheet_data)

    
@app.route('/cash_flow', methods=['POST'])
def get_cash_flow():
    # Extracting the JSON data from the request
    data = request.get_json()

    # Extracting the 'symbol' value from the data
    symbol = data.get('symbol')

    # Extracting or assigning default values for 'fields_to_include' from the data
    fields_to_include = data.get(
        'fields_to_include',
        [
            "operational_cash_efficiency",
            "investment_capability",
            "financial_flexibility",
            "dividend_sustainability",
            "debt_service_capability"
        ]
    )

    # Checking if 'symbol' is provided; if not, returning an error
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400  # HTTP status code 400 for 'Bad Request'

    # Creating a company information object and getting the cash flow data
    cash_flow_data = CompanyInformationFactory.create_cash_flow(symbol=symbol).get_cash_flow(fields_to_include, OPENAI_API_KEY)

    # Checking if the cash flow data retrieval was successful; if not, returning an error
    if cash_flow_data is None:
        return jsonify({'error': 'Unable to retrieve cash flow data'}), 500  # HTTP status code 500 for 'Internal Server Error'

    # If successful, returning the cash flow data as JSON
    return jsonify(cash_flow_data)

    
@app.route('/new_sentiment', methods=['POST'])
def get_new_sentiment():
    # Extracting the JSON data from the request
    data = request.get_json()

    # Extracting the 'symbol' and 'max_feed' values from the data
    symbol = data.get('symbol')
    max_feed = data.get('max_feed', 10)  # Assuming a default of 10 if max_feed is not provided

    # Checking if 'symbol' is provided; if not, returning an error
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400  # HTTP status code 400 for 'Bad Request'

    # Creating a company information object and getting the sentiment data
    sentiment_data = CompanyInformationFactory.create_sentiment(symbol=symbol).get_sentiment()

    # Checking if the sentiment data retrieval was successful; if not, returning an error
    if sentiment_data is None:
        return jsonify({'error': 'Unable to retrieve sentiment data'}), 500  # HTTP status code 500 for 'Internal Server Error'

    # Converting the news DataFrame to a list of dictionaries
    news_dict = sentiment_data['news'].to_dict(orient='records')

    # Updating sentiment_data to replace the DataFrame with the list of dictionaries
    sentiment_data['news'] = news_dict

    # Returning the sentiment data as JSON
    return jsonify(sentiment_data)

@app.route('/get_top_companies_gain_lose', methods=['GET'])
def get_top_companies_gain_lose():
    data = TopGainer.getTopCompaniesGainer()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No data found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)

