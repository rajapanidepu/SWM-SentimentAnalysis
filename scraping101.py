from pprint import pprint
import BeautifulSoup
import requests
import re
import urllib

print "Kranthi"
#product url
url = 'http://www.amazon.com/dp/B0074R0Z3O'
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})

soup = BeautifulSoup.BeautifulSoup(response.content)
print soup.find(id="productTitle").string

#preparing dic to store info
dic={}
dic['title'] = soup.find(id="productTitle").string

#array of reviews : MOST helpful reviews
reviewURLarr=[]
for div in soup.findAll(id=re.compile('^rev-dpReviewsMostHelpfulAUI-.*')):
	for reviewURL in div.findAll('a',{"class": "a-link-normal a-text-normal a-color-base" },href=True):
		reviewURLarr.append(str(reviewURL['href']))
print len(set(reviewURLarr))

#getting into review url and grabing the data
revdic={}
for reviewURL in set(reviewURLarr):
	# print reviewURL
	reviewResponse = requests.get(reviewURL, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
	reviewSoup = BeautifulSoup.BeautifulSoup(reviewResponse.content)
	tag = reviewSoup.findAll('div',{"style":"margin-bottom:0.5em;"})[1]
	print '-->',tag.b.string
	revdic['revTitle']=tag.b.string
	revdic['review']=reviewSoup.findAll('div',{"class":"reviewText"})
	revdic['helpfulness']=reviewSoup.findAll('div',{"style":"margin-bottom:0.5em;"})[0].string.strip()
	revdic['ratings'] = tag.find('span').find('img')['title']
	revdic['date'] = tag.find('nobr').string
	revdic['user'] reviewSoup.findAll('div',{"style":"margin-bottom:0.5em;"})[2].find('span',{'style':"font-weight: bold;"}).string
