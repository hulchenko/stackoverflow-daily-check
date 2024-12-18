import requests
from bs4 import BeautifulSoup
import os

def login_to_stackoverflow():
    print("Getting ready to log in...")

    # Credentials
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]

    # Start a session
    session = requests.Session()

    # Extract the CSRF token from the page
    login_url = "https://stackoverflow.com/users/login"
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "fkey"})["value"]

    # Submit the form
    payload = {
        "email": email,
        "password": password,
        "fkey": csrf_token
    }
    login_response = session.post(login_url, data=payload)

    # Check if login was successful
    if login_response.url == "https://stackoverflow.com/":
        print("Login successful!")
    else:
        print("Login failed. Please check your credentials or handle CAPTCHA.")

login_to_stackoverflow()