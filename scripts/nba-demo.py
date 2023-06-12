#! /usr/bin/python
import csv
import requests
from bs4 import BeautifulSoup

# Open the input file for reading
with open('input.txt', 'r') as input_file:
    # Read the lines of the input file
    search_terms = input_file.readlines()

# Initialize a list to store the search terms that don't have a table element
missing_tables = []

# Iterate through the search terms
for i, search_term in enumerate(search_terms):
    # Strip leading and trailing whitespace from the search term
    search_term = search_term.strip()
    # Replace spaces in the search term with a hyphen
    search_term = search_term.replace(' ', '-')

    # Construct the URL with the search term
    url = f'https://www.espn.com/nba/team/schedule/_/name/{search_term}/seasontype/2'

    # Make a request to the website
    response = requests.get(url)

    # Parse the HTML of the website
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table element in the HTML
    table = soup.find('table')

    # Check if the table element was found
    if table is None:
        # Add the search term to the list of missing tables
        missing_tables.append(search_term)
        # Skip to the next search term
        continue

    # Extract the rows of the table
    rows = table.find_all('tr')

    # Open a CSV file for writing
    with open(f'{search_term}.csv', 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Iterate through the rows
        for row in rows:
            # Extract the cells of the row
            cells = row.find_all('td')
            # Convert the cells to a list of strings
            cells = [cell.text for cell in cells]
            # Write the row to the CSV file
            writer.writerow(cells)

# Print the missing tables
print('The following search terms did not have a table element:')
for search_term in missing_tables:
    print(search_term)
