import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.atmovies.com.tw/movie/new/')

r.encoding = 'utf-8'

soup = BeautifulSoup(r.text, 'lxml')
filmTitle = soup.select('div.filmTitle a')

#print(filmTitle[0]['href'])
#print("http://www.atmovies.com.tw" + filmTitle[0]['href'])

'''
content = ''
for i in filmTitle:
	content += i.text + '\n' + "http://www.atmovies.com.tw" + i['href'] + '\n\n'
'''
content = ''
for index, i in enumerate(filmTitle):
	content += i.text + '\n' + "http://www.atmovies.com.tw" + i['href'] + '\n\n'
	if index >= 10: #回傳給使用者最多10筆資料
		break

print(content)