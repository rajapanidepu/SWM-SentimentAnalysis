#http://www.amazon.com/s/ref=sr_pg_15?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Aiphone%2Cp_89%3AApple&page=15&keywords=iphone&ie=UTF8&qid=1442374149


from pprint import pprint
import BeautifulSoup
import requests
import re
import urllib


url = "http://www.amazon.com/s/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Aiphone%2Cp_89%3AApple&keywords=iphone&ie=UTF8&qid=1442374599"
print url
response = requests.get(url)

soup = BeautifulSoup.BeautifulSoup(response.content)
curPage = int(soup.find('span',{'class':'pagnCur'}).string)
totalPages = int(soup.find('span',{'class':'pagnDisabled'}).string)
print curPage,'/',totalPages
# while curPage <= totalPages:
currentPage = soup.find('span',{'class':'pagnCur'})
print currentPage
while curPage <= totalPages:
	results = soup.find(id='s-results-list-atf')
	# for li in results:
	# 	print li['id']
	print len(results.findAll('li')),' - ' ,soup.find('span',{'class':'pagnDisabled'}).string
	nextPage = currentPage.findNext('span')
	nextPageURL =  nextPage.a['href']
	response = requests.get(url)
	soup = BeautifulSoup.BeautifulSoup(response.content)
	curPage+=1
	




# http://www.amazon.com/s/ref=sr_hi_2?rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Aiphone&keywords=iphone&ie=UTF8&qid=1442465611
# http://www.amazon.com/s/ref=sr_pg_2?rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Aiphone&page=2&keywords=iphone&ie=UTF8&qid=1442465616
# http://www.amazon.com/s/ref=sr_pg_3?rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Aiphone&page=3&keywords=iphone&ie=UTF8&qid=1442467326