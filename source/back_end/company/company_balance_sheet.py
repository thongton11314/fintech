import os
from source.back_end.utilities.utils import generate_insights, fetch_total_revenue, convert_to_float
from source.back_end.company.company_base_api import CompanyAPI
from source.back_end.utilities.field_pydantic import BalanceSheetInsights

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class CompanyBalanceSheet(CompanyAPI):

    def __init__(self, symbol):
        super().__init__(symbol)
        self.metrics = {}
        self.chart_data = {}
        self.insights = {}

    @staticmethod
    def _charts(data):
        report = data['annualReports'][0]
        
        asset_composition = {
            "total_current_assets": report['totalCurrentAssets'],
            "total_non_current_assets": report['totalNonCurrentAssets']              
        }

        liabilities_composition = {
            "total_current_liabilities": report['totalCurrentLiabilities'],
            "total_non_current_liabilities": report['totalNonCurrentLiabilities']
        }

        debt_structure = {
            "short_term_debt": report['shortTermDebt'],
            "long_term_debt": report['longTermDebt']
        }

        return {
            "asset_composition": asset_composition,
            "liabilities_composition": liabilities_composition,
            "debt_structure": debt_structure
        }

    @staticmethod
    def _metrics(data, total_revenue):
        totalCurrentAssets = convert_to_float(data.get("totalCurrentAssets"))
        totalCurrentLiabilities = convert_to_float(data.get("totalCurrentLiabilities"))
        totalLiabilities = convert_to_float(data.get("totalLiabilities"))
        totalShareholderEquity = convert_to_float(data.get("totalShareholderEquity"))
        totalAssets = convert_to_float(data.get("totalAssets"))
        inventory = convert_to_float(data.get("inventory"))

        # Calculating metrics with checks for potential N/A values
        current_ratio = (
            "N/A" if "N/A" in (totalCurrentAssets, totalCurrentLiabilities) else totalCurrentAssets / totalCurrentLiabilities
        )
        debt_to_equity_ratio = (
            "N/A" if "N/A" in (totalLiabilities, totalShareholderEquity) else totalLiabilities / totalShareholderEquity
        )
        quick_ratio = (
            "N/A" if "N/A" in (totalCurrentAssets, totalCurrentLiabilities, inventory) else (totalCurrentAssets - inventory) / totalCurrentLiabilities
        )
        asset_turnover = (
            "N/A" if "N/A" in (total_revenue, totalAssets) else total_revenue / totalAssets
        )
        equity_multiplier = (
            "N/A" if "N/A" in (totalAssets, totalShareholderEquity) else totalAssets / totalShareholderEquity
        )

        return {
            "current_ratio": current_ratio,
            "debt_to_equity_ratio": debt_to_equity_ratio,
            "quick_ratio": quick_ratio,
            "asset_turnover": asset_turnover,
            "equity_multiplier": equity_multiplier,
        }

    def _fetch_balance_sheet_data(self):
        data = self._get_data_from_api("BALANCE_SHEET")
        if not data:
            print(f"No data found for {self.symbol}")
            return None
        return data

    def _generate_insights(self, data_for_insights, fields_to_include, openAI_user_key):
        ins = {}
        
        # Map all fields to the string representation of data_for_insights
        mapped_data = {field: str(data_for_insights) for field in fields_to_include}

        # Create an instance of balance sheet using the mapped data
        blance_sheet_instance = BalanceSheetInsights(**mapped_data)
               
        # Iterate through the fields_to_include
        for field in fields_to_include:
            
            # Extract field description
            field_description = BalanceSheetInsights.__fields__[field].field_info.description
            
            # Use the blance sheet instance directly instead of a string representation
            response = generate_insights(insight_name=field, type_of_data="balance sheet", data=getattr(blance_sheet_instance, field), prompt_description=field_description, api_key=openAI_user_key)
            ins[field] = response

        return ins

    def get_balance_sheet(self, fields_to_include, OPENAI_API_KEY):
        data = self._fetch_balance_sheet_data()
        if not data:
            return

        self.chart_data = self._charts(data)
        report = data["annualReports"][0]
        self.metrics = self._metrics(report, fetch_total_revenue(self.symbol))
        
        data_for_insights = {
            "annual_report_data": report,
            "historical_data": self.chart_data,
        }
        self.insights = self._generate_insights(data_for_insights, fields_to_include, OPENAI_API_KEY)

        return {
            "metrics": self.metrics,
            "chart_data": self.chart_data,
            "insights": self.insights
        }
