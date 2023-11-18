from econ_indicator_base_api import EconIndicatorAPI
import datetime
from typing import Optional, Dict, List, Any

class EconIndicatorSanityBase(EconIndicatorAPI):
    """
    A base class for sanity checks on economic indicators. 
    It extends EconIndicatorAPI and provides a structured approach to process and validate data from various economic indicators.
    """
    def __init__(self, interval: str, api_function: str):
        """
        Initializes the sanity checker with a specified time interval and API function.
        :param interval: Time interval for the economic data (e.g., 'monthly').
        :param api_function: The specific API function name to call for the data.
        """
        super().__init__(interval)
        self.api_function = api_function

    def get_data_format(self, name: str, interval: str, unit: str, processed_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Formats the processed data into a structured dictionary.
        :param name: Name of the economic indicator.
        :param interval: Time interval for the economic data.
        :param unit: Measurement unit of the economic data.
        :param processed_data: The processed data list.
        :return: A dictionary with formatted economic data.
        """
        return {
            "name": name,
            "interval": interval,
            "unit": unit,
            "data": processed_data
        }

    def process_data_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes each data entry, converting date strings to datetime objects.
        :param entry: A dictionary representing a single data entry.
        :return: Processed data entry with datetime object for date.
        """
        try:
            date = datetime.datetime.strptime(entry["date"], "%Y-%m-%d")
        except ValueError:
            # If the date format is incorrect, handle the error (e.g., log or throw exception).
            return {}

        return {
            "date": date,
            "value": entry.get("value")
        }

    def get_data(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves and processes data from the API.
        :return: Processed data in a structured format or None if the API call fails.
        """
        raw_data = self._get_data_from_api(self.api_function)
        if raw_data is None:
            return None

        name = raw_data.get("name")
        interval = raw_data.get("interval")
        unit = raw_data.get("unit")

        processed_data = [self.process_data_entry(entry) for entry in raw_data.get("data", [])]

        return self.get_data_format(name=name, interval=interval, unit=unit, processed_data=processed_data)

# Below are subclasses for specific economic indicators, each initializing the base class with the appropriate API function.

class RealGDPSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Real GDP data.
    """
    def __init__(self, interval: str):
        super().__init__(interval, "REAL_GDP")

class RealGDPPerCapitaSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Real GDP Per Capita data.
    """
    def __init__(self, interval: str):
        super().__init__(interval, "REAL_GDP_PER_CAPITA")

class TreasuryYieldSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Treasury Yield data.
    """
    def __init__(self, interval: str):
        super().__init__(interval, "TREASURY_YIELD")

class FederalFundsRateSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Federal Funds Rate data.
    """
    def __init__(self, interval: str):
        super().__init__(interval, "FEDERAL_FUNDS_RATE")
        
class InflationSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Inflation data.
    """
    def __init__(self, interval: str):
        super().__init__(interval, "INFLATION")
        
class ConsumerPriceIndexSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Consumer Price Index (CPI) data.
    """
    def __init__(self, interval: str):
        super().__init__(interval, "CPI")
        
class RetailSalesSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Retail Sales data.
    """
    def __init__(self, interval: str):
        super().__init__(interval, "RETAIL_SALES")
        
class DurableGoodsOrdersSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Durable Goods Orders data.
    """
    def __init__(self, interval: str):
        """
        Initializes the sanity checker for Durable Goods Orders data.
        :param interval: Time interval for the economic data (e.g., 'monthly').
        """
        super().__init__(interval, "DURABLES")

class UnemploymentRateSanity(EconIndicatorSanityBase):
    """
    Sanity checker for Unemployment Rate data.
    """
    def __init__(self, interval: str):
        """
        Initializes the sanity checker for Unemployment Rate data.
        :param interval: Time interval for the economic data (e.g., 'monthly').
        """
        super().__init__(interval, "UNEMPLOYMENT")