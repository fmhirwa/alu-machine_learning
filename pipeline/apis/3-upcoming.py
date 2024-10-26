#!/usr/bin/env python3

"""
Module to get information about the next SpaceX launch.
"""

import requests
from datetime import datetime

def get_upcoming_launch():

    """
    Retrieves and displays the upcoming SpaceX launch details.

    Prints:
        The launch name, date (local time), rocket name, and launchpad name with locality.

    Format:
        <launch name> (<date>) <rocket name> - <launchpad name> (<launchpad locality>)
    """
    
    url = "https://api.spacexdata.com/v4/launches/upcoming"
    response = requests.get(url)
    
    if response.status_code == 200:
        launches = response.json()
        # Sort launches by date_unix to get the soonest launch
        next_launch = min(launches, key=lambda launch: launch['date_unix'])
        
        # Extract and format the launch details
        launch_name = next_launch.get("name", "Unknown launch")
        launch_date = datetime.fromtimestamp(next_launch["date_unix"]).strftime("%Y-%m-%d %H:%M:%S")
        rocket_id = next_launch["rocket"]
        launchpad_id = next_launch["launchpad"]
        
        # Fetch rocket name
        rocket_response = requests.get(f"https://api.spacexdata.com/v4/rockets/{rocket_id}")
        rocket_name = rocket_response.json().get("name", "Unknown rocket") if rocket_response.status_code == 200 else "Unknown rocket"
        
        # Fetch launchpad details
        launchpad_response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}")
        if launchpad_response.status_code == 200:
            launchpad_data = launchpad_response.json()
            launchpad_name = launchpad_data.get("name", "Unknown launchpad")
            launchpad_locality = launchpad_data.get("locality", "Unknown locality")
        else:
            launchpad_name = "Unknown launchpad"
            launchpad_locality = "Unknown locality"
        
        # Print the formatted launch information
        print(f"{launch_name} ({launch_date}) {rocket_name} - {launchpad_name} ({launchpad_locality})")
    else:
        print("Unable to retrieve SpaceX launch information.")

if __name__ == "__main__":
    get_upcoming_launch()
