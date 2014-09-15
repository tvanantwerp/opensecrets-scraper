import re
import requests
import bs4
import csv
import urllib

initialParams = {
	'employ': 'tax foundation',
	'page': 1
}

totalPages = 9999

header = ['First Name', 'Last Name', 'City', 'State', 'Zip', 'Employer', 'Date', 'Amount', 'Recipient']
output = []

baseurl = 'https://www.opensecrets.org/indivs/search.php?&name=&cand=&state=&cycle=All&soft=&zip=&sort=R&'
url = baseurl + urllib.urlencode(initialParams)

response = requests.get(url)

# Get the total number of pages of results for this query
soup = bs4.BeautifulSoup(response.text)
pages = soup.find('div', 'pageCtrl').find_all('a')
if pages != []:
	totalPages = int(pages[len(pages)-2].contents[0])
else:
	totalPages = 1

print 'Retrieving ' + str(totalPages) + ' pages'

# Retrieve all pages of results and parse into 'output'
while (initialParams['page'] <= totalPages):
	url = baseurl + urllib.urlencode(initialParams)
	response = requests.get(url)

	print 'Retrieving page ' + str(initialParams['page'])

	soup = bs4.BeautifulSoup(response.text)
	rows = soup.find('div', id='tabwrap').tbody.find_all('tr')

	for row in rows:
		tds = row('td')
		cells = []
		for td in tds:
			cells += td.contents
		output.append(cells)

	initialParams['page'] += 1

# Reformat messy data
for line in output:
	n = str(line[0])
	a = str(line[1])[4:len(str(line[1]))-5]
	if n.find(', ') == -1:
		names = [n, '']
	else:
		names = n.split(', ')
	addresses = re.split('\xc2\xa0|, ',a)
	del line[0:2]
	[line.insert(0, unicode(name)) for name in names]
	[line.insert(2, unicode(address)) for address in reversed(addresses)]

output.insert(0, header)

# Write csv
with open('secrets.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile)
	[writer.writerow(line) for line in output]