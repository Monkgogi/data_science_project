#Raluca-Irina Paiajen

from classes.LineGraph import *
import unittest


class LineGraphTest(unittest.TestCase):
    def test_add_country(self):
        """Don't let user add more than 5 countries in the plot"""
        LG = LineGraph(["C1", "C2", "C3", "C4", "C5"], 1, 1, 1)
        self.assertTrue(len(LG.country)<=5, "ErrorMsg: More than 5 countries added!")

    def test_draw_linegraph(self):
        """Don't let user plot empty graph"""


if __name__ == '__main__':
    unittest.main()

"""
filter, start_year and end_year will have default values
.
filter, start_year and end_year inputs are chosen from dropdowns,
no need for testcase
.
country does not have default values
.
no linegraph is plot unless there is at least one country added to the list of countries
"""