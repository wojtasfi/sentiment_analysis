import itertools
import json
import threading
from datetime import datetime, timedelta

import numpy as np
import tweepy

from sentiments.analysis.encoder import Model
from sentiments.models import AnalysisPending, Analysis, OneDayResult, TwitterAuth


class SentimentAnalysisService:

    def __init__(self):
        self.model = Model()
        self.api = None
        self.performing_analysis = False
        self.start_analysis()

    def start_analysis(self):
        threading.Timer(10, self.start_analysis).start()

        self.api = self.init_twitter_api()

        if self.performing_analysis is False and self.api is not None:
            self.submit_pending_analysis()

    def submit_pending_analysis(self):
        print("Looking for new analysis")
        pending_list = AnalysisPending.objects.all()
        nr_of_pending_analysis = pending_list.count()
        print("Found %s analysis" % nr_of_pending_analysis)

        if nr_of_pending_analysis > 0:
            self.performing_analysis = True
            for pending in pending_list:
                self.analyze(pending.id)
            self.performing_analysis = False

    def __get_tweets__(self, text):
        print("Getting tweets for %s" % text)
        language = 'en'
        tweet_count = 1
        max_days_back = 7
        today = datetime.now().date()
        results = []
        for i in range(max_days_back):
            since = today - timedelta(days=i)
            until = since + timedelta(days=1)
            print("Getting tweets for date " + str(since))

            result = self.api.search(q=text, language=language,
                                     count=tweet_count,
                                     tweet_mode='extended',
                                     since=since,
                                     until=until)

            results.extend(result)

        print("Found %s" % len(results))
        return results

    def __retrieve_full_text_of_tweets__(self, tweets):

        tweets_texts = []
        for tweet in tweets:
            full_text = tweet.full_text
            text1 = " ".join(filter(lambda x: x[0] != '#', full_text.split()))
            text2 = " ".join(filter(lambda x: x[0] != 'https', text1.split()))
            text3 = " ".join(filter(lambda x: x[0] != '@', text2.split()))
            tweets_texts.append(text3)

        return tweets_texts

    def analyze(self, id):
        analysis_pending = AnalysisPending.objects.get(id=id)
        text = analysis_pending.text

        try:
            tweets = self.__get_tweets__(text)
        except Exception as exception:
            print("There is a problem with Twitter authorization data")
            twitter_auth = TwitterAuth.objects.all()[0]
            twitter_auth.error = self.__retrieve_error_message__(exception)
            TwitterAuth.save(twitter_auth)
            return

        analysis = self.__create_general_analysis__(text, tweets)

        self.__perform_day_by_day_analysis__(tweets, analysis)

        analysis_pending.delete()

        print("Done analysis for " + str(text))

    def __retrieve_error_message__(self, exception):
        return json.loads(exception.response.text)['errors'][0]['message']

    def __create_general_analysis__(self, text, tweets):
        print("Starting general analysis for %s" % text)

        tweets_texts = self.__retrieve_full_text_of_tweets__(tweets)
        text_features = self.model.transform(tweets_texts)

        results = text_features[:, 2388]
        mean = np.around(np.mean(results), 2)
        median = np.around(np.median(results), 2)
        std = np.around(np.std(results), 2)
        best = np.around(np.max(results), 2)
        worst = np.around(np.min(results), 2)

        new_analysis = Analysis(text=text,
                                mean=mean,
                                median=median,
                                std=std,
                                best=best,
                                worst=worst)
        Analysis.save(new_analysis)

        return new_analysis

    def init_twitter_api(self):
        auths = TwitterAuth.objects.all()

        if auths.count() == 0:
            return None

        twitter_auth = auths[0]
        auth = tweepy.OAuthHandler(consumer_key=twitter_auth.consumer_key,
                                   consumer_secret=twitter_auth.consumer_secret)
        auth.set_access_token(twitter_auth.access_token,
                              twitter_auth.access_token_secret)

        return tweepy.API(auth)

    def __perform_day_by_day_analysis__(self, tweets, analysis):
        print("Start day by day analysis")
        for date, tweets_group in itertools.groupby(tweets, lambda tweet: tweet.created_at.date()):
            print("Analyzing tweets for date " + str(date))
            tweets_texts = self.__retrieve_full_text_of_tweets__(tweets_group)
            text_features = self.model.transform(tweets_texts)

            results = text_features[:, 2388]
            mean = np.around(np.mean(results), 2)
            median = np.around(np.median(results), 2)
            std = np.around(np.std(results), 2)
            best = np.around(np.max(results), 2)
            worst = np.around(np.min(results), 2)

            one_day_result = OneDayResult(date=date,
                                          mean=mean,
                                          median=median,
                                          std=std,
                                          best=best,
                                          worst=worst,
                                          analysis=analysis)

            OneDayResult.save(one_day_result)
