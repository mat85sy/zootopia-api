import json
import requests
# Import quote for URL encoding
from requests.utils import quote

# --- Configuration ---
TEMPLATE_FILE_PATH = 'animals_template.html'
OUTPUT_FILE_PATH = 'animals.html'
PLACEHOLDER = '__REPLACE_ANIMALS_INFO__'

# Your API details
API_KEY = 'Hv2dit0nihc91Uiy5MKKHQ==OhQp6cxuC983t8HC' # Your provided API key
API_BASE_URL = 'https://api.api-ninjas.com/v1/animals'
# --- End Configuration ---


def fetch_animal_data(animal_name):
    """Fetches animal data from the API Ninjas API."""
    # Encode the animal name for the URL (handles spaces, etc.)
    encoded_name = quote(animal_name)
    url = f"{API_BASE_URL}?name={encoded_name}"
    headers = {'X-Api-Key': API_KEY}

    try:
        print(f"Fetching data for '{animal_name}' from API...")
        response = requests.get(url, headers=headers)
        # Print status code for debugging
        # print(f"API Response Status Code: {response.status_code}")
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print(f"Successfully fetched data for '{animal_name}'.")
        return data

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
             # Not found is technically possible, though API usually returns [] for no results
            print(f"API reports 'Not Found' for '{animal_name}': {e}")
            return [] # Treat as no results for consistency
        else:
            print(f"HTTP Error fetching data from API for '{animal_name}': {e}")
            return None # Indicate a real error occurred
    except requests.exceptions.RequestException as e:
        print(f"Network Error fetching data from API for '{animal_name}': {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for '{animal_name}': {e}")
        return None


def serialize_animal(animal_obj):
    """Serializes a single animal dictionary into an HTML list item string."""
    output = '<li class="cards__item">\n'
    # Use .get() for safer access, provide a default if 'name' is missing
    output += f'<div class="card__title">{animal_obj.get("name", "Unknown Animal")}</div>\n'
    output += ' <div class="card__text">\n'
    output += ' <ul class="card__details">\n'

    # --- Display common characteristics ---
    characteristics_to_display = [
        ('Diet', 'diet'),
        ('Type', 'type'),
        ('Habitat', 'habitat'),
        ('Location(s)', 'locations'), # This is a list in the API
        ('Skin Type', 'skin_type'),
        ('Lifespan', 'lifespan')
        # Add more fields if desired
    ]

    for display_name, key in characteristics_to_display:
        if key == 'locations':
            locations_list = animal_obj.get('locations', [])
            if locations_list:
                value_str = ', '.join(locations_list)
                output += f'<li class="card__detail-item"><strong>{display_name}:</strong> {value_str}</li>\n'
        else:
            # Assume other keys are directly under 'characteristics'
            value = animal_obj.get('characteristics', {}).get(key)
            if value:
                output += f'<li class="card__detail-item"><strong>{display_name}:</strong> {value}</li>\n'

    output += '</ul>\n'
    output += '</div>\n'
    output += '</li>\n'
    return output


def generate_html_file(content_to_insert):
    """Reads the template, replaces the placeholder, and writes the output file."""
    try:
        with open(TEMPLATE_FILE_PATH, "r") as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{TEMPLATE_FILE_PATH}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred while reading the template file: {e}")
        return False

    try:
        final_html_content = template_content.replace(PLACEHOLDER, content_to_insert)
        with open(OUTPUT_FILE_PATH, "w") as output_file:
            output_file.write(final_html_content)
        return True
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}")
        return False


# --- Main Script Logic ---

# 1. Ask the user for the animal name
animal_name_input = input("Enter a name of an animal: ").strip()

# Check if the user entered something
if not animal_name_input:
    print("No animal name entered. Exiting.")
    exit(1)

# 2. Fetch the animal data from the API based on user input
animals_data = fetch_animal_data(animal_name_input)

# 3. Handle different outcomes from the API call
# Check if a real error occurred during the fetch (network issue, bad API key, etc.)
if animals_data is None:
    print(f"An error occurred while trying to retrieve data for '{animal_name_input}'. Please check your connection and API key. Exiting.")
    # Optionally, generate an error HTML page here too
    error_html_content = f"<h2 style='color:red;'>An error occurred while fetching data for '{animal_name_input}'. Please try again later.</h2>"
    if generate_html_file(error_html_content):
        print(f"An error page was generated at {OUTPUT_FILE_PATH}.")
    exit(1) # Exit with error code

# 4. Check if the API returned any results (empty list)
if not animals_data:
    # API returned an empty list [], meaning no animals matched the search term
    print(f"No animals found for '{animal_name_input}' in the API database.")
    # --- Generate HTML with the "doesn't exist" message ---
    # Escape the animal name for HTML safety (prevents issues if name contains <, >, &, etc.)
    escaped_animal_name = animal_name_input.replace("&", "&amp;").replace("<", "<").replace(">", ">").replace('"', "&quot;").replace("'", "&#x27;")
    no_results_html = f'<div style="text-align: center; padding: 20px;">\n'
    no_results_html += f'  <h2 style="color: #888;">The animal "{escaped_animal_name}" doesn\'t exist in our database.</h2>\n'
    no_results_html += f'  <p style="color: #aaa;">Please try searching for a different animal.</p>\n'
    no_results_html += f'</div>\n'
    # --- End Generate HTML ---

    if generate_html_file(no_results_html):
        print(f"Website was successfully generated to the file {OUTPUT_FILE_PATH}. (No results found)")
    else:
        print("Failed to generate the website file.")
    exit(0) # Exit successfully as the file was generated, just with a "no results" message

# 5. If we get here, animals_data contains results. Generate HTML for them.
print(f"Found {len(animals_data)} result(s) for '{animal_name_input}'.")

animals_info_string = ''
for animal in animals_data:
    animals_info_string += serialize_animal(animal)

if generate_html_file(animals_info_string):
    print(f"Website was successfully generated to the file {OUTPUT_FILE_PATH}.")
else:
    print("Failed to generate the website file.")
    exit(1)
