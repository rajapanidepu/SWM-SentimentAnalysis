#http://www.amazon.com/s/ref=sr_pg_15?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Aiphone%2Cp_89%3AApple&page=15&keywords=iphone&ie=UTF8&qid=1442374149


from pprint import pprint
import BeautifulSoup
import requests
from lxml import html
import re
import urllib
from time import sleep
from random import randint
import ProductPageReviewScraper as productScraper

# TODO url of list of products under a company
url = "http://www.amazon.com/s/ref=sr_in_-2_p_89_3?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A%212335753011%2Cn%3A7072561011%2Cp_89%3AApple&bbn=7072561011&ie=UTF8&qid=1442798627&rnid=2528832011"
# url = "http://www.amazon.com/s/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Aiphone%2Cp_89%3AApple&keywords=iphone&ie=UTF8&qid=1442374599"
response = requests.get(url)
soup = BeautifulSoup.BeautifulSoup(response.content)

curPage = int(soup.find('span',{'class':'pagnCur'}).string)
totalPages = int(soup.find('span',{'class':'pagnDisabled'}).string)

# while curPage <= totalPages:
currentPage = soup.find('span',{'class':'pagnCur'})

while curPage <= totalPages:
   tree = html.fromstring(response._content)
   items = tree.xpath('.//*/div/div[2]/div[1]/a/h2/text()')
   links = tree.xpath('.//*/div/div[2]/div[1]/a/h2/../../a/@href')

   for link in links:
       print '\nProduct:',link 
       productScraper.scrape(link)

   currentPage = soup.find('span',{'class':'pagnCur'})
   nextPage = currentPage.findNext('span')
   nextPageURL =  nextPage.a['href']
   response = requests.get("http://www.amazon.com"+nextPageURL)
   soup = BeautifulSoup.BeautifulSoup(response.content)
   curPage+=1
   sleep(randint(10,60))


