import unittest
from unittest.mock import patch
from econ_indicator_sanity_api import RealGDPSanity

class TestRealGDPSanity(unittest.TestCase):

    @patch('econ_indicator_sanity_api.EconIndicatorSanityBase._get_data_from_api')
    def test_get_data(self, mock_api_call):
        mock_api_call.return_value = {
            'name': 'Real GDP',
            'interval': 'annual',
            'unit': 'USD',
            'data': [{'date': '2023-01-01', 'value': 1000}]
        }
        sanity_checker = RealGDPSanity('annual')
        result = sanity_checker.get_data()
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Real GDP')

if __name__ == '__main__':
    unittest.main()
