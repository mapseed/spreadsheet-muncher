import csv

#list to contain Title and Description from rows of input file
rowList = []

#Open the file using 'with' to make sure it closes no matter what, assign the opened file to the variable csvinput
with open('Georgetown_Import.ods_GT_Matrix.csv', 'r') as csvinput:
	#gtContents = csvfile.read()

	#Create a dictionary reader to iterate through the rows of the file, accessing by names in 1st row
	reader = csv.DictReader(csvinput)
	for row in reader:
		#Only look at rows with nonempty Title field
		if row['Title'] != "":
			#Extract the relevant data for the description, and store it to a string with html tags added
			descriptionStr = "<h2>Goal</h2>\n<p>%s</p>\n" % row['Goal']
			descriptionStr += "<h2>Status</h2>\n<p>%s</p>\n" % row['Status']
			descriptionStr += "<h2>Progress Detail</h2>\n<p>%s</p>\n" % row['Progress Detail']
			descriptionStr += "<h2>Challenges and Barriers</h2>\n<p>%s</p>\n" % row['Challenges and barriers']
			descriptionStr += "<h2>Next Steps</h2>\n<p>%s</p>" % row['Next Steps']
			#Append the title and description to the row list, stored as a tuple
			rowList.append((row['Title'], descriptionStr))
			print rowList[-1][0] #Print the title string
			print rowList[-1][1] + "\n" #Print the description string and an extra line

#print gtContents

#Open (or create) the output file and store to the variable csvoutput
with open('GT_MapBox_Import1.csv', 'w') as csvoutput:
	#Create a writer to write one row at a time to the file
	writer = csv.writer(csvoutput, quoting=csv.QUOTE_MINIMAL)
	#Write the header row
	writer.writerow(['Title', 'Description', 'Lat', 'Long'])
	#Write the contents of the current row in rowList, followed by fake values for 'Lat' and 'Long'
	for row in rowList:
		writer.writerow([row[0], row[1], 44.666, -122.123])
