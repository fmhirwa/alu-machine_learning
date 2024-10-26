#!/usr/bin/env python3


""" Return list of ships"""

import requests
import sys
from datetime import datetime

def get_user_location(user_url):
    """
    Retrieves and prints the location of a specific GitHub user.

    Args:
        user_url (str): Full API URL of the GitHub user.

    Returns:
        None
    """
    response = requests.get(user_url)
    if response.status_code == 200:
        user_data = response.json()
        print(user_data.get("location", "Location not specified"))
    elif response.status_code == 404:
        print("Not found")
    elif response.status_code == 403:
        reset_time = datetime.fromtimestamp(int(response.headers.get("X-Ratelimit-Reset", 0)))
        minutes_until_reset = (reset_time - datetime.now()).total_seconds() // 60
        print(f"Reset in {int(minutes_until_reset)} min")
    else:
        print("Unexpected error")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./2-user_location.py <GitHub user API URL>")
    else:
        get_user_location(sys.argv[1])
