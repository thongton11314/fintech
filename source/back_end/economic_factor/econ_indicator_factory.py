from indicator_real_gdp import RealGDP, RealGDPPerCapita
from indicator_treasury_yield import TreasuryYield
from indicator_federal_funds_rate import FederalFundsRate
from indicator_inflation import Inflation
from indicator_consumer_price_index import ConsumerPriceIndex
from indicator_retail_sales import RetailSales
from indicator_durable_goods_orders import DurableGoodsOrders
from indicator_unemployment_rate import UnemploymentRate

class EconIndicatorFactory:
    """
    Factory class to get economic indicator data.
    Provides separate methods for each economic indicator.
    You can get, Real GDP data, Real GDP Per Capita data, Federal Funds Rate
    Treasury Yield data, Consumer Price Index (CPI) data, Inflation data,
    Retail Sales data, Durable Goods Orders data, Unemployment Rate data
    """

    @staticmethod
    def get_real_gdp(interval: str = 'annual'):
        """
        Gets Real GDP data.
        :param interval: Data interval, default is 'annual'.
        :return: Real GDP data.
        """
        try:
            return RealGDP(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Real GDP data: {e}"

    @staticmethod
    def get_real_gdp_per_capita(interval: str = 'annual'):
        """
        Gets Real GDP Per Capita data.
        :param interval: Data interval, default is 'annual'.
        :return: Real GDP Per Capita data.
        """
        try:
            return RealGDPPerCapita(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Real GDP Per Capita data: {e}"
        
    @staticmethod
    def get_federal_funds_rate(interval: str = 'annual'):
        """
        Gets Federal Funds Rate.
        :param interval: Data interval, default is 'annual'.
        :return: Federarl Funs Rate
        """
        try:
            return FederalFundsRate(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Federarl Funs Rate data: {e}"
        
    @staticmethod
    def get_treasury_yield(interval: str = 'monthly'):
        """
        Gets Treasury Yield data.
        :param interval: Data interval, default is 'monthly'.
        :return: Treasury Yield data.
        """
        try:
            return TreasuryYield(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Treasury Yield data: {e}"

    @staticmethod
    def get_consumer_price_index(interval: str = 'monthly'):
        """
        Gets Consumer Price Index (CPI) data.
        :param interval: Data interval, default is 'monthly'.
        :return: CPI data.
        """
        try:
            return ConsumerPriceIndex(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Consumer Price Index data: {e}"

    @staticmethod
    def get_inflation(interval: str = 'annual'):
        """
        Gets Inflation data.
        :param interval: Data interval, default is 'annual'.
        :return: Inflation data.
        """
        try:
            return Inflation(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Inflation data: {e}"

    @staticmethod
    def get_retail_sales(interval: str = 'monthly'):
        """
        Gets Retail Sales data.
        :param interval: Data interval, default is 'monthly'.
        :return: Retail Sales data.
        """
        try:
            return RetailSales(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Retail Sales data: {e}"

    @staticmethod
    def get_durable_goods_orders(interval: str = 'monthly'):
        """
        Gets Durable Goods Orders data.
        :param interval: Data interval, default is 'monthly'.
        :return: Durable Goods Orders data.
        """
        try:
            return DurableGoodsOrders(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Durable Goods Orders data: {e}"

    @staticmethod
    def get_unemployment_rate(interval: str = 'monthly'):
        """
        Gets Unemployment Rate data.
        :param interval: Data interval, default is 'monthly'.
        :return: Unemployment Rate data.
        """
        try:
            return UnemploymentRate(interval=interval).get_data()
        except Exception as e:
            return f"Error fetching Unemployment Rate data: {e}"

# Testing purpose
def main():

    # Test and print the output for each method
    print("Real GDP Data:")
    print(EconIndicatorFactory().get_real_gdp('annual'))
    print()

    print("Real GDP Per Capita Data:")
    print(EconIndicatorFactory().get_real_gdp_per_capita('annual'))
    print()

    print("Treasury Yield Data:")
    print(EconIndicatorFactory().get_treasury_yield('monthly'))
    print()

    print("Federal Funds Rate Data:")
    print(EconIndicatorFactory().get_federal_funds_rate('monthly'))
    print()

    print("Consumer Price Index Data:")
    print(EconIndicatorFactory().get_consumer_price_index('monthly'))
    print()

    print("Inflation Data:")
    print(EconIndicatorFactory().get_inflation('annual'))
    print()

    print("Retail Sales Data:")
    print(EconIndicatorFactory().get_retail_sales('monthly'))
    print()

    print("Durable Goods Orders Data:")
    print(EconIndicatorFactory().get_durable_goods_orders('monthly'))
    print()

    print("Unemployment Rate Data:")
    print(EconIndicatorFactory().get_unemployment_rate('monthly'))
    print()

if __name__ == "__main__":
    main()
