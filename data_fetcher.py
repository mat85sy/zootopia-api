import json
import requests
from requests.utils import quote

API_KEY = 'Hv2dit0nihc91Uiy5MKKHQ==OhQp6cxuC983t8HC'
API_BASE_URL = 'https://api.api-ninjas.com/v1/animals'


def fetch_data(animal_name):
    """
    Fetches animal data from the API Ninjas API.
    Returns a list of animal dictionaries, an empty list if none found, or None on error.
    """
    clean_name = animal_name.strip()
    if not clean_name:
        return []

    encoded_name = quote(clean_name)
    url = f"{API_BASE_URL}?name={encoded_name}"
    headers = {'X-Api-Key': API_KEY}

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
