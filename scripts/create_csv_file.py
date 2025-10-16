import csv
import re
from bs4 import BeautifulSoup

# Function to convert camelCase or snake_case to a readable format
def generate_data_label(data_name):
    # Split camelCase into words, e.g., 'addressLine1' -> 'Address Line 1'
    words = re.sub('([a-z])([A-Z])', r'\1 \2', data_name)
    # Convert snake_case to space-separated, e.g., 'address_line_1' -> 'Address Line 1'
    words = re.sub(r'(_)', ' ', words)
    # Capitalize the first letter of each word
    return words.title()

# Helper function to handle special image tags like qr.png, logo.png, etc.
def handle_image_data(data_name):
    if data_name == 'qr.png':
        return {
            'data-key': data_name,
            'data-label': data_name,
            'data-form-type': '',  # Keep it empty for qr.png
            'data-type': '',  # Leave empty for qr.png
            'max-size': '',  # Empty for qr.png
            'data-description': '',  # No description for image elements
            'data-qr-type': 'gradient',  # Set for qr.png
            'data-qr-style': 'extra-rounded',
            'data-qr-color1': '#000000',
            'data-qr-color2': '#000000'
        }
    else:
        # Handle other images like logo.png, photo.png, etc.
        data_key_label = data_name.replace('.png', '')  # For logo.png, return 'logo'
        return {
            'data-key': data_key_label,
            'data-label': data_key_label.capitalize(),  # Capitalize for readability
            'data-form-type': 'template',
            'data-type': data_key_label,  # Set 'logo', 'photo', etc.
            'max-size': '2500kb',  # Default size
            'data-description': ''  # No description for image elements
        }

def extract_text_data_from_svg(svg_content):
    soup = BeautifulSoup(svg_content, 'xml')
    svgDoc = soup.find('svg')

    # Initialize the list to store CSV rows and a set to track added data-names
    csv_rows = []
    image_rows = []  # Separate list for image rows
    added_data_names = set()

    # Find all tspan, text, and image tags, prioritize tspan over text
    tspan_tags = svgDoc.find_all('tspan')
    text_tags = svgDoc.find_all('text')
    image_tags = svgDoc.find_all('image')  # For handling image elements

    # Helper function to create a row
    def create_row(data_name, data_type=''):
        is_image = data_type == 'image'
        
        # Set data-form-type to 'template' for non-image elements
        data_form_type = '' if is_image else 'template'
        data_type_value = 'image' if is_image else 'textField'
        data_required = 'False' if is_image else 'True'
        data_description = f"Enter the {data_name}" if not is_image else ''
        
        return {
            'data-name': data_name,
            'data-key': data_name,
            'data-label': generate_data_label(data_name),  # Generate readable label
            'data-form-type': data_form_type,
            'data-default-value': '',
            'data-type': data_type_value,  # Set data-type to 'textField' or 'image'
            'data-required': data_required,  # Set data-required to 'True' for all except image
            'data-description': data_description,  # Set "Enter the {data-key}" description
            'max-characters': '',
            'data-format': '',
            'text-anchor': '',
            'max-size': '2500kb' if is_image else '',
            'data-qr-type': '',
            'data-qr-color1': '',
            'data-qr-color2': ''
        }

    # Process tspan tags first
    for tspan_tag in tspan_tags:
        data_name = re.search(r'\{\{(.+?)\}\}', tspan_tag.text)
        if data_name:
            data_name = data_name.group(1)
            if data_name not in added_data_names:
                csv_rows.append(create_row(data_name))
                added_data_names.add(data_name)

    # Process text tags (if not already added by tspan)
    for text_tag in text_tags:
        data_name = re.search(r'\{\{(.+?)\}\}', text_tag.text)
        if data_name:
            data_name = data_name.group(1)
            if data_name not in added_data_names:
                csv_rows.append(create_row(data_name))
                added_data_names.add(data_name)

    # Process image tags and extract their data-name attribute
    for image_tag in image_tags:
        data_name = image_tag.get('data-name')
        if data_name and data_name not in added_data_names:
            # Handle image rows using helper function
            image_data = handle_image_data(data_name)
            row = create_row(data_name, 'image')
            row.update(image_data)  # Update the row with specific image data
            image_rows.append(row)
            added_data_names.add(data_name)

    # Sort rows by data-name in natural order (for correct ordering like maxCredit1, maxCredit2, etc.)
    def natural_sort_key(row):
        return [int(text) if text.isdigit() else text for text in re.split('(\d+)', row['data-name'])]

    csv_rows.sort(key=natural_sort_key)

    # Append image rows at the end
    csv_rows.extend(image_rows)

    return csv_rows

def write_csv(csv_filename, rows):
    fieldnames = ['data-name', 'data-key', 'data-label', 'data-form-type', 'data-default-value', 'data-type', 
                  'data-required', 'data-description', 'max-characters', 'data-format', 'text-anchor', 
                  'max-size', 'data-qr-type', 'data-qr-style', 'data-qr-color1', 'data-qr-color2']

    try:
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"CSV successfully created: {csv_filename}")
    except Exception as e:
        print(f"Error writing CSV file: {e}")

if __name__ == "__main__":
    svg_file_path = '../campusLeaderCertificate/templateVariablesCampusLeaderCertificate.svg'
    output_csv_file = '../scripts/output_data.csv'

    # Read the SVG content
    with open(svg_file_path, 'r') as svg_file:
        svg_content = svg_file.read()

    # Extract data from the SVG content
    csv_data = extract_text_data_from_svg(svg_content)

    # Write the data to a CSV file
    write_csv(output_csv_file, csv_data)