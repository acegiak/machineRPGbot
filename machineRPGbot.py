#!/bin/python
import twitter,pickle,random,time


hashtag = "#machineGameTest"
obituaries = ["You have died. Please do not post any more messages in "+hashtag,
    "You have been decommissioned. Please do not post any more messages in "+hashtag,
    "The world has ended. Please do not post any more messages in "+hashtag]


try:
    seenTweets = pickle.load(open("seenTweets.pickle", "rb"))
except (OSError, IOError) as e:
    seenTweets = []
    pickle.dump(seenTweets, open("seenTweets.pickle", "wb"))

try:
    lifetimes = pickle.load(open("lifetimes.pickle", "rb"))
except (OSError, IOError) as e:
    lifetimes = {}
    pickle.dump(lifetimes, open("lifetimes.pickle", "wb"))

try:
    mortalities = pickle.load(open("mortalities.pickle", "rb"))
except (OSError, IOError) as e:
    mortalities = []
    pickle.dump(mortalities, open("mortalities.pickle", "wb"))


api = twitter.Api(consumer_key='consumer_key',
                      consumer_secret='consumer_secret',
                      access_token_key='access_token',
                      access_token_secret='access_token_secret')

print(api.VerifyCredentials())

while True:
    results = api.GetSearch(hashtag)
    for result in results:
        if legalStatus(result):
            api.PostRetweet(result.original_id)
            if isThisTheEnd(result.user):
                obituary = random.choice(obituaries)
                api.PostDirectMessage(obituary,result.user.id)
    pickle.dump(seenTweets, open("seentweets.pickle", "wb"))
    pickle.dump(lifetimes, open("lifetimes.pickle", "wb"))
    pickle.dump(mortalities, open("mortalities.pickle", "wb"))
    time.sleep(300)
        
def legalStatus(result):
    if result.id not in seenTweets and result.user.id not in mortalities:
        seenTweets.append(result.id)
        return True
    return False

def isThisTheEnd(user){
    if(user.id not in lifetimes){
        lifetimes[user.id] = 0
    }
    lifetimes[user.id] += 1
    if(lifetimes[user.id] > 3 and random.choice() < 0.15){
        mortalities.append(user.id)
        return True
    }
    return False
}
