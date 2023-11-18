from econ_indicator_sanity_api import RetailSalesSanity
import json
from typing import List, Dict

class RetailSales:
    def __init__(self, interval: str = 'monthly'):
        """
        Initializes a RetailSales instance for the given interval.
        Valid intervals: 'monthly'.
        Retrieves data using RetailSalesSanity and stores it for later use.
        """
        self._sanity_data = RetailSalesSanity(interval).get_data()
        self._data_loaded = self._sanity_data is not None

    @property
    def name(self) -> str:
        return self._sanity_data["name"] if self._data_loaded else ""

    @property
    def interval(self) -> str:
        return self._sanity_data["interval"] if self._data_loaded else ""

    @property
    def unit(self) -> str:
        return self._sanity_data["unit"] if self._data_loaded else ""

    @property
    def data(self) -> List[Dict[str, str]]:
        if self._data_loaded:
            return [{"date": item["date"].strftime("%Y-%m-%d"), "value": item["value"]} for item in self._sanity_data["data"]]
        return []

    def get_data(self) -> str:
        """
        Returns the retail sales data in JSON format.
        """
        return json.dumps({
            "name": self.name,
            "interval": self.interval,
            "unit": self.unit,
            "data": self.data
        })
