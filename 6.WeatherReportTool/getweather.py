import requests

api_key = 'YOUR_OPENWEATHERMAP_API_KEY'  # Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key
city_name = 'London'  # Replace with the desired city name

# API endpoint URL for getting current weather data by city name
api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

# Sending a GET request to the OpenWeatherMap API endpoint with the API key included in the URL
response = requests.get(api_url)

# Checking the response status code
if response.status_code == 200:  # Successful response
    data = response.json()  # Parsing the JSON response
    # Extracting relevant information from the response
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    
    # Displaying the weather information
    print(f"Weather in {city_name}:")
    print(f"Description: {weather_description}")
    print(f"Temperature: {temperature} K")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
else:
    print(f"Error: {response.status_code} - {response.text}")
