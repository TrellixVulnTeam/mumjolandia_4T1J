import logging

from src.external import requests
from src.external.requests import Timeout
from src.external.requests import ConnectionError
from src.external.requests.exceptions import MissingSchema
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor


class WeatherSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.weather_get_ok,
                                         arguments=[self.__get_weather_now()])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.weather_help,
                                         arguments=['print'])

    def __get_weather_now(self):
        try:
            response = requests.get('https://fcc-weather-api.glitch.me/api/current?lat=51.1&lon=17.03', timeout=(3, 5))
        except (Timeout, ConnectionError) as e:
            logging.info('Weather API timeout')
            return 'Timeout :('
        except MissingSchema:
            return 'Invalid URL'
        if response.status_code == 200:
            json_response = response.json()
            weather = json_response['weather'][0]['main']
            temperature = json_response['main']['temp']
            return weather + ' ' + '%.1f' % temperature + 'C'
        else:
            logging.info('Weather API returned non 200-response')
            return 'API returned status code ' + response.status_code