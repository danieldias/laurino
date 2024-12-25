import json

# Load the JSON data
def load_data(file_path):
    with open('birth.json', 'r') as file:
        return json.load(file)

#Create Search Function
def search_records(data, surname, year_range=None):

    # Get the first letter of the surname (uppercase for consistency)
    first_letter = surname[0].upper()

    #Initialize results list
    results = []

    #if a specific year range is provided
    if year_range:
        # Check if the year range exists in the data
        if year_range not in data["birth"]:
            return f"Year range {year_range} not found"

        # Get the surnames records for the specified year range
        year_surnames = data["birth"][year_range]

        #Search within the specified year range
        for key, files in year_surnames.items():
            # Check if the letter matches a single letter or range
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