import pandas as pd
from requests import get
import matplotlib.pyplot as plt
from numpy import NaN

class fredSeries:
    def __init__(self, 
                 seriesID,
                 key,
                 realtime_start = '1776-07-04',
                 realtime_end = '9999-12-31',
                 limit = 100000,
                 offset = 0,
                 sort_order = 'asc',
                 observation_start = '1776-07-04',
                 observation_end = '9999-12-31',
                 units = 'lin',
                 frequency = '',
                 aggregation_method = 'avg',
                 output_type = 1,
                 vintage_dates = ''):
        self.url = f'https://api.stlouisfed.org/fred/series/observations?series_id={seriesID}'
        self.url += f'&api_key={key}'
        self.url += f'&realtime_start={realtime_start}'
        self.url += f'&realtime_end={realtime_end}'
        self.url += f'&limit={limit}'
        self.url += f'&offset={offset}'
        self.url += f'&sort_order={sort_order}'
        self.url += f'&observation_start={observation_start}'
        self.url += f'&observation_end={observation_end}'
        self.url += f'&units={units}'
        self.url += f'&frequency={frequency}'
        self.url += f'&aggregation_method={aggregation_method}'
        self.url += f'&output_type={output_type}'
        self.url += f'&vintage_dates={vintage_dates}'
        self.url += f'&file_type=json'
        #
        meta = self._getMeta(seriesID, key)
        self.title = meta['title']
        self.frequency = meta['frequency']
        self.last_updated = meta['last_updated']
        self.value = meta['units']
        self.adjusted = meta['seasonal_adjustment']
        self.notes = meta['notes']
        
    def _getMeta(self, seriesID, key):
        url = f'https://api.stlouisfed.org/fred/series?series_id={seriesID}&api_key={key}&file_type=json'
        req = get(url)
        res = req.json()
        return res['seriess'][0]
        
    def getJson(self):
        req = get(self.url)
        res = req.json()
        return res['observations']
    
    def getDf(self):
        df = pd.DataFrame(self.getJson())
        df['date'] = pd.to_datetime(df.date)
        df['value'] = df.value.replace('.', NaN)
        df['value'] = df.value.astype('float')
        df.rename(columns = {'value':self.value}, inplace = True)
        df.set_index('date', inplace = True)
        df.drop(columns = ['realtime_start', 'realtime_end'], 
                inplace = True)
        return df
    
    def getChart(self):
        df = self.getDf()
        df.plot(title = f'{self.title}\n({self.adjusted}, {self.frequency})')
        plt.show()
        print(f'Last updated: {self.last_updated}')
        print()
        print(self.notes)