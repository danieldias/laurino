import json
import os


# Load the JSON data
def load_data(file_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(dir_path, file_path)
    with open(full_path, 'r') as file:
        return json.load(file)


def search_records(data, surname, year_range=None, links_data=None):
    # Get the first letter of the surname (uppercase for consistency)
    first_letter = surname[0].upper()

    # Use a list to preserve order, and a set to track duplicates
    results = []
    processed_files = set()  # Set to prevent duplicates
    years_found = set()  # Store unique years

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

            # Check if the user-provided range overlaps with the data range
            if not (end_year < range_start or start_year > range_end):
                for year in range(max(start_year, range_start), min(end_year, range_end) + 1):
                    for key, files in surnames.items():
                        if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                            for file in files:
                                if file not in processed_files:
                                    results.append(file)  # Preserve order
                                    processed_files.add(file)  # Prevent duplicates
                            years_found.add(year)

    else:
        # If no year range is provided, search across all years
        for range_key, year_surnames in data['birth'].items():
            try:
                if "-" in range_key:
                    range_start, range_end = map(int, range_key.split('-'))
                    for year in range(range_start, range_end + 1):
                        for key, files in year_surnames.items():
                            if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                                for file in files:
                                    if file not in processed_files:
                                        results.append(file)  # Preserve order
                                        processed_files.add(file)  # Prevent duplicates
                                years_found.add(year)
                else:
                    year = int(range_key)
                    for key, files in year_surnames.items():
                        if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                            for file in files:
                                if file not in processed_files:
                                    results.append(file)  # Preserve order
                                    processed_files.add(file)  # Prevent duplicates
                            years_found.add(year)
            except ValueError:
                continue  # Skip invalid formats

    # After collecting results, get links for the years found
    antenati_results = []
    if links_data:
        for year in sorted(years_found):  # Sort years to keep chronological order
            if str(year) in links_data:
                antenati_results.append({'year': year, 'link': links_data[str(year)]})

    return results, antenati_results
