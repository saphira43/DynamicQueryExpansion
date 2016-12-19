import sys
import tweepy
import pytz
import io
import json

consumer_key="QqgF5CYeBK8ZvVnFlPrhNNdis"
consumer_secret="dAQYJPfv0ctgnP3uVgm4Xa85u7mCHXn201Orxp1KPdodg6G9AD"
access_key="3578768241-0glX8cga4a6W4L8FzJSSCXLz3lC5enPVCAbqdFr"
access_secret="fzpHRgIeQDyepAAsZZJgueM1CiX4DpTl0wRSijGdjlybh"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
file_name='raw_tweets2.json'
saveFile = io.open(file_name, 'a', encoding='utf-8')

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        #if 'manchester united' in status.text.lower():
        basic_tweet = {'id': status.id_str, 'text': status.text}
        fmt = '%Y-%m-%dT%H:%M:%SZ'
        temp=status.created_at.replace(tzinfo=pytz.UTC)
        basic_tweet['created_at'] = temp.strftime(fmt)
        basic_tweet['name']=status.user.name
        basic_tweet['retweet_count']=status.retweet_count
        basic_tweet['favorite_count']=status.favorite_count
        basic_tweet['location']=status.place.country_code
        basic_tweet['hashtags']=status.entities["hashtags"]
        basic_tweet['urls']=status.entities["urls"]
        basic_tweet['mentions']=status.entities["user_mentions"]
        basic_tweet['reply']=status.in_reply_to_status_id
        my_data=json.dump(unicode(basic_tweet),saveFile, ensure_ascii=False)
        saveFile.write(u',')
        #print basic_tweet
        #print ","

    def on_error(self, status_code):
        print 'Encountered error with status code:%s'%status_code
        saveFile.close()
        return True # Don't kill the stream

    def on_timeout(self):
        print  'Timeout'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(locations=[-81.735749,-4.225667,-66.851923 , 13.394483])