import csv
from geopy.geocoders import Nominatim

#list to contain Title and Description from rows of input file
#rowList = []

#List of headers for the output csv to be imported into MapBox
mapboxHeaders = ['Title', 'Description', 'Lat', 'Long']
#List of headers from input csv file that go into the description field of output csv file
descriptionHeaders = ['Goal', 'Status', 'Progress Detail', 'Challenges and barriers', 'Next Steps']

#Open the file using 'with' to make sure it closes no matter what, assign the opened file to the variable csvinput
with open('Georgetown_Import.ods_GT_Matrix.csv', 'r') as csvinput, open('GT_MapBox_Import1.csv', 'w') as csvoutput:

	#Create a dictionary reader to iterate through the rows of the input file, accessing by names in 1st row
	reader = csv.DictReader(csvinput)
	#Create a writer to write one row at a time to the output file
	writer = csv.writer(csvoutput, quoting=csv.QUOTE_MINIMAL)
	#Create a geocoder to geocode locations in Georgetowh, Seattle, WA
	geocoder = Nominatim(format_string="%s, Georgetown, Seattle WA")

	#Write the header row to the output csv
	writer.writerow(mapboxHeaders)
	
	#Iterate through rows of input file, and write a line to the output file for each one
	for row in reader:
		#Get the title string
		title = row['Title']
		#Only look at rows with nonempty Title field
		if title != "":
			#Create the description string from the desired columns of input file
			description = ""
			for header in descriptionHeaders:
				description += "<h2>%s</h2>\n<p>%s</p>\n" % (header, row[header])

			#Print for testing:
			print title
			print description

			#Set default latitude and longitude in case location can't be found
			lat = 0 #"44.666"
			lon = 0 #"-12.123"

			#Geocode the location from the 'Location' column -- increase timeout to 10s to avoid GeocoderTimedOut exception
			location = geocoder.geocode(row['Location'], timeout=10)
			#Get the latitude and longitude if a valid location was found
			if location != None:
				lat = location.latitude
				lon = location.longitude

			#Print for testing:
			print row['Location'] + ": (%f, %f)\n" %(lat, lon)

			writer.writerow([title, description, lat, lon])
