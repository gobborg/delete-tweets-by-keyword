import tweepy, json

# Authenticate to Twitter
auth = tweepy.OAuthHandler("REDACTED", "REDACTED")
auth.set_access_token("REDACTED", "REDACTED")

api = tweepy.API(auth)
'''
# To test access to Twitter
try:
	api.verify_credentials()
	print("Authentication OK")
except tweepy.TweepError as error:
	print("Error during authentication")
	print(error.reason)
api.update_status("test tweet")
'''

# Counters for fun and data
deleted_tweets = 0
failed_deletion = 0
unaffected_tweets = 0

file = open("tweet.js","r")
myjson = json.load(file)
# print(repr(myjson)) # to confirm that json file is read in as a list

text_substr = 'the ' # keyword. need to have a space after it to prevent things like "they" bc it's a string. case-sensitive.

def tweet_matches(tweet, full_text_substr):
	tweet = tweet['tweet'] # parse individual tweet dictionary as a list
	full_text_matches = full_text_substr in tweet ['full_text'] # search full-text key:value for substring
	return full_text_matches

qualifying_tweets = [t for t in myjson if tweet_matches(t, text_substr)]

#print(*qualifying_tweets, sep="\n") # this will print entire dicts for each matching tweet

for tweet in qualifying_tweets:
	full_text = tweet.get("tweet").get("full_text")
	created_at = tweet.get("tweet").get("created_at")
	in_reply_to_screen_name = tweet.get("tweet").get("in_reply_to_screen_name","[none]") #  not all tweets are replies
	#print(f"{full_text}" + ' created at' + f"{created_at}")

	print(full_text + ' created at' + created_at + ' will be deleted')
	try:
		#print(f"{full_text}" + ' created at' + f"{created_at}")
		api.destroy_status(tweet['tweet']['id_str'])
	except (tweepy.error.TweepError):
		print('Error destroying due to ', tweepy.error.TweepError)
		failed_deletion +=1
	try:
		#print(f"{full_text}" + ' created at' + f"{created_at}")
		api.get_status(tweet["tweet"]["id_str"])
	except (tweepy.error.TweepError):
		print(f"{full_text}" + ' created at' + f"{created_at}"+ ' ' + tweet["tweet"]["id_str"] + ' successfully deleted')
		deleted_tweets +=1
	else:
		failed_deletion +=1

unaffected_tweets = len(myjson) - len(qualifying_tweets)

print('Total deleted tweets = ', deleted_tweets)
print('Total failed deletion = ', failed_deletion)
print('Total unaffected tweets = ', unaffected_tweets)
