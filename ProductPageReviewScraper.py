from pprint import pprint
import BeautifulSoup
import requests
import re
import urllib
from lxml import html
from time import sleep
from random import randint
import psycopg2
import sys,traceback


def scrape(url):
    try:
        #db connection 
        con = psycopg2.connect("dbname='SenticNet' user='postgres' host='ec2-52-89-108-22.us-west-2.compute.amazonaws.com' password='swm123'")
        con.autocommit = True
        cur = con.cursor()
        #product url
        # url = 'http://www.amazon.com/dp/B0074R0Z3O'
        response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})

        soup = BeautifulSoup.BeautifulSoup(response.content)
        print '----->Product Title:',soup.find(id="productTitle").string
        tree = html.fromstring(response._content)

        #get the complete product information:
        # title - brand - price - desc  - rating - revcount
        prod_name = soup.find(id="productTitle").string                 #name
        prod_cost=soup.find(id='priceblock_ourprice').string[1:]            #price
        prod_brand = soup.find(id='brand').string                       #brand
        prod_rating = soup.find(id='acrPopover')['title'].split(' ')[0]         #rating
        rev_count =  soup.find(id='acrCustomerReviewText').string.split(' ')[0] #rev_count
        rev_count = rev_count.replace(',','')
        # print soup.find('div',{'id':'productDescription'})    #prod_desc
        prod_desc=''
        for tag in soup.find('div',{'id':'productDescription'}).findAll():
            prod_desc=prod_desc+" "+str(tag.string)
        prod_desc = ' '.join(prod_desc.split())

        #insert product info into DB
        try:
            cur.execute("INSERT INTO amazon_product(prod_brand,prod_name,prod_desc,prod_cost,prod_rating,rev_count,prod_url) VALUES(%s,%s,%s,%s,%s,%s,%s)",(prod_brand,prod_name,prod_desc,prod_cost,prod_rating,rev_count,url));
            #get the inserted tuple product id    
            cur.execute("SELECT currval(pg_get_serial_sequence('amazon_product','prod_id'))")
            prod_id =  cur.fetchall()[0]
            con.commit()
        except Exception as e:
            print '***** DBException',e
        try:
            #Get the reviews page link
            allreviewslink=soup.find('a',{'class':'a-link-emphasis a-nowrap'},href=True).get('href')
            response = requests.get(allreviewslink)
            soupAllRev=BeautifulSoup.BeautifulSoup(response.content)

            #get the current page number
            curReviewPage=soupAllRev.find('li',{'data-reftag':'cm_cr_pr_btm_link','class':"a-selected page-button"})
            curReviewPageNum=int(curReviewPage.find('a').contents[0])
            print '----->:',curReviewPageNum
            #get the last page numbercurReviewPage=soupAllRev.find('li',{'data-reftag':'cm_cr_pr_btm_link','class':"a-selected page-button"})
            for i in soupAllRev.findAll('li',{'data-reftag':'cm_cr_pr_btm_link'}):
                last=i.find('a').contents[0]
                totalreviewpages=int(last)
            print '=====> Total review pages:', totalreviewpages
            #GET TO THE REVIEW PAGE AND GATHER INFORMATION AND LOOP TILL LAST PAGE
            while(curReviewPageNum<=totalreviewpages or curReviewPageNum<=50):
                print '=====> current review page:', curReviewPageNum,'/',totalreviewpages
                reviewDivs =soupAllRev.findAll('div',{'class':'a-section review'})
                print len(reviewDivs)
                for divI in xrange(len(reviewDivs)):
                    try:
                        div=reviewDivs[divI]
                        rev_heading = div.find('a',{'class':"a-size-base a-link-normal review-title a-color-base a-text-bold"}).string
                        rev_url = div.find('a',{'class':"a-size-base a-link-normal review-title a-color-base a-text-bold"})['href']
                        rev_user =  div.find('a',{'class':"a-size-base a-link-normal author"}).string
                        # TODO: USER RANKING
                        # userURL = div.find('a',{'class':"a-size-base a-link-normal author"})['href']
                        # print userURL
                        # userPageResponse = requests.get("http://www.amazon.com"+userURL)
                        # userSoup = BeautifulSoup.BeautifulSoup(userPageResponse.content)
                        # print userSoup.find('div',{'class':'body'})
                        # userRanking = userSoup.find('span',{'class':'a-size-large a-text-bold'}).string[1:]
                        # print userRanking                    
                        # userTree = html.fromstring(userPageResponse._content);
                        # print tree.xpath('/html/body/div[2]/div[2]/div/div/div/div[1]/div/span[2]/div/div[3]/a/div/span')
                        review = div.find('span',{'class':'a-size-base review-text'}).string
                        review = ' '.join(review.split())
                        rev_date = div.find('span',{'class':'a-size-base a-color-secondary review-date'}).string[3:]
                        rev_rating = div.find('span',{'class':'a-icon-alt'}).string[:3]
                        cur.execute("INSERT INTO amazon_review(prod_id,review,rev_heading,rev_date,rev_user,rev_rating,rev_url) values (%s,%s,%s,%s,%s,%s,%s)",(prod_id,review,rev_heading,rev_date,rev_user,rev_rating,rev_url))
                        con.commit()
                        print '----------> Store rev_heading',rev_heading
                        sleep(randint(1,5))
                    except:
                        print '*************** Review Exception'
                        traceback.print_exc()
                        sleep(randint(1,5))
                nextPage = curReviewPage.findNext('li').a['href']
                nextPageResponse = requests.get("http://www.amazon.com"+nextPage)
                soupAllRev = BeautifulSoup.BeautifulSoup(nextPageResponse.content)
                curReviewPage=soupAllRev.find('li',{'data-reftag':'cm_cr_pr_btm_link','class':"a-selected page-button"})
                curReviewPageNum+=1
                sleep(randint(1,5))
        except KeyboardInterrupt:
            print "Goodbye!"
            sys.exit(0)
        except:
            print '********** Exception'
            traceback.print_exc()
    except KeyboardInterrupt:
                        print "Goodbye!"
                        sys.exit(0)
    except:
        print "***** Exception  ",traceback.print_exc();





        
