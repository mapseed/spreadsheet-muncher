from __future__ import print_function

# For reading and writing .csv files
import csv


# Attempting to keep it DRY and keep with pythonic formatting examples 
# given in gtscrapeSplit.py edits
IMPORT_CSV_FILE = 'data/Tracy-urbanwaters-working_v7_precall.ods_Master.csv'
# Feel free to rename the output csv:
EXPORT_CSV_FILE = 'iframe_result.csv'


# Output csv headers
MAPBOX_HEADERS = ['Title', 'Description', 'Lat', 'Long']
# Placeholder for URL to be inserted into iframe
URL = ""

# Open and create necessary csv files
with open(IMPORT_CSV_FILE, 'r') as csvinput,\
     open(EXPORT_CSV_FILE, 'w') as csvoutput:

    # Create a dictionary reader to iterate through the rows of the input file,
    # accessing by names in the first row
    reader = csv.DictReader(csvinput)

    # Create a dictionary writer for the output files, with MAPBOX_HEADERS
    # as the ordered list of keys
    writer = csv.DictWriter(csvoutput, MAPBOX_HEADERS, quoting = csv.QUOTE_MINIMAL)

    # Write MAPBOX_HEADERS as the first row of the output files
    writer.writeheader()

    # Iterate through rows of input file, and write a line to the output
    # file for each one
    for row in reader:
        # Ensure that only the locations with a URL will be processed
        if row['URL'] != 'n/a':
            # Get the title string
            title = row['Slug']

            # Get the URL
            URL = row['URL']

            # Get lat and lon
            lat = row['LAT']
            lon = row['LONG']

            # Build Description field
            description = "<iframe src='" + URL + "' width='100%' height='750' sandbox>\n \
                  <p>\n \
                    <!--Fallback link for browsers that, unlikely, don't support frames -->\n \
                    <a href= " + URL + " >\n \
                    </a>\n \
                  </p>\n \
                </iframe>"

            # Print for testing:
            print(title)
            print(URL)
            print(description)

            # Input values as a dictionary to ensure order of contents
            # in outputcsv
            writer.writerow({'Title': title, 'Description': description,
                        'Lat': lat, 'Long': lon})