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
        if login_response.status_code == 200 and "https://stackoverflow.com/" in login_response.url:
            print("Login successful!")
            profile_url = "https://stackoverflow.com/users/current"
            profile_response = session.get(profile_url)
            if profile_response.status_code == 200 and "Summary" in profile_response.text:
                print("Session is active!")
            else:
                print("Session failed!")
        else:
            print("Login failed.")
            print(f"Response status: {login_response.status_code}")
            print(f"Response URL: {login_response.url}")
            print(f"Response text: {login_response.text}")
    except Exception as error:
        print(f"An unexpected error occured: {error}")

login_to_stackoverflow()