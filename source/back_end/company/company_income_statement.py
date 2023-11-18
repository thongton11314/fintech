from source.back_end.company.company_base_api import CompanyAPI
from source.back_end.utilities.field_pydantic import IncomeStatementInsights
from source.back_end.utilities.utils import generate_insights, convert_to_float

class CompanyIncomeStatement(CompanyAPI):
    
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
        dates = []
        total_revenue = []
        net_income = []
        interest_expense = []

        for report in reversed(data["annualReports"]):
            dates.append(report["fiscalDateEnding"])
            total_revenue.append(report["totalRevenue"])
            net_income.append(report["netIncome"])
            interest_expense.append(report["interestAndDebtExpense"])

        return {
            "dates": dates,
            "total_revenue": total_revenue,
            "net_income": net_income,
            "interest_expense": interest_expense
        }

    @staticmethod
    def _metrics(data):
        # Extract values
        grossProfit = convert_to_float(data.get("grossProfit"))
        totalRevenue = convert_to_float(data.get("totalRevenue"))
        operatingIncome = convert_to_float(data.get("operatingIncome"))
        costOfRevenue = convert_to_float(data.get("costOfRevenue"))
        costofGoodsAndServicesSold = convert_to_float(data.get("costofGoodsAndServicesSold"))
        sellingGeneralAndAdministrative = convert_to_float(data.get("sellingGeneralAndAdministrative"))
        ebit = convert_to_float(data.get("ebit"))
        interestAndDebtExpense = convert_to_float(data.get("interestAndDebtExpense"))
        netIncome = convert_to_float(data.get("netIncome"))

        # Calculate metrics
        gross_profit_margin = CompanyIncomeStatement._safe_divide(grossProfit, totalRevenue)
        operating_profit_margin = CompanyIncomeStatement._safe_divide(operatingIncome, totalRevenue)
        net_profit_margin = CompanyIncomeStatement._safe_divide(netIncome, totalRevenue)
        cost_efficiency = CompanyIncomeStatement._safe_divide(totalRevenue, (costOfRevenue + costofGoodsAndServicesSold))
        sg_and_a_efficiency = CompanyIncomeStatement._safe_divide(totalRevenue, sellingGeneralAndAdministrative)
        interest_coverage_ratio = CompanyIncomeStatement._safe_divide(ebit, interestAndDebtExpense)

        # Returning the results
        return {
            "gross_profit_margin": gross_profit_margin,
            "operating_profit_margin": operating_profit_margin,
            "net_profit_margin": net_profit_margin,
            "cost_efficiency": cost_efficiency,
            "sg_and_a_efficiency": sg_and_a_efficiency,
            "interest_coverage_ratio": interest_coverage_ratio,
        }

    def _fetch_income_statement_data(self):
        data = self._get_data_from_api("INCOME_STATEMENT")
        if not data:
            print(f"No data found for {self.symbol}")
            return None
        return data

    def _generate_insights(self, data_for_insights, fields_to_include, openAI_user_key):
        ins = {}
        
        # Map all fields to the string representation of data_for_insights
        mapped_data = {field: str(data_for_insights) for field in fields_to_include}

        # Create an instance of IncomeStatement using the mapped data
        income_statement_instance = IncomeStatementInsights(**mapped_data)
               
        # Iterate through the fields_to_include
        for field in fields_to_include:
            
            # Extract field description
            field_description = IncomeStatementInsights.__fields__[field].field_info.description
            
            # Use the Income Statement instance directly instead of a string representation
            response = generate_insights(insight_name=field, type_of_data="income statement", data=getattr(income_statement_instance, field), prompt_description=field_description, api_key=openAI_user_key)
            ins[field] = response

        return ins

    def get_income_statement(self, fields_to_include, openAI_user_key):
        data = self._fetch_income_statement_data()
        if not data:
            return
        self.chart_data = self._charts(data)
        report = data["annualReports"][0]
        self.metrics = self._metrics(report)

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
