from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from PhotoGallery.models import Tweet

import oauth2
import json
from datetime import datetime

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_SECRET = settings.ACCESS_SECRET
# Create your views here.

def home(request):

    # If the form was submitted
    if request.method == "POST":
        # First check if the user exists
        handle = request.POST['handle']
        num_tweets = request.POST['quantity']

        url = 'https://api.twitter.com/1.1/users/lookup.json?screen_name='+handle

        user_exist_response = oauth_req(url, CONSUMER_KEY, CONSUMER_SECRET)
        data = json.loads(user_exist_response)
       
        if not isinstance(data, list):
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?tweet_mode=extended'+'&screen_name='+handle+'&count='+num_tweets
            timeline_response = oauth_req(url, CONSUMER_KEY, CONSUMER_SECRET)
            data = json.loads(timeline_response)


            tweet_list = []

            for tweet in data:
                # if there is media then we want to add this to our database
                # we will add every tweet with a picture to our database
                if tweet['entities']['media']:
                    media_url = tweet['entities']['media'][0]['media_url']
                    ts = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')


                    tweet_list.append(Tweet(twitter_handle=handle, 
                        picture_url=media_url, 
                        posting_date=ts))

            Tweet.objects.bulk_create(tweet_list)

            return HttpResponse("Tweets Have Been Added")
    

    context = {} 
    return render(request, 'PhotoGallery/home.html', context)

    
def oauth_req(url, key, secret):
        consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth2.Token(key=ACCESS_TOKEN, secret=ACCESS_SECRET)
        client = oauth2.Client(consumer, access_token)
        resp, content = client.request(url)
        return content

def gallery(request):
    return HttpResponse("Hello this will eventually display a gallery of pictures!")

