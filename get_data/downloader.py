import os
import datetime
import pandas as pd
from fred_client import FredClient

class FredDownloader:
    def __init__(self, client, output_dir='data', items=None):
        self.client = client
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if items is None:
            self.items = list(client.series_codes.keys())
        else:
            self.items = items

    def download_data(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        for item in self.items:
            file_path = os.path.join(self.output_dir, f'{item}.csv')
            if os.path.exists(file_path):
                # If file exists, load the existing data and append new data
                df = pd.read_csv(file_path, index_col='date')
                latest_date = pd.to_datetime(df.index[-1]).date()
                if latest_date < datetime.date.today():
                    new_data = self.client.get_series(item)[latest_date+datetime.timedelta(days=1):today]
                    df = df.append(new_data.rename('value')).sort_index()
            else:
                # If file does not exist, download all data
                df = self.client.get_series(item)[:today].rename('value')
            df.to_csv(file_path, header=True)


if __name__ == "__main__":
    client = FredClient()
    downloader = FredDownloader(client)
    downloader.download_data()
