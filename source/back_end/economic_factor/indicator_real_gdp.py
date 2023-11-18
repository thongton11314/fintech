from econ_indicator_sanity_api import RealGDPSanity, RealGDPPerCapitaSanity
import json
from typing import List, Dict

class RealGDP:
    def __init__(self, interval: str = 'annual'):
        """
        Initializes a RealGDP instance for the given interval.
        Valid intervals: ''quarterly', 'annual'.
        Retrieves data using RealGDPSanity and stores it for later use.
        """
        self._sanity_data = RealGDPSanity(interval).get_data()
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
        Returns the real GDP data in JSON format.
        """
        return json.dumps({
            "name": self.name,
            "interval": self.interval,
            "unit": self.unit,
            "data": self.data
        })

class RealGDPPerCapita:
    def __init__(self, interval: str = 'annual'):
        """
        Initializes a RealGDPPerCapita instance for the given interval.
        Valid intervals: ''quarterly', 'annual'.
        Retrieves data using RealGDPPerCapitaSanity and stores it for later use.
        """
        self._sanity_data = RealGDPPerCapitaSanity(interval).get_data()
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
        Returns the real GDP per capita data in JSON format.
        """
        return json.dumps({
            "name": self.name,
            "interval": self.interval,
            "unit": self.unit,
            "data": self.data
        })
