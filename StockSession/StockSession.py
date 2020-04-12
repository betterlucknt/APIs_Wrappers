import requests
import pandas as pd

class StockSession:

    _api_key = None
    _base_url = None

    def __init__(   self,
                    api_key,
                    base_url = 'https://www.alphavantage.co/query'):
        self._api_key = api_key
        self._base_url = base_url

    def GetSymbolWeekly(self, symbol):
        params = {'function': 'TIME_SERIES_WEEKLY',
                  'symbol': symbol}
        r = self.Get(self._base_url, params = params)
        rValue = self._FormatResponse(r, 'Weekly Time Series')

        return(rValue)

    def GetSymbolDaily(self, symbol):
        params = {'function': 'TIME_SERIES_DAILY',
                  'symbol': symbol}
        r = self.Get(self._base_url, params = params)
        rValue = self._FormatResponse(r, 'Time Series (Daily)')

        return(rValue)

    def GetSymbolIntraday(self, symbol, interval = '15min'):
        params = {'function': 'TIME_SERIES_INTRADAY',
                  'symbol': symbol,
                  'interval': interval}
        r = self.Get(self._base_url, params = params)
        rValue = self._FormatResponse(r, 'Time Series (' + interval + ')')

        return(rValue)

    def _FormatResponse(self, response, key):
        if(response.status_code == 200):
            rValue = pd.concat([pd.DataFrame({'Time': update_time,
                                              'Open': [update['1. open']],
                                              'High': [update['2. high']],
                                              'Low': [update['3. low']],
                                              'Close': [update['4. close']],
                                              'Volume': [update['5. volume']]}) for update_time, update in response.json()[key].items()])
            rValue = pd.melt(rValue, id_vars=['Time', 'Volume'], value_vars=['Open', 'High', 'Low', 'Close'], value_name='Value', var_name='Variable')
            rValue.Time = pd.to_datetime(rValue.Time)
            rValue.Value = pd.to_numeric(rValue.Value)
            rValue.Volume = pd.to_numeric(rValue.Volume)

        else:
            rValue = None

        return (rValue)

    def Get(self, url, params = None):
        if(params == None):
            params = {"apikey": self._api_key}
        else:
            params['apikey'] = self._api_key

        return(requests.get(url, params = params))

    def Post(self, url, params = None):
        if(params == None):
            params = {"apikey": self._api_key}
        else:
            params['apikey'] = self._api_key

        return(requests.post(url, params = params))