import requests
import re
import psycopg2
import thread
import sys

def getChunks():
    query = 'Select * from amazon_review'
    cur.execute(query);
    results = cur.fetchall()
    chunks=[results[x:x+1003] for x in xrange(0, len(results), 1003)]
    return chunks;  

def HitInThread(threadName,chunk):
    for record in chunk:
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
            polarity = ''

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
            matchForAspects = ''

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
            matchForConcepts = ''

        updateQuery = 'update amazon_review SET polarity=\''+polarity+'\', aspects=\''+str(matchForAspects)+'\', concepts = \''+str(matchForConcepts)+'\' where review_id='+str(record[0])
        cur.execute(updateQuery);


con = psycopg2.connect("dbname='SenticNet' user='postgres' host='ec2-52-89-108-22.us-west-2.compute.amazonaws.com' password='swm123'")
con.autocommit = True
cur = con.cursor()
chunks = getChunks()
try:
    thread.start_new_thread( HitInThread, ("Thread-1", chunks[0], ) )
    thread.start_new_thread( HitInThread, ("Thread-2", chunks[1], ) )
    thread.start_new_thread( HitInThread, ("Thread-3", chunks[2], ) )
    thread.start_new_thread( HitInThread, ("Thread-4", chunks[3], ) )
except:
    print "Error: unable to start thread"
    print sys.exc_info()

while(1):
    pass


'''for record in results:
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
    polarity = ''

# For getting the aspects of the review
r = requests.post("http://sentiment.gelbukh.com/sentiment/aspects.php", data={'input': input})
mystring = r.text
try:
    matchForAspects = mystring.replace("<span>", "")
    matchForAspects = matchForAspects.replace("</span>", "")
    matchForAspects = matchForAspects.replace("<br>", ",")
    print matchForAspects
except:
    print 'Match not found'
    matchForAspects = ''

# For getting the concepts of the review
r = requests.post("http://sentiment.gelbukh.com/sentiment/concepts.php", data={'input': input})
mystring = r.text
try:
    matchForConcepts = mystring.replace("<span>", "")
    matchForConcepts = matchForConcepts.replace("</span>", "")
    matchForConcepts = matchForConcepts.replace("<br>", ",")
    print matchForConcepts
except:
    print 'Match not found'
    matchForConcepts = ''

updateQuery = 'update amazon_review_mohan_senti SET polarity='+polarity+', aspects='+matchForAspects+', concepts = '+matchForConcepts+' where review_id='+str(record[0]);
cur.execute(updateQuery);'''
