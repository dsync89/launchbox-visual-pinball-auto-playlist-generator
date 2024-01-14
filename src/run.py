import json
import subprocess

def run_gen_theme_unique_table_names(theme, theme_txt_file):
    script_path = 'gen_theme_unique_table_names.py'
    try:
        subprocess.run(["python3", script_path, theme, theme_txt_file])
    except FileNotFoundError:
        print(f"File '{script_path}' not found.") 

def run_gen_manufacturer_unique_table_names(manufacturer, theme_txt_file):
    script_path = 'gen_manufacturer_unique_table_names.py'
    try:
        subprocess.run(["python3", script_path, manufacturer, theme_txt_file])
    except FileNotFoundError:
        print(f"File '{script_path}' not found.")         

def run_gen_lb_playlist_and_copy_to_lb_playlist_dir(playlist_name, auto_populated_list, LB_PLAYLIST_DIR):
    script_path = 'gen_lb_playlist_xml.py'
    try:
        subprocess.run(["python3", script_path, playlist_name, auto_populated_list, LB_PLAYLIST_DIR])
    except FileNotFoundError:
        print(f"File '{script_path}' not found.") 

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":


    # Read JSON data from the file
    with open('.\config.json', 'r') as file:
        json_data = json.load(file)

    LB_PLAYLIST_DIR = json_data['launchbox']['playlist_dir']

    # Iterate through each element in "platforms"
    # for playlist in json_data['playlists_by_theme']:
    #     theme = playlist['theme']
    #     playlist_name = playlist['lb_playlist_name']
    #     theme_txt_file = playlist['theme_txt_file']

    #     print("Theme: ", theme)
    #     print("Playlist Name: ", playlist_name)
    #     print("Theme TXT File: ", theme_txt_file)

    #     # Generate per theme table names
    #     print("Generate unique table names for themes based on pinballx csv file downloaded from https://virtual-pinball-spreadsheet.web.app/ ")
    #     run_gen_theme_unique_table_names(theme, theme_txt_file)  
    
    #     # Generate Launchbox playlist xml
    #     run_gen_lb_playlist_and_copy_to_lb_playlist_dir(playlist_name, theme_txt_file, LB_PLAYLIST_DIR)

    for playlist in json_data['playlists_by_manufacturer']:
        manufacturer = playlist['manufacturer']
        playlist_name = playlist['lb_playlist_name']
        unique_table_txt_file = playlist['unique_table_txt_file']

        print("Manufacturer: ", manufacturer)
        print("Playlist Name: ", playlist_name)
        print("Unique Table TXT File: ", unique_table_txt_file)

        # Generate per manufacturer table names
        print("Generate unique table names for manufacturer based on pinballx csv file downloaded from https://virtual-pinball-spreadsheet.web.app/ ")
        run_gen_manufacturer_unique_table_names(manufacturer, unique_table_txt_file)  
    
        # Generate Launchbox playlist xml
        run_gen_lb_playlist_and_copy_to_lb_playlist_dir(playlist_name, unique_table_txt_file, LB_PLAYLIST_DIR)        

    print("All done!")