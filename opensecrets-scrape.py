import requests
import bs4

url = 'https://www.opensecrets.org/indivs/search.php?&name=&employ=walmart&cand=&state=&cycle=All&soft=&zip=&sort=R&page=1'

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text)
rows = soup.find('div', id='tabwrap').tbody.find_all('tr')

print rows