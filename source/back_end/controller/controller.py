# Define paths, get files from current root
import sys, os
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from source.back_end.company.company_information_factory import CompanyInformationFactory

class CompanyController:
       
    def __init__(self, symbol : str):
        self.symbol = symbol
        self.companyOverview = CompanyInformationFactory.create_overview(symbol)
        self.companyIncomeStatement = CompanyInformationFactory.create_income_statement(symbol)
        self.companyBalanceSheet = CompanyInformationFactory.create_balance_sheet(symbol)
        self.companyCashFlow = CompanyInformationFactory.create_cash_flow(symbol)
        self.companySentiment = CompanyInformationFactory.create_sentiment(symbol)
    
    def get_symbol(self):
        """
        Return a company symbol
        """
        return self.symbol

    def get_overview(self):
        """
        Returns a Company Overview.
        """
        return self.companyOverview

    def get_income_statement(self):
        """
        Returns a Company Income Statement.
        """
        return self.companyIncomeStatement

    def get_balance_sheet(self):
        """
        Returns a Company Balance Sheet.
        """
        return self.companyBalanceSheet

    def get_cash_flow(self):
        """
        Returns a Company Cash Flow.
        """
        return self.companyCashFlow

    def get_sentiment(self):
        """
        Returns a Company Sentiment.
        """
        return self.companySentiment