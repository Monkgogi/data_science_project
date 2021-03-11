#Raluca-Irina Paiajen
#13th Jan 2021

import matplotlib.pyplot as plt


class LineGraph:
    def __init__(self, country, filter, start_year, end_year):
        self.country = country
        self.filter = filter
        self.start_year = start_year
        self.end_year = end_year

    def add_country(self, country, add_country):
        self.country.append(str(add_country))
        return country

    def remove_country(self, country, remove_country):
        self.country.remove(str(remove_country))
        return country

    def change_start_year(self, start_year):
        self.start_year = start_year
        return start_year

    def change_end_year(self, end_year):
        self.end_year = end_year
        return end_year

    def change_filter(self, filter):
        self.filter = filter
        return filter

    def draw_linegraph(self, years, filter):
        plt.plot(years, filter)
        plt.show()
        return