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

    # Initialize results set (to avoid duplicates)
    results = set()
    years_found = set()  # Set to store the years found based on the search

    # If a specific year range is provided
    if year_range:
        try:
            # If it's a range, split and convert to integers
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
                # Iterate through each year in the overlapping range
                for year in range(max(start_year, range_start), min(end_year, range_end) + 1):
                    # Process the surnames directly for the current range
                    for key, files in surnames.items():
                        # Check if the first letter of the surname matches
                        if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                            results.update(files)  # Add files for the matching surname
                            years_found.add(year)  # Store the matching year

    else:
        # If no year range is provided, search across all years
        for range_key, year_surnames in data['birth'].items():
            try:
                # Handle year ranges or single years
                if "-" in range_key:
                    range_start, range_end = map(int, range_key.split('-'))
                    # Iterate through all years in the range
                    for year in range(range_start, range_end + 1):
                        # Process the surnames directly for the current range
                        for key, files in year_surnames.items():
                            # Check if the first letter of the surname matches
                            if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                                results.update(files)
                                years_found.add(year)
                else:
                    # Handle individual years (not ranges)
                    year = int(range_key)
                    for key, files in year_surnames.items():
                        if first_letter == key or ("-" in key and key.split("-")[0] <= first_letter <= key.split("-")[1]):
                            results.update(files)
                            years_found.add(year)
            except ValueError:
                continue  # Skip invalid formats

    # After collecting the results, get links for the years found
    if links_data:
        antenati_results = []  # List to store the year links
        for year in years_found:
            if str(year) in links_data:
                # Add the year and corresponding link to antenati_results
                antenati_results.append({'year': year, 'link': links_data[str(year)]})
        return list(results), antenati_results  # Convert results back to a list

    # Return the results and empty links if no links data is provided
    return list(results), []
