import requests
import re
import psycopg2


con = psycopg2.connect("dbname='SenticNet' user='postgres' host='ec2-52-89-108-22.us-west-2.compute.amazonaws.com' password='swm123'")
con.autocommit = True
cur = con.cursor()


query = 'Select * from amazon_review_mohan_senti where review_id > 1'
cur.execute(query);
results = cur.fetchall()
for record in results:
    input = record[2]
    print "Sentence:",input

    # For getting the polarity of the review
    r = requests.post("http://sentiment.gelbukh.com/sentiment/run.php", data={'input': input})
    mystring = r.text
    try:
        matchForPolarity = re.search(r"<span>Sentence polarity - (.*)</span>", mystring)
        polarity =  matchForPolarity.group(1)
        print polarity
    except:
        print 'Match not found ',mystring
        polarity = 'NONE'

    # For getting the aspects of the review
    r = requests.post("http://sentiment.gelbukh.com/sentiment/aspects.php", data={'input': input})
    mystring = r.text
    try:
        matchForAspects = mystring.replace("<span>", "")
        matchForAspects = matchForAspects.replace("</span>", "")
        matchForAspects = matchForAspects.replace("<br>", ",").replace("'","")
        print matchForAspects
    except:
        print 'Match not found'
        matchForAspects = 'NONE'

    # For getting the concepts of the review
    r = requests.post("http://sentiment.gelbukh.com/sentiment/concepts.php", data={'input': input})
    mystring = r.text
    try:
        matchForConcepts = mystring.replace("<span>", "")
        matchForConcepts = matchForConcepts.replace("</span>", "")
        matchForConcepts = matchForConcepts.replace("<br>", ",").replace("'","")
        print matchForConcepts
    except:
        print 'Match not found'
        matchForConcepts = 'NONE'

    updateQuery = 'update amazon_review_mohan_senti SET polarity=\''+polarity+'\', aspects=\''+str(matchForAspects)+'\', concepts = \''+str(matchForConcepts)+'\' where review_id='+str(record[0])
    print updateQuery
    cur.execute(updateQuery);
