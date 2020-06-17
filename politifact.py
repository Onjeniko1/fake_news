import sys, os, json, tweepy, mysql.connector, requests, time, re
from bs4 import BeautifulSoup
from ast import literal_eval


f = open("/tmp/politifact-log.txt", "w")


url = "https://www.politifact.com/api/factchecks/?format=json&page=1784"
mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database = "fake_news"
        )
mycursor = mydb.cursor()

#truncate the database
sql = "truncate politifact"

mycursor.execute(sql)

mydb.commit()

html_doc = requests.get(url, cookies="").text


soup = BeautifulSoup(html_doc,"html.parser")
time.sleep(0.01)

items = soup.find("div", {"class": "response-info"})

contents = str(items)

result = json.loads(html_doc)


news = result["results"]

for single_news in news: 
	
	#insert into the database
        sql = ("INSERT INTO politifact(id, statement, ruling_slug, sources, website) VALUES(%s, %s, %s, %s, 'politifact')")
	
        val = (single_news["id"], single_news["statement"], single_news["ruling_slug"], single_news["sources"])
        mycursor.execute(sql, val)

        mydb.commit()
        
#make API call to buzzfeed
buzzfeed_api = "https://www.buzzfeed.com/api/v2/feeds/index"
buzzfeed_doc = requests.get(buzzfeed_api, cookies="").text

buzzfeed_news = json.loads(buzzfeed_doc)

all_buzzfeed_news = buzzfeed_news["big_stories"]
for single_feed in all_buzzfeed_news:

        #insert into the database
        sql = ("INSERT INTO politifact(id, statement, ruling_slug, sources, website) VALUES(%s, %s, %s, 'none', 'buzzfeed')")
	
        val = (single_feed["id"], single_feed["title"], single_feed["is_quiz"])
        mycursor.execute(sql, val)

        mydb.commit()	

#make api call to twitter and save it in a text file
f = open("/tmp/tweet", "w") 

#loop through news in the politifact table 
mycursor.execute("SELECT statement FROM politifact;")

myresult = mycursor.fetchall()

for result in myresult:
        #load the tweet
        fact = result[0]
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler("lJRN0ZEa2Ec4Ked4ulM5otRO9", "O6qtxw1vuwCv4iJlTD2Xsqv50kuJRJ6re2CPUYQOtK2fHMkCM2")
        auth.set_access_token("1566670046-AMW4BzrRQKj9zvW7qh9s3x9TYnuG0jUXAnd4prv", "Rc9efXD1kRtIEj5RgdFamfmwW3WXdVB7cd811ahv0pdfa")
        api = tweepy.API(auth)
        mydetails = api.me()
        user_details = json.dumps(mydetails._json, indent=2)
        print("Authorized user Details: \n")
        print(user_details)
        print (fact) 
        fact = "Here's What Parental Leave Is Really Like Around The World "   
        tweet = api.search(fact, count= 300)
        print (tweet)
        tweet = str(tweet)
        
        #tweet= json.dumps(tweet, indent=2)
        print (tweet)
        tweet = tweet.replace("[Status(_api=<tweepy.api.API object at 0x7f33d7f87780>, _json=", "") 

        tweet = tweet.replace("\"", "&quot;")
        tweet = tweet.replace("\'", "\"")
        tweet = tweet.replace("None", "\"None\"")
        tweet = tweet.replace("True", "\"True\"")
        tweet = tweet.replace("False", "\"False\"")
        #write the tweet into a file
        f.write(tweet)
        #tweet = json.loads(tweet)
        print (tweet)

        print (type(tweet))
        time.sleep(960)



#insert the tweet into mysl database




	

