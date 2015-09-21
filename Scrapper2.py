'''
Created on Sep 19, 2015

@author: system
'''
'''
Created on Sep 19, 2015

@author: system
'''
from pprint import pprint
import BeautifulSoup
import requests
import re
import urllib
from random import randint
from time import sleep
from sets import Set
html=open("amazon1.html",'r').read()
soup=BeautifulSoup.BeautifulSoup(html)
allreviewslink=soup.find('a',{'class':'a-link-emphasis a-nowrap'},href=True)

newurl=allreviewslink.get('href')

html1=open("allreviews.html",'r').read()
soupAllRev=BeautifulSoup.BeautifulSoup(html1)

curPage=soupAllRev.find('li',{'data-reftag':'cm_cr_pr_btm_link'})
print curPage.find('a').contents[0]
curPage=curPage.find('a').contents[0]
for i in soupAllRev.findAll('li',{'data-reftag':'cm_cr_pr_btm_link'}):
    last=i.find('a').contents[0]
totalpages=last
print totalpages
html2=open("customerReview.html").read()
'''
#onereview=soupAllRev.findAll(id='cm_cr-review_list')
# Retrieving whole Review

soupCustomerReview=BeautifulSoup.BeautifulSoup(html2)
fullReview="".join(str(soupCustomerReview.find('div',{'class':'reviewText'}).contents))
fullReview=fullReview.replace("u'","")

#----------------

soupusefulRev=BeautifulSoup.BeautifulSoup(html2)
useful=soupusefulRev.find('div', {'style':'margin-left:0.5em;'}).find('div',{'style':'margin-bottom:0.5em;'})
useful= "".join(useful.contents).replace("u'","").replace("[","").replace("]","").replace("  ","")
Peopleinfluenced=useful.split(" ")[0]
TotalNoofPeople=useful.split(" ")[2]
#------------------------------------------------------------------------
'''
''' All links of full reviews in a page
review=[]
for div in soupAllRev.findAll('div',{'class':'a-section review'}):
    #print div
    full_page_review=div.find('a',{'class':'a-link-normal'},href=True)
    sublink=full_page_review['href']
    amazon='http://www.amazon.com'+str(sublink)
    review.append(amazon)

print review
'''
'''Product Description"
product_Description=soup.find('div',{'id':'productDescription'})
pd=""
for text in  product_Description.findAll('p'):
    #print type(text)
    pd=pd+str(text.contents)
print pd.replace("[]","").replace("[","").replace("]","").replace("u'","").replace("  ","")
productDec=pd

'''