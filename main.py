import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import schedule
import os
import time

load_dotenv()

def login_to_stackoverflow():
    # Credentials
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

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


# Schedule login once a day
schedule.every().day.at("01:27").do(login_to_stackoverflow)

# Keep script running
while True:
    schedule.run_pending()
    time.sleep(1)
