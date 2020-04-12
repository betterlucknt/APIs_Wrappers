import requests
import pandas as pd

class WeatherSession:

    _api_key = None
    _current_weather_url = None
    _forecast_url = None

    def __init__(   self,
                    api_key,
                    current_weather_url = r'http://api.openweathermap.org/data/2.5/weather/',
                    forecast_url = r'http://api.openweathermap.org/data/2.5/forecast/'):
        self._api_key = api_key
        self._current_weather_url = current_weather_url
        self._forecast_url = forecast_url

    def GetForecast(self, city_id = None, latitude = None, longitud = None):

        if(city_id != None):
            params = {"id": city_id}
        elif((latitude != None) & (longitud != None)):
            params = {'lat': latitude,
                      'lon': longitud}
        else:
            return(None)

        r = self.Get(self._forecast_url, params=params)

        if(r.status_code == 200):
            rList = []
            for forecast in r.json()['list']:
                df = pd.DataFrame({'date_time': [forecast['dt_txt']]})
                for item in forecast['main'].items():
                    df['main_' + item[0]] = item[1]
                for item in forecast['weather'][0].items():
                    df['weather_' + item[0]] = item[1]
                for item in forecast['clouds'].items():
                    df['clouds_' + item[0]] = item[1]
                for item in forecast['wind'].items():
                    df['wind_' + item[0]] = item[1]
                for item in forecast['sys'].items():
                    df['sys_' + item[0]] = item[1]

                rList.append(df)
            rDF = pd.concat(rList, ignore_index=True)

        else:
            rDF = None

        return(r)

    def GetCurrentWeather(self, city_id = None, latitude = None, longitud = None):

        if(city_id != None):
            params = {"id": city_id}
        elif((latitude != None) & (longitud != None)):
            params = {'lat': latitude,
                      'lon': longitud}
        else:
            return(None)

        r = self.Get(self._current_weather_url, params=params).json()

        if(r.status_code == 200):
            r_json = r.json()
            rDF = pd.DataFrame({'name': [r_json['name']]})
            for item in r_json['coord'].items():
                rDF['coord_' + item[0]] = item[1]
            for item in r_json['weather'][0].items():
                rDF['weather_' + item[0]] = item[1]
            for item in r_json['main'].items():
                rDF['main_' + item[0]] = item[1]
            rDF['visibility'] = r_json['visibility']
            for item in r_json['wind'].items():
                rDF['wind_' + item[0]] = item[1]
            for item in r_json['clouds'].items():
                rDF['clouds_' + item[0]] = item[1]
            for item in r_json['sys'].items():
                rDF['sys_' + item[0]] = item[1]

        else:
            rDF = None

        return(rDF)

    def Get(self, url, params = None):
        if(params == None):
            params = {"APPID": self._api_key}
        else:
            params['APPID'] = self._api_key

        return(requests.get(url, params = params))

    def Post(self, url, params = None):
        if(params == None):
            params = {"APPID": self._api_key}
        else:
            params['APPID'] = self._api_key

        return(requests.post(url, params = params))