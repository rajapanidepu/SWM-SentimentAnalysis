# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:49:39 2015

This script is to scrape all the categories in the Download.com site.
I have written this code in a way that a category can be controlled and scraped. Few changes that should be made for having different categories selected are
--> #while iteratorForSoftware < len(firstPageCategories):      	Should uncomment this if all the categories should be run at the sametime
--> iteratorForSoftware = __ 						(One can fill the number of category that should be scraped here)
--> while iteratorForSoftware < __: 					(One can restrict the number of categories starting from the number mentioned above)
--> pageCounter=0 							(By default it is set to 0, one can update this to scrape only desired pages)
--> fileToWrite = "C:\Users\mmaddula\Desktop\NetworkingSoftware.csv" 	(Location of file into which the output should be written)

@author: mmaddula
"""

import urllib
import re
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep

# FIRST LEVEL
htmlfileForTool = urllib.urlopen("http://download.cnet.com/windows/?tag=hdr")
htmltextForTool = htmlfileForTool.read()
htmlfileForTool.close()
soup = BeautifulSoup("".join(htmltextForTool))
catFlyList = soup.find("dl",{"class":"catNav catFly"})
#print catFlyList
try:
    Hier2CatList = str(catFlyList)
except IndexError:
    Hier2CatList = 'null'
#print Hier2CatList
regex = '<dd> <a href="(.+?)">(.+?)</a> <div class="catFlyout">'
pattern = re.compile(regex)
firstPageCategories = re.findall(pattern,Hier2CatList)
iteratorForSoftware = 7

# SECOND LEVEL
#while iteratorForSoftware < len(firstPageCategories):      Should uncomment this if everything has to be run at the sametime
while iteratorForSoftware < 8:
    #print firstPageCategories[iteratorForSoftware][0]
    urlForCategory = firstPageCategories[iteratorForSoftware][0]
    if urlForCategory[0] != 'h':
        urlForCategory = "http://download.cnet.com"+urlForCategory
    print urlForCategory
    #print firstPageCategories[iteratorForSoftware][1]
    
    pageLink = ""
    htmlfileForSecondLevel = urllib.urlopen(urlForCategory)
    htmltextForSecondLevel = htmlfileForSecondLevel.read()
    regex = '<a href="(.+?)2.html">2</a>'
    pattern = re.compile(regex)
    commonPageLink = re.findall(pattern,htmltextForSecondLevel)
    pageLink = "http://download.cnet.com"+commonPageLink[0]
    
    
    regex = '<a href="'+commonPageLink[0]+'(.+?).html">(.+?)</a>'
    pattern = re.compile(regex)
    pageNumberList = re.findall(pattern,htmltextForSecondLevel)
    lastPageNumber = (pageNumberList[2])[0]
    print lastPageNumber
    
    currentPageNumber = 1
    pagesToVisit = []
    while currentPageNumber <= int(lastPageNumber):
        eachPageLink = pageLink+str(currentPageNumber)+".html"
        #print currentPageNumber
        #print eachPageLink
        pagesToVisit.append(eachPageLink)
        currentPageNumber = currentPageNumber+1
    
    
    data = [[0]*6]*(int(lastPageNumber)*10)
    data[0] = ["Software","Company","Description","CategoryHier1","CategoryHier2","CategoryHier3","Downloads","Rank"]
    
    pageCounter=2573
    pointer = 0
    
    #print data
    globalCounter = 0
    fileToWrite = "C:\Users\mohan\Desktop\ScrapedOutput\Drivers_FifthPart.csv"
    file_out = open(fileToWrite, 'wb')
    mywriter = csv.writer(file_out)
    mywriter.writerow(data[0])
    #THIRD LEVEL
    # Iterating over all the pages for a particular subcategory
    while pageCounter<len(pagesToVisit):
        print pagesToVisit[pageCounter]
        htmlfile = urllib.urlopen(pagesToVisit[pageCounter])
        htmltext = htmlfile.read()
        regex = '<a class="OneLinkNoTx" href="(.+?)">(.+?)</a>'
        pattern = re.compile(regex)
        linkAndName = re.findall(pattern,htmltext)
        toolsInPage = 0
        #print len(linkAndName)
        while toolsInPage<len(linkAndName):
            fullDescription = ""
            #print "The link is",(linkAndName[toolsInPage])[0]
            # Getting the name of the Software
            print "The name is",(linkAndName[toolsInPage])[1]
            name = (linkAndName[toolsInPage])[1]
            # Getting information needed for each software by getting into its URL
            # Getting company name
            htmlfileForTool = urllib.urlopen((linkAndName[toolsInPage])[0])
            htmltextForTool = htmlfileForTool.read() 
            regex = '<span class="OneLinkNoTx">(.+?):</span>'
            pattern = re.compile(regex)
            company = re.findall(pattern,htmltextForTool)
            try:
                companyName = str(company[0])
            except IndexError:
                companyName = 'null'
            
            # Getting number of downloads
            regex = '<div class="product-landing-quick-specs-row-content">(.+?)</div>'
            pattern = re.compile(regex)
            matchingList = re.findall(pattern,htmltextForTool)
            try:
                noOfDownloads = str(matchingList[1])
            except IndexError:
                noOfDownloads = 'null'
            
            rank = 'null'
            rankAttr = 'null'
            rankingList = 'null'
            rankAll = 'null'
            htmlfileForTool.close()
            soup = BeautifulSoup("".join(htmltextForTool))
            rankAttr = soup.findAll("li",{"class":"ranking"})
            try:
                rankingList = str(rankAttr[0])
            except IndexError:
                rankigList = 'null'
            #print rankingList
            regex = '<div class="product-landing-quick-specs-row-content">(.+?)#(.+?)in(.+?)</a>'
            pattern = re.compile(regex)
            rankAll = re.findall(pattern,rankingList)
            try:
                rank = (rankAll[0])[1]
            except IndexError:
                rank = 'null'
            #print "rank=",rank
            #print company[0]
            # Getting the hieracrhy of categories
            #htmlfileForTool.close()
            soup = BeautifulSoup("".join(htmltextForTool))
            category = soup.findAll("ul",{"class":"breadcrumb"})
            try:
                categoryList = str(category[0])
            except IndexError:
                categoryList = 'null'
            regex = '<li><a href="(.+?)">(.+?)</a></li>'
            pattern = re.compile(regex)
            hierarchy = re.findall(pattern,categoryList)
            try:
                hierOne = (hierarchy[1])[1]
            except IndexError:
                hierOne = 'null'
            #print "Hierarchy Level 1 is",hierOne
            try:
                hierTwo = (hierarchy[2])[1]
            except IndexError:
                hierTwo = 'null'
            #print "Hierarchy Level 2 is",hierTwo
            try:
                hierThree = (hierarchy[3])[1]
            except IndexError:
                hierThree = 'null'
            #print "Hierarchy Level 3 is",hierThree
            # Getting the description of the software
            description = soup.find("div",{"id":"publisher-description"})
            try:
                desc = (description).text
                desc = desc.replace('\n','')
            except AttributeError:
                desc = 'null'
            #print (description).text
            #desc.replace('\t','')
            #print desc
            data[globalCounter+1] = [(linkAndName[toolsInPage])[1],companyName,desc,hierOne,hierTwo,hierThree,noOfDownloads,rank]
            try:
                mywriter.writerow(data[globalCounter+1])
            except UnicodeEncodeError:
                print "Error in encoding"
            print ""
            #print category
            toolsInPage = toolsInPage + 1
            globalCounter = globalCounter+1
        pageCounter=pageCounter+1
        print pageCounter," out of",len(pagesToVisit)," completed"
        sleep(randint(10,60))
    iteratorForSoftware = iteratorForSoftware +1
file_out.close()
        