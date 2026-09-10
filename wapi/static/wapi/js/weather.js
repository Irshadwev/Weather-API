/* ================================
   Get HTML Elements
================================ */

const weatherForm = document.getElementById("weather-form");
const cityInput = document.getElementById("city-input");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("error-message");
const weatherResult = document.getElementById("weather-result");

const cityName = document.getElementById("city-name");
const weatherDescription = document.getElementById("weather-description");

const temperature = document.getElementById("temperature");
const feelsLike = document.getElementById("feels-like");
const humidity = document.getElementById("humidity");
const windSpeed = document.getElementById("wind-speed");
const pressure = document.getElementById("pressure");

const dataSource = document.getElementById("data-source");


/* ================================
   Weather Form
================================ */

weatherForm.addEventListener("submit", function (event) {

    // Prevent normal form submission
    event.preventDefault();

    const city = cityInput.value.trim();

    // Check if city is empty
    if (!city) {
        showError("Please enter a city name.");
        return;
    }

    getWeather(city);
});


/* ================================
   Get Weather From Django API
================================ */

async function getWeather(city) {

    // Reset previous messages
    hideError();
    weatherResult.classList.add("hidden");

    // Show loading
    loading.classList.remove("hidden");

    try {

        // Call our Django Weather API
        const response = await fetch(
            `/weather/?city=${encodeURIComponent(city)}`
        );

        // Convert response into JSON
        const result = await response.json();

        // Hide loading
        loading.classList.add("hidden");


        /* ================================
           Handle API Errors
        ================================= */

        if (!response.ok) {

            showError(
                result.error || "Unable to get weather information."
            );

            return;
        }


        /* ================================
           Display Weather Data
        ================================= */

        displayWeather(result);

    } catch (error) {

        // Hide loading
        loading.classList.add("hidden");

        // Handle network/frontend errors
        showError(
            "Unable to connect to the weather server."
        );

        console.error("Weather API Error:", error);
    }
}


/* ================================
   Display Weather
================================ */

function displayWeather(result) {

    const data = result.data;

    /*
     * Visual Crossing returns the current
     * weather information inside currentConditions.
     */

    const current = data.currentConditions;


    // City
    cityName.textContent = data.resolvedAddress || "Unknown location";


    // Weather condition
    weatherDescription.textContent =
        current.conditions || "Unknown";


    // Temperature
    temperature.textContent =
        current.temp ?? "--";


    // Feels like
    feelsLike.textContent =
        current.feelslike !== undefined
            ? `${current.feelslike} °C`
            : "--";


    // Humidity
    humidity.textContent =
        current.humidity !== undefined
            ? `${current.humidity}%`
            : "--";


    // Wind speed
    windSpeed.textContent =
        current.windspeed !== undefined
            ? `${current.windspeed} km/h`
            : "--";


    // Pressure
    pressure.textContent =
        current.pressure !== undefined
            ? `${current.pressure} hPa`
            : "--";


    // Show whether data came from API or Redis cache
    dataSource.textContent =
        result.source === "cache"
            ? "Redis Cache"
            : "Weather API";


    // Show weather result
    weatherResult.classList.remove("hidden");
}


/* ================================
   Show Error
================================ */

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");
}


/* ================================
   Hide Error
================================ */

function hideError() {

    errorMessage.textContent = "";

    errorMessage.classList.add("hidden");
}