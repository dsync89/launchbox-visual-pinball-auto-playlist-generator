import pandas as pd
import re
import sys

# Replace 'your_file.csv' with the actual path to your CSV file
csv_file_path = 'pinballxdatabase.csv'

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <THEME_TAG> <OUT_THEME_LIST_TXT")
        exit(1)
    else:
        # Extract command line arguments
        THEME_TAG = sys.argv[1]
        OUT_THEME_LIST_TXT = sys.argv[2]

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Define the keywords you want to filter themes on
    # keywords_to_select = ['Adult', 'TV Show', 'Sports', 'Movie']
    keywords_to_select = [ THEME_TAG ]

    # Fill NaN values in the 'Theme' column with an empty string
    df['Theme'] = df['Theme'].fillna('')

    # Filter rows based on whether the 'Theme' column contains any of the specified keywords
    filtered_df = df[df['Theme'].str.contains('|'.join(keywords_to_select))]

    # Remove duplicates based on all columns
    unique_filtered_df = filtered_df.drop_duplicates()

    # Extract the text before the first '(' in the 'Table Name (Manufacturer Year)' column using regex
    unique_filtered_df['New_Column'] = unique_filtered_df['Table Name (Manufacturer Year)'].apply(lambda x: re.search(r'^([^(]+)', x).group(1).strip())

    # Iterate over the unique themes and save each subset to a separate CSV file
    for keyword in keywords_to_select:
        # Filter rows for the current keyword
        keyword_filtered_df = unique_filtered_df[unique_filtered_df['Theme'].str.contains(keyword)]

        # Drop duplicates based on the 'Table Name' column to ensure uniqueness
        keyword_filtered_df = keyword_filtered_df.drop_duplicates(subset=['New_Column'])

        # Save the unique rows to a separate CSV file
        keyword_csv_file_path = f'vpx-theme-{keyword}.csv'
        
        # Save the DataFrame with the new column to CSV
        keyword_filtered_df.to_csv(keyword_csv_file_path, index=False)

        # Select only the last column and save to a text file
        # last_column_text_file_path = f'vpx-theme-{keyword}.txt'
        last_column_text_file_path = OUT_THEME_LIST_TXT
        keyword_filtered_df.iloc[:, -1].to_csv(last_column_text_file_path, header=False, index=False)

        print(f'Saved {len(keyword_filtered_df)} unique rows with keyword "{keyword}" to {keyword_csv_file_path}')
        print(f'Saved the last column to {last_column_text_file_path}')
