# Aidan Coyne
# 12 January 2021

class CountryData:
    def __init__(self, country, num_visits, total_spent, nights, purpose, stay_dur):
        self.country = country
        self.num_visits = num_visits
        self.total_spent = total_spent
        self.nights = nights
        self.purpose = purpose
        self.stay_dur = stay_dur

    def get_info_for_year(self, year):
        """Return list of data for specific year"""

    def info_for_year_and_quarter(self, year, quarter):
        """Return data for year and specific quarter"""

    def get_travel_purpose_vals(self):
        """Return purposes for travel"""
