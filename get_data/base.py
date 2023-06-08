import os
import pandas as pd
from fredapi import Fred

# vim ~/.zshrc and add below
# export FRED_API_KEY=''

class FredClient:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.environ.get('FRED_API_KEY')
            if api_key is None:
                raise ValueError("No FRED API key provided. Please set the 'FRED_API_KEY' environment variable.")
        self.fred = Fred(api_key)
        self.series_codes = {
            'federal_funds_rate':'DFF',
            'gdp':'GDP',
            'core_cpi':'CORESTICKM159SFRBATL',
            'fed_total_assets':'walcl',
            'm2':'WM2NS',
            'unemployment_rate': 'UNRATE',
            'sp500':'SP500',
            'washington_homeownership_rate':'WAHOWN',
            'washington_unemployment_rate':'WAUR',
            'washington_housing_inventory': 'NEWLISCOUWA',
            'washington_per_capital_income':'WAPCPI',
            'washington_median_household_income':'MEHOINUSWAA646N',
            'washington_resident_population':'WAPOP',
            'washington_rental_vacancy_rate':'WARVAC',
            'washington_zillow_home_value_index':'WAUCSFRCONDOSMSAMID',
        }

    def get_series(self, item, ffill=True):
        code = self.series_codes.get(item)
        if ffill:
            return self.fred.get_series(code).ffill()
        else:
            return self.fred.get_series(code)

    def get_info(self, item):
        code = self.series_codes.get(item)
        return self.fred.get_series_info(code)

    def search_item(self, item):
        return self.fred.search(item).T

    def get_latest_release(self, item, ffill=True):
        code = self.series_codes.get(item)
        if ffill:
            return self.fred.get_series_latest_release(code).ffill()
        else:
            return self.fred.get_series_latest_release(code)

    def get_all_releases(self, item):
        code = self.series_codes.get(item)
        return self.fred.get_series_all_releases(code)


if __name__ == "__main__":
    client = FredClient()

    m2 = client.get_latest_release('m2')
    gdp = client.get_latest_release('gdp')
    core_cpi = client.get_latest_release('core_cpi')
    fed_assets = client.get_latest_release('fed_total_assets')
    federal_funds_rate = client.get_latest_release('federal_funds_rate')

    print(federal_funds_rate)
