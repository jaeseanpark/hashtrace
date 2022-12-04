import requests
from bs4 import BeautifulSoup


#user agent string
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

url = ("https://github.com/EvanLi/Github-Ranking/blob/master/Top100/Top-100-stars.md")
res = requests.get(url, headers=headers)

#error handling
res.raise_for_status()

# parsing
with open("gitcrawling2.txt", "a", encoding="utf8") as f:
	soup = BeautifulSoup(res.text, 'html.parser')
	tds = soup.find_all('td')
	for td in tds:
		link = td.find('a')
		if link:
			f.write(link["href"])
			f.write('\n')


