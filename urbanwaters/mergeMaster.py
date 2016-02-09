from __future__ import print_function
from collections import Counter
import csv

#Names of the input and output csv files
IMPORT_CSV_FILE = 'Tracy-urbanwaters-working_v7_precall.csv' #'Tracy-urbanwaters-working_v7_precall.ods_Master.csv'
OUTPUT_CSV_FILE = 'Tracy-urbanwaters-merged.csv'

#Headers for both input and output files
HEADERS = ["#", "STATUS", "Location ID",
			"Title", "Address", "ORGANIZATIONS",
			"LAT", "LONG", "PROJECT_DESCRIPTION",
			"PROJECT_DATE", "END_DATE","Id",
			"Source", "URL", "Slug"]

#Default values indicating that data for a column is unavailable
DEFAULT_ORG = "{{Unlisted}}"
DEFAULT_ID = "{{unlisted}}"
DEFAULT_LAT = "47.5"
DEFAULT_LONG = "-122.3"
DEFAULT_URL = "n/a"

#Each row of output will have a unique identifier in colum '#',
#starting with the following number and increasing 
FIRST_NUMBER = 257

#Function to read through the input csv, merge rows with the same Location ID,
#and write the merged rows to the output csv
def crunchCSV(inFileName, outFileName):

	with open(inFileName, 'r') as csvinput,\
		 open(outFileName, 'w') as csvoutput:

		reader = csv.DictReader(csvinput, HEADERS)
		# Create a dictionary writer for the output files, with HEADERS
	    # as the ordered list of keys
		writer = csv.DictWriter(csvoutput, HEADERS)
		#Write HEADERS as the 1st row of the output file
		writer.writeheader()


		#Version 3 of reading through input file: 
		#Make it more like a do loop, and make iteration more explicit
		
		#Control flow boolean to keep track of whether we've reached end of input file
		end_of_csvinput = False

		#Number the output rows consecutively starting with FIRST_NUMBER
		newRowNum = FIRST_NUMBER

		#Various counters to help with debugging the while loop that reads the file
		row_count = 0 #The number of rows we've read
		#To count # of groups of matching rows that have a given size
		row_group_counter = Counter()
		#To count 
		id_counter = Counter()

		#Try reading the header row and first row of data
		try:
			print("Header row:", reader.next().values(), "\n") #first row should contain headers
			currentRow = reader.next() #2nd row is first row of data
			currentID = currentRow['Location ID'] #store the ID for future use
			row_count += 1 #Start counting rows of data
			print("1st row, row count: %i\n" % row_count)
		except StopIteration:
			end_of_csvinput = True
			print("File is empty or contains only headers.")

		while(not end_of_csvinput):

			#Create a list to store the current row and the matching rows to be merged
			rows = [currentRow]

			#Try reading the next row. As long as a next row exists and its ID matches
			#that of the current row, continue adding rows to the list.
			try:
				nextRow = reader.next()
				nextID = nextRow['Location ID']
				row_count += 1
				#print("current, row count: %i\n" % row_count)
				while (nextID == currentID):
					rows.append(nextRow)
					nextRow = reader.next()
					nextID = nextRow['Location ID']
					row_count += 1
					#print("additional, row count: %i\n" % row_count)
			except StopIteration:
				end_of_csvinput = True #currentRow contains the last ID in the file
				print("end of input, row count: %i\n" % row_count)

			#Record how many matching rows there were in this group,
			#for testing purposes
			row_group_counter[len(rows)] += 1

			#Alert user if more than 2 rows match
			if (len(rows) > 2):
				print("\n%i rows match Location ID %s.\n" % (len(rows), currentID))

			newRow = mergeRows(rows, newRowNum) #newRow should be a dictionary
			if (newRow != None):
				writer.writerow(newRow)
			else:
				print("%i rows match Location ID %s:" % (len(rows), currentID))
				for row in rows:
					print(row, '\n')

			
			# print("Histogram of # of matching rows:", row_group_counter)
			# print("row count: %i\n" % row_count)
			# #print("Number of distinct decimal ID's = %i" % sum(row_group_counter.values()))
			# print("Number of distinct ID's = %i" % sum(row_group_counter.values()))
			# print("Computed number of rows = %i\n" % sum([ k*v for (k,v) in row_group_counter.iteritems()]))

			currentRow = nextRow
			currentID = currentRow['Location ID']
			newRowNum += 1

		print("Histogram for size of row groups:", row_group_counter)
		print("row count: %i" % row_count)
		print("Number of distinct ID's = %i" % sum(row_group_counter.values()))
		print("Computed number of rows = %i\n" \
			% sum([ k*v for (k,v) in row_group_counter.iteritems()]))
		print('Final row number:', newRowNum-1)
		print('Last row number+1 - first row number:', newRowNum - FIRST_NUMBER)

# HEADERS = ["#", "STATUS", "Location ID",
# 			"Title", "Address", "ORGANIZATIONS",
# 			"LAT", "LONG", "PROJECT_DESCRIPTION",
# 			"PROJECT_DATE", "END_DATE","Id",
# 			"Source", "URL", "Slug"]

#rows = a list of rows (each a dictionary), rowNumber = number to assign the new row
def mergeRows(rows, rowNumber):
	numRows = len(rows)
	#Create a new row identical to the first row in list
	newRow = rows[0].copy()
	#Change newRow's number to the new value
	newRow['#'] = rowNumber
	if (numRows == 1):
		return newRow
	#elif (numRows == 2):
	else:
		#do something interesting...
		newRow['STATUS'] = selectContent('STATUS', rows)
		newRow['Title'] = selectContent('Title', rows, \
			test=lambda row: row['Source']=='B')
		newRow['Address'] = selectContent('Address', rows)
		newRow['ORGANIZATIONS'] = selectContent('ORGANIZATIONS', rows, \
			default_val=DEFAULT_ORG)
		newRow['LAT'] = selectContent('LAT', rows, \
			default_val=DEFAULT_LAT)
		newRow['LONG'] = selectContent('LONG', rows, \
			default_val=DEFAULT_LONG)
		newRow['PROJECT_DESCRIPTION'] = selectContent('PROJECT_DESCRIPTION', rows)
		newRow['PROJECT_DATE'] = selectContent('PROJECT_DATE', rows)
		newRow['END_DATE'] = selectContent('END_DATE', rows)
		newRow['Id'] = selectContent('Id', rows, \
			default_val=DEFAULT_ID)
		#newRow['Source'] = ???
		newRow['URL'] = selectContent('URL', rows, \
			default_val=DEFAULT_URL)
		#newRow['Slug'] = selectContent('Slug', rows)
		return newRow
	# else:
	# 	#Not sure how to handle multiple rows yet...
	# 	#Return None for now to indicate a special case
	# 	return None

#Choose one of two (or multiple) rows for the given header
def selectContent(header, rows, test='dominant', default_val = "", empty_is_ok=False):
	if test == 'dominant':
		test = lambda row: row[header] != default_val
		empty_is_ok=True

	matches = [row for row in rows if test(row)]

	if (empty_is_ok and len(matches) == 0):
		return default_val

	if (len(matches) != 1):
		print("%i matches for '%s' in Location ID %s:" \
			% (len(matches), header, rows[0]['Location ID']))
		print("List of all %i row[%s]'s:\n" % (len(rows), header), [row[header] for row in rows], "\n")
		print("%i matches:\n" % len(matches), [row[header] for row in matches],"\n")
		if (len(matches) == 0):
			return ""
	
	#If there is one or more match, the first is returned
	return matches[0][header]

crunchCSV(IMPORT_CSV_FILE, OUTPUT_CSV_FILE)


