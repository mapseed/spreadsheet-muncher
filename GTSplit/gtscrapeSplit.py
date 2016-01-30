#!/usr/bin/env python

from __future__ import print_function
from time import sleep
# For reading and writing .csv files
import csv
# If you want to change the geocoder from "GeocodeFarm" to something else,
# you only need to do it here since it's imported as farm_geocoder
from geopy.geocoders import GeocodeFarm as farm_geocoder
from geopy.geocoders import GoogleV3 as google_geocoder

IMPORT_CSV_FILE = 'data/Georgetown_Import.ods_GT_Matrix.csv'

# The bounding box of the viewport within which to bias geocode results
# more prominently (only on GoogleV3).
# http://bboxfinder.com/#47.506997,-122.349243,47.571198,-122.285385
GEOCODE_BOUNDING_BOX = (47.506997, -122.349243, 47.571198, -122.285385)
API_KEY = ''  # Only needed for lots of requests

# List of headers for the output csv to be imported into MapBox
# (these can be rearranged if desired)
MAPBOX_HEADERS = ['Title', 'Description', 'Lat', 'Long']

# List of headers from input csv file that go into the description field
# of output csv file.
# The code will still work if these headers are rearranged or
# different ones are chosen.
DESCRIPTION_HEADERS = ['Goal', 'Progress',
                       'Progress Detail',
                       'Challenges and barriers', 'Next Steps']

# The names of the studies
STUDY_NAMES = ["1977 Neighborhood Plan", "1995 Needs Assessment",
               "1998 Neighborhood Plan", "2007 Bicycle Master Plan",
               "2007 Airport Way Visioning", "2008 Duwamish Visioning"]


def splitting(targetCategory, short):
    # Open the files using 'with' to make sure they close no matter what,
    # assign the files to the variables csvinput, csvoutput
    with open(IMPORT_CSV_FILE, 'r') as csvinput,\
         open(short + '_complete.csv', 'w') as complete_output,\
         open(short + '_prog.csv', 'w') as prog_output,\
         open(short + '_no-prog-or-dead.csv', 'w') as no_prog_or_dead:
        # TODO: Categorize rows with 'Dead' progress into their own csv's:
        # open(short + 'Dead.csv', 'w') as Deadcsvoutput:

        # Create a dictionary reader to iterate through the rows of the
        # input file, accessing by names in 1st row
        reader = csv.DictReader(csvinput)

        # Create a dictionary writer for the output files, with MAPBOX_HEADERS
        # as the ordered list of keys
        complete_writer = csv.DictWriter(complete_output, MAPBOX_HEADERS,
                                    quoting=csv.QUOTE_MINIMAL)
        prog_writer = csv.DictWriter(prog_output, MAPBOX_HEADERS,
                                    quoting=csv.QUOTE_MINIMAL)
        no_prog_or_dead_writer = csv.DictWriter(no_prog_or_dead,
                                                MAPBOX_HEADERS,
                                                quoting=csv.QUOTE_MINIMAL)

        # Write MAPBOX_HEADERS as the 1st row of the output files
        complete_writer.writeheader()
        prog_writer.writeheader()
        no_prog_or_dead_writer.writeheader()
        # writerDead.writeheader()

        # Create a geocoder to geocode locations in Georgetown, Seattle, WA
        # GoogleV3 uses 'bounds' kwarg on geocode instead of 'format_string'
        # Increase timeout to 10s to avoid GeocoderTimedOut exception
        geocoder = google_geocoder(api_key=API_KEY, timeout=10)
        # geocoder = farm_geocoder(format_string="%s, Seattle WA", timeout=10)

        # Iterate through rows of input file, and write a line to the output
        # file for each one
        for row in reader:
            # Get the title string
            title = row['Slug']

            # Only look at rows with nonempty Title field
            if title != "" and row['Category'] == targetCategory:
                # Create the description string from the desired columns of
                # input file
                description = "<h1>%s</h1>\n" % (row['Title'])
                for header in DESCRIPTION_HEADERS:
                    description += "<h2>%s</h2>\n" % (header)
                    if row[header] != "":
                        description += "<p>%s</p>\n" % (row[header])
                    else:
                        description += "<p><em>%s</em></p>\n" % ('Unknown')

                # Add two blank lines, then a list of the studies for the
                # current item
                description += "<br><br>\n<h4>Study:</h4>\n<p>"
                for study in STUDY_NAMES:
                    # If the column for the current study is marked,
                    # add it to the description
                    if row[study] != "":
                        description += study + ", "

                # This if statement should always execute as long as every
                # row has at least one study, in which case the above for loop
                # added an extra ", " at the end, which we need to remove:
                # If the last two characters of the description are ", "
                # then remove them.
                if description[-2:] == ", ":
                    description = description[:-2]

                # Close the <p> tag for the studies, and add the contents of
                # the 'Category' column to the description
                description += "</p>\n<h5>Category:</h5>\n<p>" + \
                               row['Category'] + "</p>\n"

                # Print for testing:
                print(title)
                print(description)

                # while geocoding is commented out, these serve as a
                # lat and lon placeholders
                lat = row['Lat']
                lon = row['Long']

                if lat == '' or lon == '':
                    # Geocode the location from the 'Location' column
                    # GoogleV3 uses GEOCODE_BOUNDING_BOX
                    location = geocoder.geocode(row['Location'],
                                                bounds=GEOCODE_BOUNDING_BOX)
                    sleep(3)  # Limit our max requests/sec for geocoderservice
                    # If a valid location was found, get lat/long
                    # (i.e. location != None),
                    # and otherwise set the values to ''.
                    if location:
                        (lat, lon) = (location.latitude, location.longitude)
                    else:
                        (lat, lon) = ('', '')

                    # Print for testing:
                    print(row['Location'] + ": (%f, %f)\n" % (lat, lon))

                # Using a dictionary writer ensures that the row contents are
                # matched to the correct columns, even if headers are
                # rearranged
                # Sorting the data for values in 'Progress' column
                newRow = {'Title': title, 'Description': description,
                          'Lat': lat, 'Long': lon}

                # Write our new row to the appropriate CSV,
                # depending on the value of the row's 'Progress'
                {
                    'Complete': lambda x: complete_writer.writerow(x),
                    'In Progress': lambda x: prog_writer.writerow(x),
                    'No Progress': lambda x: no_prog_or_dead_writer.writerow(x),
                    'Dead': lambda x: no_prog_or_dead_writer.writerow(x)
                }[row['Progress']](newRow)

# For each category, we need to change these parameters with the target
# category and a shortened name for the csv file title
splitting('Quality of Life', 'qual')
splitting('Safety', 'safe')
splitting('Transportation', 'transp')
splitting('Parks and Open Space', 'parks')
splitting('Historic Preservation', 'hist')
splitting('Land Use', 'land')
