import tweepy
import csv
from tweepy import OAuthHandler
consumer_key = "CtUdKqeUKFFNrz6tZtYe1bVMh"
consumer_secret = "Rl36xMgQdWfZ0mjVBvYLBDq2H3cNh7mjSHhk3HLwlNNnfYXAJ3"
access_token = "702648186263851008-eMtwCp8WDmArJy4chzVMnZObvaoKUDt"
access_secret = "Gw0sefQqew8MTEyx6shXBGJhjiazhC2M5MazwS7yEU2LV"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

user = api.get_user('realDonaldTrump')
screen_name = 'realDonaldTrump'

for tweet in tweepy.Cursor(api.user_timeline(screen_name = screen_name)).items():
	print(tweet)


def oldway(api, screen_name):
	alltweets = []
	new_tweets = api.user_timeline(screen_name = screen_name, count = 200)

	alltweets.extend(new_tweets)

	oldest = alltweets[-1].id - 1
		#keep grabbing tweets until there are no tweets left to grab
	while (len(new_tweets) > 0):
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))

	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	for item in outtweets[-10:]:
		print(item)
		
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(outtweets)
