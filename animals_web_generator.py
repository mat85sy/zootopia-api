import json
import requests  # Step 1: Import requests

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
    url = f"{API_BASE_URL}?name={animal_name}"
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
    output += f'<div class="card__title">{animal_obj.get("name", "Unknown Animal")}</div>\n'
    output += ' <div class="card__text">\n'
    output += ' <ul class="card__details">\n'

    skin_type = animal_obj.get('characteristics', {}).get('skin_type')
    if skin_type:
        output += f'<li class="card__detail-item"><strong>Skin Type:</strong> {skin_type}</li>\n'

    diet = animal_obj.get('characteristics', {}).get('diet')
    if diet:
        output += f'<li class="card__detail-item"><strong>Diet:</strong> {diet}</li>\n'

    locations = animal_obj.get('locations', [])
    if locations:
        output += f'<li class="card__detail-item"><strong>Location:</strong> {locations[0]}</li>\n'

    animal_type = animal_obj.get('characteristics', {}).get('type')
    if animal_type:
        output += f'<li class="card__detail-item"><strong>Type:</strong> {animal_type}</li>\n'

    output += '</ul>\n'
    output += '</div>\n'
    output += '</li>\n'
    return output


# --- Main Script Logic ---

# 1. Fetch the animal data from the API (searching for "Fox")
animals_data = fetch_animal_data("Fox")

if animals_data is None:
    print("Failed to retrieve animal data. Exiting.")
    exit(1)

# 2. Extract unique skin_type values from the fetched data
skin_types_set = set()
for animal in animals_data:
    s_type = animal.get('characteristics', {}).get('skin_type')
    if s_type is not None:
        skin_types_set.add(s_type)

unique_skin_types = sorted(list(skin_types_set))

if not unique_skin_types:
    print("No animals with 'skin_type' found in the API response.")
    exit(1)

# 3. Display options to the user
print("\nAvailable skin types (from API data):")
for i, skin_type in enumerate(unique_skin_types, 1):
    print(f"{i}. {skin_type}")

# 4. Get user input and validate
selected_skin_type = None
while True:
    try:
        choice_input = input("\nEnter the number corresponding to the skin type: ")
        choice_index = int(choice_input) - 1
        if 0 <= choice_index < len(unique_skin_types):
            selected_skin_type = unique_skin_types[choice_index]
            print(f"You selected: {selected_skin_type}")
            break
        else:
            print("Invalid number. Please choose from the list.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)

# 5. Filter animals based on the selected skin_type
filtered_animals = [
    animal for animal in animals_data
    if animal.get('characteristics', {}).get('skin_type') == selected_skin_type
]

if not filtered_animals:
    print(f"No animals found with skin type '{selected_skin_type}' in the API data.")
    # Handle this case if needed. For now, proceed with empty list.


# 6. Generate the HTML string for the filtered animals
animals_info_string = ''
for animal in filtered_animals:
    animals_info_string += serialize_animal(animal)

# 7. Read the template file
try:
    with open(TEMPLATE_FILE_PATH, "r") as template_file:
        template_content = template_file.read()
except FileNotFoundError:
    print(f"Error: Template file '{TEMPLATE_FILE_PATH}' not found.")
    exit(1)

# 8. Replace placeholder and write the final HTML file
final_html_content = template_content.replace(PLACEHOLDER, animals_info_string)

with open(OUTPUT_FILE_PATH, "w") as output_file:
    output_file.write(final_html_content)

print(f"Generated {OUTPUT_FILE_PATH} successfully for skin type '{selected_skin_type}' using data from the API!")
