from datetime import datetime, timezone
from typing import Dict
import logging
import requests

from weather.dto import CurrentWeatherDTO
from weather.exceptions import CityNotFoundError, ExternalServiceError

logger = logging.getLogger(__name__)


class CurrentWeatherService:
    def __init__(self, api_key: str, units: str):
        self._api_key = api_key
        self._units = units

    def get_weather(self, city_name: str) -> CurrentWeatherDTO:
        weather_json = self._make_api_request(city_name)
        weather_dto = self._parse_weather_json(weather_json)
        return weather_dto

    def _make_api_request(self, city_name: str) -> Dict:
        params = {
            'q': city_name,
            'appid': self._api_key,
            'units': self._units
        }
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        status_code = response.status_code

        if status_code == 200:
            return response.json()
        elif status_code == 404:
            message = response.json()['message']
            raise CityNotFoundError(message)
        else:
            message = response.json()['message']
            logger.error(f"OpenWeather service error message: {message}")
            raise ExternalServiceError(message)

    def _parse_weather_json(self, weather_json: Dict) -> CurrentWeatherDTO:
        description = weather_json['weather'][0]['description']
        temp = int(weather_json['main']['temp'])
        name = weather_json['name']
        wind = float(weather_json['wind']['speed'])
        humidity = weather_json['main']['humidity']

        local_now = datetime.now(timezone.utc).astimezone()
        offset_seconds = local_now.utcoffset().total_seconds()

        last_update = datetime.utcfromtimestamp(
            weather_json['dt'] + offset_seconds).strftime('%H:%M')
        sunrise = datetime.utcfromtimestamp(
            weather_json['sys']['sunrise'] + weather_json['timezone']).strftime('%H:%M')
        sunset = datetime.utcfromtimestamp(
            weather_json['sys']['sunset'] + weather_json['timezone']).strftime('%H:%M')
        icon_code = weather_json['weather'][0]['icon']
        icon = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'
        weather_dto = CurrentWeatherDTO(
            description=description,
            temp=temp,
            name=name,
            wind=wind,
            humidity=humidity,
            last_update=last_update,
            sunrise=sunrise,
            sunset=sunset,
            icon=icon
        )
        return weather_dto


# weather_service = CurrentWeatherService(api_key='b7eabda962f25282f09cad961bd46cc8', units='metric')
# weather_service.get_weather('paris')
