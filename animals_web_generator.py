import json
import data_fetcher

TEMPLATE_FILE_PATH = 'animals_template.html'
OUTPUT_FILE_PATH = 'animals.html'
PLACEHOLDER = '__REPLACE_ANIMALS_INFO__'


def serialize_animal(animal_obj):
    """Turns an animal dict into an HTML list item."""
    output = '<li class="cards__item">\n'
    output += f'<div class="card__title">{animal_obj.get("name", "Unknown Animal")}</div>\n'
    output += ' <div class="card__text">\n'
    output += ' <ul class="card__details">\n'

    # What to show
    characteristics_to_show = [
        ('Diet', 'diet'),
        ('Type', 'type'),
        ('Habitat', 'habitat'),
        ('Location(s)', 'locations'),
        ('Skin Type', 'skin_type'),
        ('Lifespan', 'lifespan')
    ]

    for label, key in characteristics_to_show:
        if key == 'locations':
            locations_list = animal_obj.get('locations', [])
            if locations_list:
                locations_str = ', '.join(locations_list)
                output += f'<li class="card__detail-item"><strong>{label}:</strong> {locations_str}</li>\n'
        else:
            value = animal_obj.get('characteristics', {}).get(key)
            if value:
                output += f'<li class="card__detail-item"><strong>{label}:</strong> {value}</li>\n'

    output += '</ul>\n'
    output += '</div>\n'
    output += '</li>\n'
    return output


def generate_html_file(content_to_insert):
    """Makes the final HTML file."""
    try:
        with open(TEMPLATE_FILE_PATH, "r") as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f"Template file '{TEMPLATE_FILE_PATH}' not found.")
        return False
    except Exception as e:
        print(f"Error reading template: {e}")
        return False

    try:
        final_html_content = template_content.replace(PLACEHOLDER, content_to_insert)
        with open(OUTPUT_FILE_PATH, "w") as output_file:
            output_file.write(final_html_content)
        return True
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False


# --- Main Script ---

if __name__ == "__main__":
    animal_name_input = input("Enter a name of an animal: ").strip()

    if not animal_name_input:
        print("No name entered. Exiting.")
        exit(1)

    print(f"Looking up '{animal_name_input}'...")
    animals_data = data_fetcher.fetch_data(animal_name_input)

    if animals_data is None:
        print(f"Failed to get data for '{animal_name_input}'.")
        error_msg = f"<h2 style='color:red;'>Couldn't fetch data for '{animal_name_input}'.</h2>"
        generate_html_file(error_msg)
        exit(1)

    if not animals_data:
        print(f"No animals found for '{animal_name_input}'.")
        safe_name = animal_name_input.replace("&", "&amp;").replace("<", "<").replace(">", ">")
        no_results_html = (
            f'<div style="text-align: center; padding: 20px;">\n'
            f'  <h2 style="color: #888;">The animal "{safe_name}" doesn\'t exist.</h2>\n'
            f'  <p style="color: #aaa;">Try a different animal.</p>\n'
            f'</div>\n'
        )
        generate_html_file(no_results_html)
        print(f"Website saved to {OUTPUT_FILE_PATH}.")
        exit(0)

    print(f"Found {len(animals_data)} animal(s).")
    animals_html_string = ''
    for animal in animals_data: # Fixed the loop variable
        animals_html_string += serialize_animal(animal)

    if generate_html_file(animals_html_string):
        print(f"Website was successfully generated to the file {OUTPUT_FILE_PATH}.")
    else:
        print("Failed to create the website.")
        exit(1)
