#!/bin/python
import twitter,pickle,random,time,json,sys,signal,webapp2

class machineRPGbot:

    def __init__(self):
        self.seenTweets = []
        self.lifetimes = {}
        self.mortalities = []
        self.hashtag = "#machineGameTest"
        self.obituaries = ["You have died. Please do not post any more messages in "+self.hashtag,
        "You have been decommissioned. Please do not post any more messages in "+self.hashtag,
        "The world has ended. Please do not post any more messages in "+self.hashtag]
        self.myTwitterId = 0

    def main(self):
        try:
            self.seenTweets = pickle.load(open("pickles/seentweets.pickle", "rb"))
        except (OSError, IOError) as e:
            self.seenTweets = []
            pickle.dump(self.seenTweets, open("pickles/seentweets.pickle", "wb"))

        try:
            self.lifetimes = pickle.load(open("pickles/lifetimes.pickle", "rb"))
        except (OSError, IOError) as e:
            self.lifetimes = {}
            pickle.dump(self.lifetimes, open("pickles/lifetimes.pickle", "wb"))

        try:
            self.mortalities = pickle.load(open("pickles/mortalities.pickle", "rb"))
        except (OSError, IOError) as e:
            self.mortalities = []
            pickle.dump(self.mortalities, open("pickles/mortalities.pickle", "wb"))


        json_data=open("credentials.json").read()

        creds = json.loads(json_data)
        self.obituaries = creds['obituaries']
        self.hashtag = creds['hashtag']

        api = twitter.Api(consumer_key=creds['consumer_key'],
                            consumer_secret=creds['consumer_secret'],
                            access_token_key=creds['access_token'],
                            access_token_secret=creds['access_token_secret'])

        verified = api.VerifyCredentials()
        print(verified)
        self.myId = verified.id

        while True:
            print("Checking hashtag!")
            results = api.GetSearch(self.hashtag)
            for result in results:
                print("\n\nExamining tweet:"+str(result.id)+"\nfrom "+result.user.screen_name+"\ncontents:"+result.text)
                if self.legalStatus(result):
                    try:
                        api.PostRetweet(result.id)
                    except twitter.TwitterError as e:
                        print("\n TWITTER ERROR:\n")
                        print(e)
                    if self.isThisTheEnd(result.user):
                        obituary = random.choice(self.obituaries)
                        api.PostDirectMessage(obituary,result.user.id)
            pickle.dump(self.seenTweets, open("pickles/seentweets.pickle", "wb"))
            pickle.dump(self.lifetimes, open("pickles/lifetimes.pickle", "wb"))
            pickle.dump(self.mortalities, open("pickles/mortalities.pickle", "wb"))
            time.sleep(300)



    def legalStatus(self,result):
        print ("usersid:"+str(result.user.id)+" myid:"+str(self.myId))
        if result.id not in self.seenTweets and result.user.id not in self.mortalities and result.user.id != self.myId:
            self.seenTweets.append(result.id)
            print("\ntweet is fresh and new and good")
            return True
        print("\ntweet is not legal for processing. It's old or from the dead")
        return False

    def isThisTheEnd(self,user):
        if user.id not in self.lifetimes:
            self.lifetimes[user.id] = 0
        self.lifetimes[user.id] += 1
        if self.lifetimes[user.id] > 3 and random.random() < 0.15:
            self.mortalities.append(user.id)
            print("\ntweet has caused the death of it's creator")
            return True
        print("\ntweet has escaped the clutches of death")
        return False

class MainPage(webapp2.RequestHandler):
    def get(self):
        machineRPGbot().main()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
