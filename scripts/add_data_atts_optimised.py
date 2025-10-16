import re
import csv
from datetime import datetime
from bs4 import BeautifulSoup

colors = {
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'END': '\033[0m'
}

def colored_print(message, color='GREEN'):
    color_code = colors.get(color.upper(), colors['GREEN'])
    print(f"{color_code}{message}{colors['END']}")

def read_csv_data(csv_file):
    data_dict = {}
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                key = row['data-name']  
                data_dict[key] = row
        colored_print(f"CSV data successfully read: {len(data_dict)} entries found.", 'GREEN')
    except Exception as e:
        colored_print(f"Error reading CSV file: {e}", 'RED')
    return data_dict

def remove_unwanted_data_attributes(tag):
    # List of data attributes that should be removed from <text> tags
    unwanted_attributes = [
        'data-default-value', 'data-description', 'data-form-type',
        'data-key', 'data-label', 'data-name', 'data-required', 'text-anchor','max-characters', 'data-type'
    ]
    
    # Remove the unwanted attributes from the tag if they exist
    for attr in unwanted_attributes:
        if attr in tag.attrs:
            del tag[attr]

def update_svg_with_data_atts(svg_content, csv_data):
    try:
        soup = BeautifulSoup(svg_content, 'xml')
        svgDoc = soup.find('svg')

        # Finding unique {{keys}} for text only within text content
        all_text = ' '.join([tag.get_text() for tag in svgDoc.find_all(['text', 'tspan'])])
        text_keys = set(re.findall(r'\{\{([^\}]+)\}\}', all_text))
        colored_print(f"Text Keys: {text_keys}", 'BLUE')

        # Remove unwanted attributes from <text> elements
        for text_tag in svgDoc.find_all('text'):
            remove_unwanted_data_attributes(text_tag)

        # Update only <tspan> elements with data attributes from CSV
        for key in sorted(text_keys, key=lambda x: (len(x), x)):  # Sort keys to handle longer keys first
            if key in csv_data:
                csv_row = csv_data[key]

                # Find only <tspan> elements, not <text>
                tspan_tags = svgDoc.find_all('tspan', string=re.compile(rf'\{{{{{key}}}}}'))

                for tag in tspan_tags:
                    # Skip if the tag already has 'data-default-value' attribute
                    if 'data-default-value' in tag.attrs:
                        continue

                    # Add attributes from CSV to the <tspan> tag only if they don't already exist
                    for attr_name, attr_value in csv_row.items():
                        if attr_value and attr_name not in tag.attrs:
                            tag[attr_name] = attr_value

        # Update image elements based on 'data-name' in the CSV
        for image_tag in svgDoc.find_all('image'):
            data_name = image_tag.get('data-name')
            if data_name and data_name in csv_data:
                csv_row = csv_data[data_name]
                for attr_name, attr_value in csv_row.items():
                    if attr_value:
                        image_tag[attr_name] = attr_value

        # Save modified SVG
        modified_svg = str(soup)
        output_filename = f"data_atts_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.svg"
        with open(output_filename, 'w') as f:
            f.write(modified_svg)

        colored_print(f"Modified SVG with data attributes has been saved to {output_filename}", 'GREEN')

    except Exception as e:
        colored_print(f"Error occurred during SVG processing: {e}", 'RED')


if __name__ == "__main__":
    file_path = '../campusLeaderCertificate/templateVariablesCampusLeaderCertificate.svg'
    csv_file = '../scripts/output_data.csv'  

    # Read the CSV data
    csv_data = read_csv_data(csv_file)

    # Load the SVG file
    with open(file_path, 'r') as f:
        current_svg = f.read()

    # Update SVG with CSV data attributes
    update_svg_with_data_atts(current_svg, csv_data)
