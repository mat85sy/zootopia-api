import json
import requests

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
    encoded_name = requests.utils.quote(animal_name)
    url = f"{API_BASE_URL}?name={encoded_name}"
    headers = {'X-Api-Key': API_KEY}

    try:
        print(f"Fetching data for '{animal_name}' from API...")
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print(f"Successfully fetched data for '{animal_name}'.")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None


def serialize_animal(animal_obj):
    """Serializes a single animal dictionary into an HTML list item string."""
    output = '<li class="cards__item">\n'
    # Use .get() for safer access, provide a default if 'name' is missing
    output += f'<div class="card__title">{animal_obj.get("name", "Unknown Animal")}</div>\n'
    output += ' <div class="card__text">\n'
    output += ' <ul class="card__details">\n'

    # --- Display common characteristics ---
    # You can add more fields here as needed
    characteristics_to_display = [
        ('Diet', 'diet'),
        ('Type', 'type'), # Note: API uses 'type', JSON used 'group' sometimes
        ('Habitat', 'habitat'),
        ('Location(s)', 'locations'), # This is a list in the API
        ('Skin Type', 'skin_type'), # Added Skin Type as requested in previous steps
        # Add more fields if desired, e.g., ('Lifespan', 'lifespan')
    ]

    for display_name, key in characteristics_to_display:
         # Handle nested keys like 'locations' or 'characteristics.skin_type'
        if key == 'locations':
             # Get the list of locations
            locations_list = animal_obj.get('locations', [])
            if locations_list:
                # Join the list items, e.g., "North-America, Europe"
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


# --- Main Script Logic ---

# 1. Ask the user for the animal name
animal_name_input = input("Enter a name of an animal: ").strip()

# Check if the user entered something
if not animal_name_input:
    print("No animal name entered. Exiting.")
    exit(1)

# 2. Fetch the animal data from the API based on user input
animals_data = fetch_animal_data(animal_name_input)

# Check if data was fetched successfully
if animals_data is None:
    print(f"Failed to retrieve data for '{animal_name_input}'. Exiting.")
    exit(1)

# Check if the API returned any results
if not animals_data:
     # API returned an empty list []
    print(f"No animals found for '{animal_name_input}' in the API database.")
    # Create an HTML file indicating no results
    no_results_html = f"<h2>No animals found for '{animal_name_input}'.</h2>"
    try:
        with open(TEMPLATE_FILE_PATH, "r") as template_file:
            template_content = template_file.read()
        final_html_content = template_content.replace(PLACEHOLDER, no_results_html)
        with open(OUTPUT_FILE_PATH, "w") as output_file:
            output_file.write(final_html_content)
        print(f"Website was successfully generated to the file {OUTPUT_FILE_PATH}. (No results found)")
    except FileNotFoundError:
        print(f"Error: Template file '{TEMPLATE_FILE_PATH}' not found.")
    except Exception as e:
        print(f"An error occurred while generating the file: {e}")
    exit(0) # Exit successfully as the file was generated, just with a "no results" message


# 3. Generate the HTML string for ALL animals returned by the API
animals_info_string = ''
for animal in animals_data:
    animals_info_string += serialize_animal(animal)

# 4. Read the template file
try:
    with open(TEMPLATE_FILE_PATH, "r") as template_file:
        template_content = template_file.read()
except FileNotFoundError:
    print(f"Error: Template file '{TEMPLATE_FILE_PATH}' not found.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the template file: {e}")
    exit(1)

# 5. Replace placeholder and write the final HTML file
try:
    final_html_content = template_content.replace(PLACEHOLDER, animals_info_string)
    with open(OUTPUT_FILE_PATH, "w") as output_file:
        output_file.write(final_html_content)
    print(f"Website was successfully generated to the file {OUTPUT_FILE_PATH}.")
except Exception as e:
    print(f"An error occurred while writing the output file: {e}")
    exit(1)
