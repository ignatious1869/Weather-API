import socket
import json
import requests
import time
from datetime import datetime

# ---------------------------
# Configuration
# ---------------------------
HOST = "0.0.0.0"          # Listen on all available network interfaces
PORT = 5050               # Port number for incoming connections
SHARED_KEY = "jwu2025"    # Simple shared authentication key for security
LOG_FILE = "server_log.txt"  # File where server logs will be stored

# ---------------------------
# Function to log events with timestamps
# ---------------------------
def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {event}\n")

# ---------------------------
# Function to get forecast data from Open-Meteo API
# ---------------------------
def get_forecast(city):
    try:
        # Step 1: Convert city name to coordinates using the geocoding API
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo = requests.get(url, timeout=5).json()

        # Handle invalid city names
        if "results" not in geo or len(geo["results"]) == 0:
            return None

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        # Step 2: Use coordinates to fetch hourly temperature forecast
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days=1"
        )
        data = requests.get(weather_url, timeout=5).json()

        # Step 3: Compute a simple average of hourly temperatures
        temps = data["hourly"]["temperature_2m"]
        avg_temp = sum(temps) / len(temps)
        return round(avg_temp, 1)

    except Exception as e:
        # Log any errors that occur during the API call
        log_event(f"Error fetching forecast: {e}")
        return None

# ---------------------------
# Main server function
# ---------------------------
def start_server():
    log_event("Server starting...")

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    log_event(f"Server listening on port {PORT}")

    while True:
        # Wait for a client connection
        conn, addr = s.accept()
        log_event(f"Connected by {addr}")

        try:
            # Receive data from client
            data = conn.recv(1024).decode()
            if not data:
                continue

            # Parse received JSON data
            request = json.loads(data)
            city = request.get("city")
            key = request.get("key")

            # Check authentication key
            if key != SHARED_KEY:
                conn.send("Access denied".encode())
                log_event(f"Unauthorized access attempt from {addr}")
                conn.close()
                continue

            # Retrieve forecast from public API
            forecast = get_forecast(city)
            if forecast is not None:
                message = f"Avg Temperature in {city}: {forecast}°C"
                conn.send(message.encode())
                log_event(f"Sent forecast to {addr}: {message}")
            else:
                conn.send("Error retrieving data".encode())

        except Exception as e:
            log_event(f"Error: {e}")

        finally:
            # Always close the connection
            conn.close()

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    start_server()
