#For reading and writing .csv files
import csv
#If you want to change the geocoder from "GeocodeFarm" to something else,
#you only need to do it here since it's imported as myCoder
from geopy.geocoders import GeocodeFarm as myCoder

#List of headers for the output csv to be imported into MapBox (these can be rearranged if desired)
mapboxHeaders = ['Title', 'Description', 'Lat', 'Long']
#List of headers from input csv file that go into the description field of output csv file.
#The code will still work if these headers are rearranged or different ones are chosen.
descriptionHeaders = ['Goal', 'Status', 'Progress Detail', 'Challenges and barriers', 'Next Steps']
#The names of the studies
studyNames = ["1977 Neighborhood Plan","1995 Needs Assessment","1998 Neighborhood Plan","2007 Bicycle Master Plan","2007 Airport Way Visioning","2008 Duwamish Visioning"]

#Open the files using 'with' to make sure they close no matter what, assign the files to the variables csvinput, csvoutput
with open('Georgetown_Import.ods_GT_Matrix.csv', 'r') as csvinput, open('GT_MapBox_Import2.csv', 'w') as csvoutput:

	#Create a dictionary reader to iterate through the rows of the input file, accessing by names in 1st row
	reader = csv.DictReader(csvinput)
	#Create a dictionary writer for the output file, with mapboxHeaders as the ordered list of keys
	writer = csv.DictWriter(csvoutput, mapboxHeaders, quoting=csv.QUOTE_MINIMAL)
	#Write mapboxHeaders as the 1st row of the output file
	writer.writeheader()

	#Create a geocoder to geocode locations in Georgetown, Seattle, WA
	geocoder = myCoder(format_string="%s, Seattle WA")
	
	#Iterate through rows of input file, and write a line to the output file for each one
	for row in reader:
		#Get the title string
		title = row['Title']
		#Only look at rows with nonempty Title field
		if title != "":
			#Create the description string from the desired columns of input file
			description = ""
			for header in descriptionHeaders:
				if row[header] != "":
					description += "<h2>%s</h2>\n<p>%s</p>\n" % (header, row[header])

			#Add two blank lines, then a list of the studies for the current item
			description += "<br><br>\n<h4>Study:</h4>\n<p>"
			for study in studyNames:
				#If the column for the current study is marked, add it to the description
				if row[study] != "":
					description += study + ", "

			#This if statement should always execute as long as every row has at least one study,
			#in which case the above for loop added an extra ", " at the end, which we need to remove:
			#If the last two characters of the description are ", " then remove them.
			if description[-2:] == ", ":
				description  = description[:-2]

			#Close the <p> tag for the studies, and add the contents of the 'Category' column to the description
			description += "</p>\n<h5>Category:</h5>\n<p>" + row['Category'] + "</p>\n"

			#Print for testing:
			print title
			print description

			#Geocode the location from the 'Location' column -- increase timeout to 10s to avoid GeocoderTimedOut exception
			location = geocoder.geocode(row['Location'], timeout=10)
			#Get the latitude and longitude if a valid location was found (i.e. location != None), 
			#and otherwise set the values to 0.
			(lat, lon) = (location.latitude, location.longitude) if location else (0, 0) #(47.55,-122.33)

			#Print for testing:
			print row['Location'] + ": (%f, %f)\n" %(lat, lon)

			#Using a dictionary writer ensures that the row contents are matched to the correct columns, even if headers are rearranged
			writer.writerow({'Title':title, 'Description':description, 'Lat':lat, 'Long':lon})
