from source.back_end.company.company_overview import CompanyOverview
from source.back_end.company.company_income_statement import CompanyIncomeStatement
from source.back_end.company.company_cash_flow import CompanyCashFlow
from source.back_end.company.company_balance_sheet import CompanyBalanceSheet
from source.back_end.company.company_sentiment import CompanySentiment

class CompanyInformationFactory:
    
    @staticmethod
    def create_overview(symbol: str):
        """
        Creates and returns a CompanyOverview object for the given symbol.
        """
        return CompanyOverview(symbol)

    @staticmethod
    def create_income_statement(symbol: str):
        """
        Creates and returns a CompanyIncomeStatement object for the given symbol.
        """
        return CompanyIncomeStatement(symbol)

    @staticmethod
    def create_balance_sheet(symbol: str):
        """
        Creates and returns a CompanyBalanceSheet object for the given symbol.
        """
        return CompanyBalanceSheet(symbol)

    @staticmethod
    def create_cash_flow(symbol: str):
        """
        Creates and returns a CompanyCashFlow object for the given symbol.
        """
        return CompanyCashFlow(symbol)

    @staticmethod
    def create_sentiment(symbol: str):
        """
        Creates and returns a CompanySentiment object for the given symbol.
        """
        return CompanySentiment(symbol)

