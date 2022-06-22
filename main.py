import smtplib
import requests
from datetime import datetime
import time
import os

MY_LAT = 5.603717  # Your latitude
MY_LONG = -0.186964  # Your longitude
MY_EMAIL = os.environ['gmail_account']
MY_PASS = os.environ['gmail_key']


def is_iss_above_me():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_data = response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.

    lat_diff = min(abs(MY_LAT - iss_latitude), abs(MY_LAT + iss_latitude))
    long_diff = min(abs(MY_LONG - iss_longitude), abs(MY_LONG + iss_longitude))

    if lat_diff <= 5 and long_diff <= 5:
        return True
    else:
        return False


def is_night_at_my_location():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sun_data = response.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    time_hour = time_now.hour

    return time_hour >= sunset or time_now <= sunrise


def send_mail():
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(MY_EMAIL, MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="MY_EMAIL",
            msg="Subject:Look Up NOW\n\nThe ISS is above you now")


while True:
    if is_iss_above_me() and is_night_at_my_location():
        send_mail()

    time.sleep(300)
