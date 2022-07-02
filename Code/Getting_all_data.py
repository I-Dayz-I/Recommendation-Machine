from tangled_up_in_unicode import script
import tweepy
import pandas as pd
import re
import os



def Get_Tweets(all_tweets):
    # API KEY Pv0lCgvrfPndDuImQntGGeXGx
    # API SECRET KEY YSTTtViPNlWWEhI96d21p18WnjGSKS6z3MbUNo1FRDVEAr7nZ9
    
    # bEARER TOKEN AAAAAAAAAAAAAAAAAAAAAE2YeQEAAAAA9d%2Bm%2FKXz7wuNgQyKjKPb35Ue3Z8%3DVZ90TCksYFndImSV9IzH86UiQ5FkWhJ3FeetdEkf09eGR13efV
    
    #aCCESS TOKEN 1543006621625995267-XuAsXH9hgGZZaTqRMiqhUTe2V7axxu
    #aCCESS TOKEN SECRET XNDWQxkzV1tdnRaZYbliKQOO09yrtHPemkmvFJ5TbY2Sb
    
    CONSUMER_KEY = "Pv0lCgvrfPndDuImQntGGeXGx"
    CONSUMER_SECRET = "YSTTtViPNlWWEhI96d21p18WnjGSKS6z3MbUNo1FRDVEAr7nZ9"
    OAUTH_TOKEN = "1543006621625995267-XuAsXH9hgGZZaTqRMiqhUTe2V7axxu"
    OAUTH_TOKEN_SECRET = "XNDWQxkzV1tdnRaZYbliKQOO09yrtHPemkmvFJ5TbY2Sb"
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)

    for id_of_tweet in tweets_id:
        tweet = api.get_status(id_of_tweet)
        print(tweet.text)
    
    
    
def Create_User_GraphCSV():

    filepath = os.path.join(os.path.dirname(__file__), '..','Dataset','active_follower_real.txt')
    

    with open(filepath, mode='r') as f:
        #print("I GOT PATH")
        content = f.read()
        thelist = content.splitlines()
        f.close()
        print(filepath)
        # print(content)
        print()

    CleanContent = re.split('\)|\(|,',content)
    clean = filter(None, CleanContent)

    index = 0
    integer = []
    for i in clean:
        try:
            integer.append(int(i))
        except:
            continue
    data = []
    for i in range(len(integer)):
        if i%2 == 0:
            data.append([integer[i], integer[i+1]])

    dataframe = pd.DataFrame(data, columns=['user_id', 'follower_id'])
    newfile = os.path.join(os.path.dirname(__file__), '..','Dataset','active_follower_real.csv')
    dataframe.to_csv(newfile)
    
    
Create_User_GraphCSV()