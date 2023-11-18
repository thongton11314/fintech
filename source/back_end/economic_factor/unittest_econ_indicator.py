import unittest
from unittest.mock import patch
from econ_indicator_factory import EconIndicatorFactory  # Replace with your actual module name

class TestEconIndicatorFactory(unittest.TestCase):

    @patch('econ_indicator_factory.RealGDP.get_data')  # Corrected to use the actual module name
    def test_get_real_gdp(self, mock_get_data):
        mock_get_data.return_value = {'sample': 'data'}
        result = EconIndicatorFactory.get_real_gdp('annual')
        self.assertEqual(result, {'sample': 'data'})

if __name__ == '__main__':
    unittest.main()
