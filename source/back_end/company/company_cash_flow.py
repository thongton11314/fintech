from source.back_end.company.company_base_api import CompanyAPI
from source.back_end.utilities.utils import generate_insights, fetch_total_revenue, fetch_total_debt, convert_to_float
from source.back_end.utilities.field_pydantic import CashFlowInsights

class CompanyCashFlow(CompanyAPI):

    def __init__(self, symbol):
        super().__init__(symbol)
        self.metrics = {}
        self.chart_data = {}
        self.insights = {}

    @staticmethod
    def _safe_divide(numerator, denominator):
        if "N/A" in (numerator, denominator) or denominator == 0:
            return "N/A"
        return numerator / denominator

    @staticmethod
    def _charts(data):
        dates, operating_cash_flow, cash_flow_from_investment, cash_flow_from_financing = [], [], [], []

        for report in reversed(data["annualReports"]):
            dates.append(report["fiscalDateEnding"])
            operating_cash_flow.append(report["operatingCashflow"])
            cash_flow_from_investment.append(report["cashflowFromInvestment"])
            cash_flow_from_financing.append(report["cashflowFromFinancing"])

        return {
            "dates": dates,
            "operating_cash_flow": operating_cash_flow,
            "cash_flow_from_investment": cash_flow_from_investment,
            "cash_flow_from_financing": cash_flow_from_financing
        }

    @staticmethod
    def _metrics(data, total_revenue, total_debt):
        operatingCashFlow = convert_to_float(data.get("operatingCashflow"))
        capitalExpenditures = convert_to_float(data.get("capitalExpenditures"))
        dividendPayout = convert_to_float(data.get("dividendPayout"))
        netIncome = convert_to_float(data.get("netIncome"))

        operating_cash_flow_margin = CompanyCashFlow._safe_divide(operatingCashFlow, total_revenue)
        capital_expenditure_coverage_ratio = CompanyCashFlow._safe_divide(operatingCashFlow, capitalExpenditures)
        free_cash_flow = operatingCashFlow - capitalExpenditures
        dividend_coverage_ratio = CompanyCashFlow._safe_divide(netIncome, dividendPayout)
        cash_flow_to_debt_ratio = CompanyCashFlow._safe_divide(operatingCashFlow, total_debt)

        return {
            "operating_cash_flow_margin": operating_cash_flow_margin,
            "capital_expenditure_coverage_ratio": capital_expenditure_coverage_ratio,
            "free_cash_flow": free_cash_flow,
            "dividend_coverage_ratio": dividend_coverage_ratio,
            "cash_flow_to_debt_ratio": cash_flow_to_debt_ratio
        }

    def _fetch_cash_flow_data(self):
        data = self._get_data_from_api("CASH_FLOW")
        if not data:
            print(f"No data found for {self.symbol}")
            return None
        return data

    def _generate_insights(self, data_for_insights, fields_to_include, openAI_user_key):
        ins = {}
        
        # Map all fields to the string representation of data_for_insights
        mapped_data = {field: str(data_for_insights) for field in fields_to_include}

        # Create an instance of cash flow using the mapped data
        cash_flow_instance = CashFlowInsights(**mapped_data)
               
        # Iterate through the fields_to_include
        for field in fields_to_include:
            
            # Extract field description
            field_description = CashFlowInsights.__fields__[field].field_info.description
            
            # Use the cash flow instance directly instead of a string representation
            response = generate_insights(insight_name=field, type_of_data="cash flow", data=getattr(cash_flow_instance, field), prompt_description=field_description, api_key=openAI_user_key)
            ins[field] = response

        return ins

    def get_cash_flow(self, fields_to_include, openAI_user_key):
        data = self._fetch_cash_flow_data()
        if not data:
            return

        self.chart_data = self._charts(data)
        report = data["annualReports"][0]
        total_revenue = fetch_total_revenue(self.symbol) 
        total_debt = fetch_total_debt(self.symbol)
        self.metrics = self._metrics(report, total_revenue, total_debt)

        data_for_insights = {
            "annual_report_data": report,
            "historical_data": self.chart_data,
        }
        self.insights = self._generate_insights(data_for_insights, fields_to_include, openAI_user_key)

        return {
            "metrics": self.metrics,
            "chart_data": self.chart_data,
            "insights": self.insights
        }