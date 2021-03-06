# -*- coding: utf-8 -*-
import os
import re
import requests
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse
import urllib
from time import sleep
from random import randint

# Set up variables
entity_id = "E3001_NCC_gov"
url = "http://www.opendatanottingham.org.uk/dataset.aspx?id=21"
errors = 0
# Set up functions
def validateFilename(filename):
    filenameregex = '^[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+_[0-9][0-9][0-9][0-9]_[0-9][0-9]$'
    dateregex = '[0-9][0-9][0-9][0-9]_[0-9][0-9]'
    validName = (re.search(filenameregex, filename) != None)
    found = re.search(dateregex, filename)
    if not found:
        return False
    date = found.group(0)
    year, month = int(date[:4]), int(date[5:7])
    now = datetime.now()
    validYear = (2000 <= year <= now.year)
    validMonth = (1 <= month <= 12)
    if all([validName, validYear, validMonth]):
        return True
def validateURL(url):
    validURL = 200
    validFiletype = '.csv'
    return validURL, validFiletype

def convert_mth_strings ( mth_string ):

    month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
    #loop through the months in our dictionary
    for k, v in month_numbers.items():
#then replace the word with the number

        mth_string = mth_string.replace(k, v)
    return mth_string
# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

# find all entries with the required class
block = soup.find('table', 'downloadTable')
links = block.findAll('a', href=True)
for link in links:
    url = link['href']
    csvfile = link.text.strip().split('-')
    csvYr = csvfile[0]
    csvMth = csvfile[-1][:2]
    filename = entity_id + "_" + csvYr + "_" + csvMth
    todays_date = str(datetime.now())

    file_url = url.strip()
    validFilename = validateFilename(filename)
    validURL, validFiletype = validateURL(file_url)
    if not validFilename:
        print filename, "*Error: Invalid filename*"
        print file_url
        errors += 1
        continue
    if not validURL:
        print filename, "*Error: Invalid URL*"
        print file_url
        errors += 1
        continue
    if not validFiletype:
        print filename, "*Error: Invalid filetype*"
        print file_url
        errors += 1
        continue
    scraperwiki.sqlite.save(unique_keys=['l'], data={"l": file_url, "f": filename, "d": todays_date })
    print filename
if errors > 0:
    raise Exception("%d errors occurred during scrape." % errors)
