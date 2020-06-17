import sys, os, json, tweepy, mysql.connector

def main():
    """ A demo daemon main routine, write a datestamp to 
        /tmp/daemon-log every 10 seconds.
    """
    import time

    f = open("/tmp/daemon-log", "w") 
    while 1: 
        f.write('%s\n' % time.ctime(time.time()))
   
        mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database = "fake_news"
        )

        mycursor = mydb.cursor()

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler("lJRN0ZEa2Ec4Ked4ulM5otRO9", "O6qtxw1vuwCv4iJlTD2Xsqv50kuJRJ6re2CPUYQOtK2fHMkCM2")
        auth.set_access_token("1566670046-AMW4BzrRQKj9zvW7qh9s3x9TYnuG0jUXAnd4prv", "Rc9efXD1kRtIEj5RgdFamfmwW3WXdVB7cd811ahv0pdfa")
        api = tweepy.API(auth)
        # test  authentication
        try:            
            api.verify_credentials()        

            mydetails = api.me()
            f.write("Authentication OK to twitter \n")

            #Load the details of the authenticated user
            user_details = json.dumps(mydetails._json, indent=2)
            f.write("Authorized user Details: \n")
            #################f.write(user_details)
            user_details = json.loads(user_details)
           
            
            #fetch and display statements
            # Make SQL query to fetch politifacts data
            mycursor.execute("SELECT statement FROM politifact;")

            myresult = mycursor.fetchall()
            
            #fetch tweets hardcoded
            fact = "Corona Virus in Kenya"
            
            tweets = api.search(fact, count= 1)
            
            collected_tweets = json.dumps(tweets, indent=2)
            f.write("Collected Tweets: \n")
            f.write(collected_tweets)
            
	    #iterate through the tweets and insert int the database
            news = tweets["_json"]
    
            

            for single_news in user_details: 
                print (single_news)

                #insert into the database
                sql = ("INSERT INTO twitter(created_at, tweet, retweet_count, location, place, mentions, url) VALUES(%s, %s, %s, %s, %s, %s, %s)")

                val = (single_news["created_at"], single_news["text"], single_news["friends_count"], single_news["location"], single_news["location"], single_news["friends_count"], single_news["url"])
                mycursor.execute(sql, val)

                mydb.commit()


            for x in myresult:
                
                #loop through the facts in the database
                fact = x[0]
                
                #fetch tweets
                #tweets = api.search(fact, count=20)
                
                #print (fact)
                #print (tweets)
                
                time.sleep(960) 

                # Loop through Politifcts database
                # For each fake news, make an API call to twitter
                #fact = "Corona Virus in Kenya victims"
                #tweets = api.search(fact, count=300)
                #print(tweets._json) 
                #print(tweets.status._json)
                #f.write("'Corona virus in kenya' tweet \n")
                #tweets_json = json.dumps(tweets, indent = 2)
                #print ('Json type')
                #f.write(tweets_json)

                #loop through each tweet
                #cccheck if the tweet exists in the database
                #insert the tweet into the database if it does nor exist			
                # mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")ss


        except:
            f.write("Error: Failed to fetch data from Twitter API or authentication Error")

        f.flush() 
        time.sleep(960) 


if __name__ == "__main__":
    # do the UNIX double-fork magic, see Stevens' "Advanced 
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try: 
        pid = os.fork() 
        if pid > 0:
            # exit first parent
            sys.exit(0) 
    except OSError as e: 
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    # do second fork
    try: 
        pid = os.fork() 
        if pid > 0:
            # exit from second parent, print eventual PID before
            print ("Daemon PID %d" % pid) 
            sys.exit(0) 
    except OSError as e: 
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1) 

    # start the daemon main loop
    main() 
