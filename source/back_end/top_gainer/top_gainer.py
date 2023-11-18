# Define paths, get files from current root
import sys, os
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import requests

# API KEY
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
AV_API_KEY = os.environ.get('AV_API_KEY')


class TopGainer():
    
    @staticmethod
    def _get_top_companies_from_api(function, additional_params=None):
        url = "https://www.alphavantage.co/query"
        params = {
            "function": function,
            "apikey": AV_API_KEY
        }
        if additional_params:
            params.update(additional_params)
        
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if not data:
                print(f"No data found")
                return None
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    @staticmethod
    def getTopCompaniesGainer():
        return TopGainer._get_top_companies_from_api('TOP_GAINERS_LOSERS')