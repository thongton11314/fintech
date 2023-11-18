import sys, os
from pathlib import Path
import requests

script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

AV_API_KEY = os.environ.get('AV_API_KEY')

class CompanyAPI:

    def __init__(self, symbol):
        self.symbol = symbol
    
    def _get_data_from_api(self, function, additional_params=None):
        url = "https://www.alphavantage.co/query"
        params = {
            "function": function,
            "symbol": self.symbol,
            "apikey": AV_API_KEY
        }
        if additional_params:
            params.update(additional_params)
        
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if not data:
                print(f"No data found for {self.symbol}")
                return None
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None