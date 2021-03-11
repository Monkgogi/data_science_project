from country_data import *
import unittest


class TestCountryData(unittest.TestCase):
    def test_get_info_for_year(self):
        """
        List should have country, travel purpose
        total visits, total nights,
        total spend, and average stay duration
        """
        c = CountryData("Test", 1, 1, 1, 1, 1)
        self.assertEqual(len(c.get_info_for_year(1)), 6)

    def test_info_for_year_and_quarter(self):
        """
        List should have three positive values:
        total visits, total nights, total spend
        """

    def test_get_travel_purpose_vals(self):
        """
        List should have only five positive
        values for travel purposes
        """


if __name__ == '__main__':
    unittest.main()
