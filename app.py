from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
import tweepy
from textblob import TextBlob

consumer_key = 'ZT3teoSauRNfVkIvaBWg1CGBH'
consumer_secret = 'qWwBp5BFAGubIeHKKSqKGCgFGXMG5AE2rAzm4LWIjJZ8uUmOy0'

access_token = '128648452-aCcCcHoM8EhGud0F6DgQ98tOS5mcAhMMEEXaEauz'
access_token_secret = 'EuNSIt3SEQw1IDPEEPiTii5s2OHzticaWzUIG8EIWMSnj'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
bad_tweets = []

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/search',methods=['GET','POST'])
def index():
    if request.method == 'POST':
	    username = request.form['username']
	    number_of_tweets = request.form['number_of_tweets']
	    if username[0] is '@':
	        username = username[1:]
	    stuff = api.user_timeline(screen_name=username, count=number_of_tweets, include_rts=False)
	    bad_tweets[:] = []
	    for statuses in stuff:
	        analysis = TextBlob(statuses.text)
	        if analysis.sentiment.polarity < -0.15:
	            bad_tweets.append(str(statuses.text) + '  ---- (' + str(statuses.created_at) + ')')
	    return render_template('search.html',bad_tweets=bad_tweets)
    return render_template('search.html')

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
