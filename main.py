import requests
from bs4 import BeautifulSoup
import os

def login_to_stackoverflow():
    print("Getting ready to log in...")

    # Credentials
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]

    try:
        # Start a session
        session = requests.Session() # so that cookies are persisted

        # Extract the CSRF token from the page
        login_url = "https://stackoverflow.com/users/login"
        response = session.get(login_url)
        soup = BeautifulSoup(response.text, "html.parser")
        token = soup.find("input", {"name": "fkey"})["value"] # stackoverflow's form validation token

        # Submit the form
        payload = {
            "email": email,
            "password": password,
            "fkey": token
        }
        login_response = session.post(login_url, data=payload)

        # Check if login was successful
        if "https://stackoverflow.com/" in login_response.url:
            print("Login successful!")
        else:
            print("Login failed.")
            print(f"Response URL: {login_response.url}")
            print(f"Response text: {login_response.text}")
    except Exception as error:
        print(f"An unexpected error occured: {error}")

login_to_stackoverflow()