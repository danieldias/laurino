import json
import os


# Load the JSON data
def load_data(file_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(dir_path, file_path)
    with open(full_path, 'r') as file:
        return json.load(file)


# Create Search Function
def search_records(data, surname, year_range=None):
    # Get the first letter of the surname (uppercase for consistency)
    first_letter = surname[0].upper()

    # Initialize results list
    results = []

    # If a specific year range is provided
    if year_range:
        try:
            if "-" in year_range:
                start_year, end_year = map(int, year_range.split('-'))
            else:
                start_year = end_year = int(year_range)

        except ValueError:
            return "Invalid year range or year format. Please use YYYY-YYYY or YYYY."

        # Iterate over the year ranges in the JSON data
        for range_key, surnames in data['birth'].items():
            try:
                range_start, range_end = map(int, range_key.split('-'))
            except ValueError:
                continue  # Skip if the format is wrong
            # Check for overlap between the user-provided range and the JSON range
            if not (end_year < range_start or start_year > range_end):
                for key, files in surnames.items():
                    # Check if the letter matches a single letter or a range
                    if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                        results.extend(files)

    else:
        # Search across all year ranges if no specific year range is provided
        for year, year_surnames in data['birth'].items():
            for key, files in year_surnames.items():
                # Check if the letter matches a single letter or a range
                if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                    results.extend(files)

    # Return the search results
    if results:
        return results
    else:
        return f"No records found for surname starting with '{first_letter}'."