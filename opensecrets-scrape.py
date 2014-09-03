import requests
import bs4
import csv

url = 'https://www.opensecrets.org/indivs/search.php?&name=&employ=walmart&cand=&state=&cycle=All&soft=&zip=&sort=R&page=1'

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text)
rows = soup.find('div', id='tabwrap').tbody.find_all('tr')

output = []

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