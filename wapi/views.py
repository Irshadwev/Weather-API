from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
import redis
import requests
import json 

# Redis connection
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# Weather API view
def weather(request):

    # Get the secret API key from the .env file
    api_key = config("WEATHER_API_KEY")

    # Get the city from the URL query parameter
    # Example: /weather/?city=Lahore
    city = request.GET.get("city")

    # Validate that the user actually provided a city
    if not city:
        return JsonResponse(
            {"error": "City is required."},
            status=400
        )

    # Create a unique Redis key for this city's weather data
    # Example: weather:lahore
    cache_key = f"weather:{city.lower()}"

    # Check Redis to see if weather data for this city is already cached
    cached_data = redis_client.get(cache_key)

    # If cached data exists, return it without calling Visual Crossing
    if cached_data:
        return JsonResponse(
            {
                "source": "cache",
                "data": json.loads(cached_data)
            },
            status=200
        )

    # Build the Visual Crossing API URL
    url = (
        f"https://weather.visualcrossing.com/"
        f"VisualCrossingWebServices/rest/services/timeline/{city}"
    )

    # Try to communicate with the external Weather API
    try:

        # Send GET request to Visual Crossing
        # timeout prevents our Django server from waiting forever
        response = requests.get(
            url,
            params={
                "key": api_key,
                "unitGroup": "metric"
            },
            timeout=10
        )

        # Check whether the external API returned an HTTP error
        # Example: 400, 401, 404, 500
        response.raise_for_status()

        # Convert the API response from JSON text into Python data
        data = response.json()

        # Save the successful weather response in Redis
        # The data is converted to JSON text because Redis stores strings
        # 600 seconds = 10 minutes
        redis_client.setex(
            cache_key,
            600,
            json.dumps(data)
        )

        # Return the fresh weather data to the client
        return JsonResponse(
            {
                "source": "api",
                "data": data
            },
            status=200
        )

    # Handle request timeout
    except requests.exceptions.Timeout:
        return JsonResponse(
            {"error": "Weather service request timed out."},
            status=504
        )

    # Handle HTTP errors returned by the Weather API
    except requests.exceptions.HTTPError as e:
        return JsonResponse(
            {
                "error": "Weather API request failed.",
                "details": str(e)
            },
            status=response.status_code
        )

    # Handle other problems communicating with the external API
    except requests.exceptions.RequestException:
        return JsonResponse(
            {"error": "Unable to connect to weather service."},
            status=502
        )


# Frontend connected 
def weather_page(request):
    """
    Render the frontend weather application.

    This view only serves the HTML page.
    The JavaScript on that page calls the /weather/ API.
    """
    return render(request, "wapi/weather.html")