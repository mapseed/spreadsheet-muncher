from __future__ import print_function
from collections import Counter
import csv


IMPORT_CSV_FILE = 'Tracy-urbanwaters-working_v7_precall.ods_Master.csv'
OUTPUT_CSV_FILE = 'Tracy-urbanwaters-merged.csv'

HEADERS = ["#", "STATUS", "Location ID",
			"Title", "Address", "ORGANIZATIONS",
			"LAT", "LONG", "PROJECT_DESCRIPTION",
			"PROJECT_DATE", "END_DATE","Id",
			"Source", "URL", "Slug"]

FIRST_NUMBER = 257

def mergeRows(inFileName, outFileName):

	with open(inFileName, 'r') as csvinput,\
		 open(outFileName, 'w') as csvoutput:

		reader = csv.DictReader(csvinput, HEADERS)
		# Create a dictionary writer for the output files, with HEADERS
	    # as the ordered list of keys
		writer = csv.DictWriter(csvoutput, HEADERS)
		#Write HEADERS as the 1st row of the output file
		writer.writeheader()

		#rows = []

		#Version 1: I think this will skip over rows because the for loop automatically iterates
		# for row in reader:

		# 	# rows.append(row)
		# 	# if (nextRow exists):
		# 	# 	nextRow = reader.next()
		# 	# while (nextRow and nextRow['Location ID'] == row['Location ID']):
		# 	# 	rows.append(nextRow)
		# 	# 	nextRow = reader.next() if nextRow exists else None

		# 	#Create a list to store the current row and all subsequent rows to be merged
		# 	rows = [row]
		# 	#Try reading more rows - if the location id matches the current row,
		# 	#add them to the list. If there are no more rows, do nothing.
		# 	try:
		# 		nextRow = reader.next()
		# 		while (nextRow['Location ID'] == row['Location ID']):
		# 			rows.append(nextRow)
		# 			nextRow = reader.next()
		# 	except StopIteration:
		# 		#No more rows: Do nothing, and continue with remaining code
		# 		pass

		# 	print("Number of matching rows = %i\n" % len(rows))
		# 	print(str(rows) + "\n")

		# #Version 2: I think this fixes the 'skipping over rows' problem
		# currentRow = None
		# for row in reader:

		# 	#Create a list to store the current row and all subsequent rows to be merged
		# 	rows = [currentRow]
		# 	nextRow = row
		# 	#Try reading more rows - if the location id matches the current row,
		# 	#add them to the list. If there are no more rows, do nothing.
		# 	while (currentRow && nextRow['Location ID'] == currentRow['Location ID']):
		# 		try:
		# 			rows.append(nextRow)
		# 			nextRow = reader.next()
		# 		except StopIteration:
		# 			#No more rows: Break out of loop
		# 			break

		# 	print(rows)

		# 	currentRow = nextRow


		#Version 3: Make it more like a do loop, and make iteration more explicit
		end_of_csvinput = False
		row_count = 0
		match_hist = Counter()

		#Try reading the header row and first row of data
		try:
			print("Header row:", reader.next().values(), "\n") #first row should contain headers
			currentRow = reader.next() #2nd row is first row of data
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
				row_count += 1
				print("current, row count: %i\n" % row_count)
				while (nextRow['Location ID'] == currentRow['Location ID']):
					rows.append(nextRow)
					nextRow = reader.next()
					row_count += 1
					print("additional, row count: %i\n" % row_count)
			except StopIteration:
				end_of_csvinput = True #currentRow contains the last ID in the file
				print("end of input, row count: %i\n" % row_count)

			match_hist[len(rows)] += 1

			print("# of matching rows:", len(rows))
			for row in rows:
				print(row)

			
			print("Histogram of # of matching rows:", match_hist)
			print("row count: %i\n" % row_count)
			print("Number of distinct ID's = %i" % sum(match_hist.values()))
			print("Computed number of rows = %i\n" % sum([ k*v for (k,v) in match_hist.iteritems()]))

			currentRow = nextRow





mergeRows(IMPORT_CSV_FILE, OUTPUT_CSV_FILE)


