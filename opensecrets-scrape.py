import requests
import bs4
import csv
import urllib

initialParams = {
	'employ': 'walmart',
	'page': 1
}

totalPages = 1

output = []

baseurl = 'https://www.opensecrets.org/indivs/search.php?&name=&cand=&state=&cycle=All&soft=&zip=&sort=R&'
url = baseurl + urllib.urlencode(params)

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text)
rows = soup.find('div', id='tabwrap').tbody.find_all('tr')
pages = soup.find('div', 'pageCtrl').find_all('a')
totalPages = int(pages[len(pages)-2].contents[0])

for row in rows:
	tds = row('td')
	cells = []
	for td in tds:
		cells += td.contents
	output.append(cells)

with open('secrets.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile)
	for line in output:
		writer.writerow(line)