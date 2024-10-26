#!/usr/bin/env python3
"""
Module to count the number of SpaceX launches per rocket.
"""

import requests
from collections import defaultdict

def get_launches_per_rocket():
    """
    Retrieves and displays the number of launches per SpaceX rocket.

    Each line is formatted as:
        <rocket name>: <launch count>

    Results are sorted by launch count (descending), and alphabetically for ties.
    """
    launches_url = "https://api.spacexdata.com/v4/launches"
    rockets_url = "https://api.spacexdata.com/v4/rockets"

    # Fetch all launches and rockets
    launches_response = requests.get(launches_url)
    rockets_response = requests.get(rockets_url)

    if launches_response.status_code == 200 and rockets_response.status_code == 200:
        launches = launches_response.json()
        rockets = rockets_response.json()

        # Create a dictionary mapping rocket IDs to names
        rocket_name_map = {rocket["id"]: rocket["name"] for rocket in rockets}

        # Count launches per rocket
        launch_counts = defaultdict(int)
        for launch in launches:
            rocket_id = launch["rocket"]
            rocket_name = rocket_name_map.get(rocket_id, "Unknown Rocket")
            launch_counts[rocket_name] += 1

        # Sort rockets by launch count (descending) and alphabetically if tied
        sorted_launch_counts = sorted(
            launch_counts.items(),
            key=lambda item: (-item[1], item[0])
        )

        # Print the formatted result
        for rocket_name, count in sorted_launch_counts:
            print("{}: {}".format(rocket_name, count))
    else:
        print("Unable to retrieve SpaceX data.")

if __name__ == "__main__":
    get_launches_per_rocket()
