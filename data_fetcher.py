import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv('API_KEY')
# Basic check if the API key was loaded
if not API_KEY:
    print("WARNING: API_KEY not found in environment variables (.env file).")


API_BASE_URL = 'https://api.api-ninjas.com/v1/animals'


def fetch_data(animal_name):
    """
    Fetches animal data from the API Ninjas API.
    Returns a list of animal dictionaries, an empty list if none found, or None on error.
    """
    clean_name = animal_name.strip()
    if not clean_name:
        return []

    # Use quote directly from requests.utils
    encoded_name = requests.utils.quote(clean_name)
    url = f"{API_BASE_URL}?name={encoded_name}"
    headers = {'X-Api-Key': API_KEY}

    # Prevent making a request if the API key is definitely missing
    if not API_KEY:
        print(f"Error: No API key available. Cannot fetch data for '{clean_name}'.")
        return None

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return []
        else:
            print(f"HTTP error {response.status_code} for '{clean_name}': {e}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Problem connecting to the API for '{clean_name}': {e}")
        return None

    except json.JSONDecodeError as e:
        print(f"Bad response from API for '{clean_name}': {e}")
        return None

    encoded_name = quote(clean_name)
    url = f"{API_BASE_URL}?name={encoded_name}"
    headers = {'X-Api-Key': API_KEY}

    # Prevent making a request if the API key is definitely missing
    if not API_KEY:
        print(f"Error: No API key available. Cannot fetch data for '{clean_name}'.")
        return None

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return []
        else:
            print(f"HTTP error {response.status_code} for '{clean_name}': {e}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Problem connecting to the API for '{clean_name}': {e}")
        return None

    except json.JSONDecodeError as e:
        print(f"Bad response from API for '{clean_name}': {e}")
        return None
