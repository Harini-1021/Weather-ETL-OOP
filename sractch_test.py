from src.fetcher import DataFetcher

fetcher = DataFetcher()
fetcher.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
data = fetcher.fetch_current_weather("London")
print(data)