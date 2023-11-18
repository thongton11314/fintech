
# Define paths, get files from current root
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

# Import needed libraries, functions
from source.back_end.utilities.utils import convert_to_float, currency_formatting

# company_overview.py
from source.back_end.company.company_base_api import CompanyAPI

class CompanyOverview(CompanyAPI):
    
    def get_company_overview(self):
        data = self._get_data_from_api("OVERVIEW")
        if not data:
            return None

        # Extract relevant details from the data
        extracted_data = {
            "Symbol": data.get("Symbol"),
            "AssetType": data.get("AssetType"),
            "Name": data.get("Name"),
            "Description": data.get("Description"),
            "CIK": data.get("CIK"),
            "Exchange": data.get("Exchange"),
            "Currency": data.get("Currency"),
            "Country": data.get("Country"),
            "Sector": data.get("Sector"),
            "Industry": data.get("Industry"),
            "Address": data.get("Address"),
            "FiscalYearEnd": data.get("FiscalYearEnd"),
            "LatestQuarter": data.get("LatestQuarter"),
            "MarketCapitalization": currency_formatting(convert_to_float(data.get("MarketCapitalization"))),
        }
        return extracted_data
