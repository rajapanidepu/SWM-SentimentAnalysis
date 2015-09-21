from pprint import pprint
import BeautifulSoup
import requests
import re
import urllib
import csv
from time import sleep
from sets import Set
from random import randint
html=open("amazon.html",'r').read()
soup=BeautifulSoup.BeautifulSoup(html)
links=soup.find(id="ref_2528832011")
linksList=[]
# Getting all Links of all Phones
with open('links.csv', 'a') as fp:
    a = csv.writer(fp, delimiter=',')
    for link in links.findAll('a'):
        a.writerow([link.get('href'),link.contents[1].contents[0],link.contents[2].contents[0].split(";")[1].replace('(',"").replace(')',"")])
        linksList.append([link.get('href'),link.contents[1].contents[0],link.contents[2].contents[0].split(";")[1].replace('(',"").replace(')',"")])
print linksList[1][0]

for i in range(0,len(linksList)):
    sleep(randint(10,60))
    url=linksList[i][0]
    curPage=0
    totalPages=0
    if soup.find('span',{'class':'pagnCur'}):
        curPage = int(soup.find('span',{'class':'pagnCur'}).string)
    if soup.find('span',{'class':'pagnDisabled'}):
        totalPages = int(soup.find('span',{'class':'pagnDisabled'}).string)
        print curPage,'/',totalPages
    while(curPage<=totalPages):
        
        results = soup.find(id='s-results-list-atf').findAll('li')
        LinksinPage=[]
        for result in results:
            #sleep(10)
            LinksinPage.append(result.find('a',{'class':"a-link-normal s-access-detail-page  a-text-normal"},href=True).get('href'))
        for i in range(len(LinksinPage)):
            url=LinksinPage[i]
            response = requests.get(url)
            soup=BeautifulSoup.BeautifulSoup(response.content)
            allreviewslink=soup.find('a',{'class':'a-link-emphasis a-nowrap'},href=True)
            newurl=allreviewslink.get('href')
            sleep(randint(10,60))
            response = requests.get(newurl)
            soupAllRev=BeautifulSoup.BeautifulSoup(response.content)
            if soupAllRev.find('li',{'data-reftag':'cm_cr_pr_btm_link'}):
                curReviewPage=soupAllRev.find('li',{'data-reftag':'cm_cr_pr_btm_link'})
                print curReviewPage.find('a').contents[0]
                curReviewPage=curReviewPage.find('a').contents[0]
            if soupAllRev.findAll('li',{'data-reftag':'cm_cr_pr_btm_link'}):
                for i in soupAllRev.findAll('li',{'data-reftag':'cm_cr_pr_btm_link'}):
                    last=i.find('a').contents[0]
                    totalreviewpages=last
                print totalreviewpages
            while(curReviewPage<=totalreviewpages):
                review=[]
                #copying all review links to a list
                for div in soupAllRev.findAll('div',{'class':'a-section review'}):
                    full_page_review=div.find('a',{'class':'a-link-normal'},href=True)
                    sublink=full_page_review['href']
                    amazon='http://www.amazon.com'+str(sublink)
                    review.append(amazon)
                for j in range(len(review)):
                    FullReviewUrl=review[i]
                    response = requests.get(FullReviewUrl)
                    soupCustomerReview=BeautifulSoup.BeautifulSoup(response.content)
                    fullReview="".join(str(soupCustomerReview.find('div',{'class':'reviewText'}).contents))
                    fullReview=fullReview.replace("u'","")
                    
                    
                    
                totalreviewpages=totalreviewpages-1
        totalPages=totalPages-1   
                
        


    