from typing import NamedTuple


class CurrentWeatherDTO(NamedTuple):
    description: str
    temp: int
    name: str
    wind: float
    humidity: int
    last_update: str
    sunrise: str
    sunset: str
    icon: str
