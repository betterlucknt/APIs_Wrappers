import requests
import pandas as pd
from datetime import date, timedelta

class AirQualitySession:

    _api_key = None
    _latest_measurements_url = None
    _measurements_url = None

    def __init__(   self,
                    _latest_measurements_url = 'https://api.openaq.org/v1/latest',
                    _measurements_url = 'https://api.openaq.org/v1/measurements'):
        self._latest_measurements_url = _latest_measurements_url
        self._measurements_url = _measurements_url

    def GetLatestMeasurements(self, latitud, longitud, radius = 6000):
        params = {'coordinates' : str(latitud) + ',' + str(longitud),
                  'radius': radius}
        r = self.Get(self._latest_measurements_url, params = params)

        if (r.status_code == 200):
            rValue = pd.concat([pd.DataFrame({'location': [location['location']],
                                  'country': [location['country']],
                                  'parameter': [measurement['parameter']],
                                  'value': [measurement['value']],
                                  'unit': [measurement['unit']],
                                  'last_updated': [measurement['lastUpdated']]}) for location in r.json()['results'] for measurement in location['measurements']])

        else:
            rValue = None

        return(rValue)

    def GetMeasurements(self, latitud, longitud, radius = 6000, from_date = date.today() - timedelta(days=1), to_date = date.today()):
        params = {'coordinates' : str(latitud) + ',' + str(longitud),
                  'radius': radius,
                  'date_from': from_date.strftime('%Y-%m-%d'),
                  'date_to': to_date.strftime('%Y-%m-%d')}
        r = self.Get(self._measurements_url, params = params)

        if (r.status_code == 200):
            rValue = pd.concat([pd.DataFrame({'location': [location['location']],
                                  'country': [location['country']],
                                  'parameter': [location['parameter']],
                                  'value': [location['value']],
                                  'unit': [location['unit']],
                                  'date': [location['date']['utc']]}) for location in r.json()['results']])
        else:
            rValue = None

        return(rValue)

    def Get(self, url, params = None):
        return(requests.get(url, params = params))

    def Post(self, url, params = None):
        return(requests.post(url, params = params))