import socket
import json
import time
from datetime import datetime

# ---------------------------
# Configuration
# ---------------------------
SERVER_IP = "127.0.0.1"   # Server IP (change to remote server IP if needed)
PORT = 5050               # Must match server port
SHARED_KEY = "jwu2025"    # Shared authentication key (must match server)
LOG_FILE = "client_log.txt"  # File where client logs will be stored

# ---------------------------
# Function to log events with timestamps
# ---------------------------
def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {event}\n")

# ---------------------------
# Function to connect to the server and request a forecast
# ---------------------------
def connect_and_request(city):
    attempt = 1

    # Retry up to 3 times if connection fails
    while attempt <= 3:
        try:
            # Create a TCP socket and connect to the server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, PORT))

            # Prepare JSON payload with city name and key
            payload = json.dumps({"city": city, "key": SHARED_KEY})
            s.send(payload.encode())  # Send request to server

            # Receive response from server
            response = s.recv(1024).decode()
            print(response)  # Display forecast on screen
            log_event(f"Response: {response}")

            s.close()
            return  # Stop after successful communication

        except ConnectionRefusedError:
            # Handle server unavailable case
            log_event("Connection failed. Retrying...")
            print("Server unavailable, retrying...")
            time.sleep(3)
            attempt += 1

        except Exception as e:
            # Handle unexpected errors
            log_event(f"Error: {e}")
            print("Unexpected error:", e)
            break

    # If all retries fail
    log_event("Failed after multiple attempts.")

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    city = input("Enter city name: ")
    connect_and_request(city)
