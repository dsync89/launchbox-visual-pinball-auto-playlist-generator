import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re
import sys
import uuid  # Import the uuid module
import shutil

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <PLAYLIST_NAME> <AUTO_POPULATED_LIST>")
        exit(1)
    else:
        # Extract command line arguments
        PLAYLIST_NAME = sys.argv[1]
        AUTO_POPULATED_LIST = sys.argv[2]
        LB_PLAYLIST_DIR = sys.argv[3]

    # Load the base XML file
    xml_file_path = 'base_playlist_pinball.xml'
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Generate a UUID for PlaylistId
    playlist_id_elem = root.find(".//PlaylistId")
    if playlist_id_elem is not None:
        playlist_id_elem.text = str(uuid.uuid4())  # Set PlaylistId to a new UUID

    # Set Playlist Name, Nested Name, and Sort Title to PLAYLIST_NAME
    playlist_name_elem = root.find(".//Name")
    nested_name_elem = root.find(".//NestedName")
    sort_title_elem = root.find(".//SortTitle")

    if playlist_name_elem is not None:
        playlist_name_elem.text = PLAYLIST_NAME

    if nested_name_elem is not None:
        nested_name_elem.text = PLAYLIST_NAME

    if sort_title_elem is not None:
        sort_title_elem.text = PLAYLIST_NAME

    # Read values from AUTO_POPULATED_LIST.txt and modify using regex
    with open(AUTO_POPULATED_LIST, 'r') as file:
        values = [re.search(r'^[^(]+', line).group(0).strip() for line in file]

    # Iterate through each modified value and append PlaylistFilter to the XML
    for value in values:
        playlist_filter = ET.Element('PlaylistFilter')

        value_elem = ET.SubElement(playlist_filter, 'Value')
        value_elem.text = value

        field_key_elem = ET.SubElement(playlist_filter, 'FieldKey')
        field_key_elem.text = 'Title'

        comparison_type_key_elem = ET.SubElement(playlist_filter, 'ComparisonTypeKey')
        comparison_type_key_elem.text = 'Contains'

        # Append the PlaylistFilter to the root element
        root.append(playlist_filter)

    # Add the last PlaylistFilter block before </LaunchBox>
    last_playlist_filter = ET.Element('PlaylistFilter')

    value_elem = ET.SubElement(last_playlist_filter, 'Value')
    value_elem.text = 'Visual Pinball'

    field_key_elem = ET.SubElement(last_playlist_filter, 'FieldKey')
    field_key_elem.text = 'Platform'

    comparison_type_key_elem = ET.SubElement(last_playlist_filter, 'ComparisonTypeKey')
    comparison_type_key_elem.text = 'Contains'

    root.append(last_playlist_filter)

    # Remove double quotes from 'Value' elements
    for value_element in root.iter('Value'):
        value_element.text = value_element.text.replace('"', '')

    # Save the modified XML to out.xml with formatting
    tree_str = ET.tostring(root, encoding='utf-8').decode('utf-8')
    xml_content = minidom.parseString(tree_str).toprettyxml(indent="  ")

    # Write the updated content back to PLAYLIST_NAME.xml
    output_file_path = f'{PLAYLIST_NAME}.xml'
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        out_file.write(xml_content)
        print(f'Generated playlist: {output_file_path}')

    # Copy to Launchbox Playlist folder
    try:
        # Copy the XML file from source to destination
        shutil.copy(output_file_path, LB_PLAYLIST_DIR)
        print(f"XML file successfully copied from {output_file_path} to {LB_PLAYLIST_DIR}")
    except FileNotFoundError:
        print("Error: Source file not found.")
    except PermissionError:
        print("Error: Permission denied. Make sure you have the necessary permissions.")
