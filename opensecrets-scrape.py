import requests
import bs4
import csv
import urllib

initialParams = {
	'employ': 'walmart',
	'page': 1,
	'totalPages': 9999
}

header = ['Name', 'Zip', 'City and State', 'Employer', 'Date', 'Amount', 'Recipient']
output = []

baseurl = 'https://www.opensecrets.org/indivs/search.php?&name=&cand=&state=&cycle=All&soft=&zip=&sort=R&'
url = baseurl + urllib.urlencode(initialParams)

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text)
pages = soup.find('div', 'pageCtrl').find_all('a')
initialParams['totalPages'] = int(pages[len(pages)-2].contents[0])

print 'Retrieving ' + str(initialParams['totalPages']) + ' pages'

while (initialParams['page'] <= initialParams['totalPages']):
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

for line in output:
	address = str(line[1])[4:len(str(line[1]))-5].split('\xc2\xa0')
	line.pop(1)
	for x in address:
		line.insert(1, unicode(x))
	print line

output.insert(0, header)

with open('secrets.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile)
	for line in output:
		writer.writerow(line)