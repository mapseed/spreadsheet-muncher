#!/usr/bin/env python

from __future__ import print_function
import csv
from lxml import html
import requests

# # Names of the input and output csv files
IMPORT_CSV_FILE = 'import.csv'
EXPORT_CSV_FILE = 'export.csv'

URL_HEADER = 'CONTACT_WEBSITE'
CONTACT_ORGANIZATION_HEADER = 'CONTACT_ORGANIZATION'
ORGANIZATIONS_HEADER = 'ORGANIZATIONS'
DESCRIPTION_HEADER = 'PROJECT_DESCRIPTION'


def processAllRows(inFileName, outFileName):
    """

    Function to read through the input csv,
    merge rows with the same Location ID,
    and write the merged rows to the output csv

    """

    with open(inFileName, 'r') as csvinput,\
         open(outFileName, 'w') as csvoutput:

        reader = csv.DictReader(csvinput)
        fieldnames = reader.fieldnames
        print("fieldnames:", fieldnames)
        writer = csv.DictWriter(csvoutput, fieldnames)
        writer.writeheader()
        for row in reader:
            updateRowFromURL(row)
            writer.writerow(row)


def updateRowFromURL(row):
    """
    If there is a link, add the link's description, contact organization,
    and organizations attributes to the description column.
    If the row already has that attribute, don't add that row's attribute.
    """
    url = row[URL_HEADER]
    if (not url):
        return

    page = requests.get(url)
    tree = html.fromstring(page.content)
    description = tree.xpath('//span[@id="DESCRIPTION"]/text()')
    # description = tree.xpath('//span[@id="ENTITIES"]/div/ul/li//text()')

    # Update the description:
    if (row[DESCRIPTION_HEADER] == '' or
        row[DESCRIPTION_HEADER] == '_' or
       row[DESCRIPTION_HEADER] == ' '):
        if (len(description) > 0):
            row[DESCRIPTION_HEADER] = description[0]
        else:
            print("No description at url:", url)

    # Update the organizations:
    organizations = tree.xpath('//span[@id="ENTITIES"]/div/ul/'
                               'li/descendant-or-self::*/text()')
    if (len(organizations) == 0):
        print("No organization at url: \n", url)
        return

    contact = organizations[0]  # first item is always the contact organization
    if (row[ORGANIZATIONS_HEADER] == ''):
        # organizations = tree.xpath('//span[@id="ENTITIES"]/'
        # 'descendant-or-self::*/text()')
        organizations = set(organizations)  # removes duplicates
        organizations = ', '.join(organizations)
        row[ORGANIZATIONS_HEADER] = organizations

    # Update the contact organization:
    if (row[CONTACT_ORGANIZATION_HEADER] == ''):
        row[CONTACT_ORGANIZATION_HEADER] = contact

    return

if __name__ == '__main__':
    processAllRows(IMPORT_CSV_FILE, EXPORT_CSV_FILE)
