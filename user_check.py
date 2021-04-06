#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 19:44:17 2021

@author: pablogtorres
"""

def user_check(user):
        
        import re
        import pickle
        import numpy as np
        import pandas as pd
        from newspaper import Article
        # nltk
        from nltk.stem import WordNetLemmatizer
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics import confusion_matrix, classification_report
        
        import tweepy
         
        API_KEY = "GRIQAjcXXHQTT8TJoLACQCIpM"
        API_SECRET = "iXcOdHc98PAlba4g1Gtaqo1yJyydG5PiV2Mzp2DpQ7fjy7y3Qb"
        #Bearer ACCESS_TOKEN = "AAAAAAAAAAAAAAAAAAAAALQiNQEAAAAAyJ4pI5a6X1vfSXQqAPcBVhA8u%2Fg%3Dbu6ldlBvjjmh3AQpToK6qsRH4nXQxjvzGUEC8DZ0lVdPd6FpDa"
        ACCESS_TOKEN = "1241856200288976901-XhSvVLXUnJ8Xd957mbAiECeOEdgVtB"
        
        ACCESS_TOKEN_SECRET = "pk5Cv1drDfHaPvTg46Ny63OMsVuwywaOdHAsMtKGyyIgM"
         
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        
        def get_timeline(user, count=50):
            results = api.user_timeline(user, count=count)
            twittes = [pd.Series(twits._json) for twits in results]
            df = pd.DataFrame(twittes)
            return df
        user_timeline = get_timeline(user)
        text_check = []
        for i in range(len(user_timeline['text'])):
            try:
                text_check.append(user_timeline['text'][i])
            except: 
                pass
        news_check = []
        for i in range(len(user_timeline['entities'])):
            try:
                news_check.append(user_timeline['entities'][i]['urls'][0]['expanded_url'])
            except: 
                pass
            
         # Defining dictionary containing all emojis with their meanings.
        emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad', 
                  ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
                  ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed', 
                  ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
                  '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
                  '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink', 
                  ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}
        
        ## Defining set containing all stopwords in english.
        stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
                     'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
                     'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
                     'does', 'doing', 'down', 'during', 'each','few', 'for', 'from', 
                     'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
                     'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
                     'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
                     'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
                     'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're',
                     's', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
                     't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
                     'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 
                     'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
                     'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
                     'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
                     "youve", 'your', 'yours', 'yourself', 'yourselves']   
        
        def preprocess(textdata):
            processedText = []
            
            # Create Lemmatizer and Stemmer.
            wordLemm = WordNetLemmatizer()
            
            # Defining regex patterns.
            urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
            userPattern       = '@[^\s]+'
            alphaPattern      = "[^a-zA-Z0-9]"
            sequencePattern   = r"(.)\1\1+"
            seqReplacePattern = r"\1\1"
            
            for tweet in textdata:
                tweet = tweet.lower()
                
                # Replace all URls with 'URL'
                tweet = re.sub(urlPattern,' URL',tweet)
                # Replace all emojis.
                for emoji in emojis.keys():
                    tweet = tweet.replace(emoji, "EMOJI" + emojis[emoji])        
                # Replace @USERNAME to 'USER'.
                tweet = re.sub(userPattern,' USER', tweet)        
                # Replace all non alphabets.
                tweet = re.sub(alphaPattern, " ", tweet)
                # Replace 3 or more consecutive letters by 2 letter.
                tweet = re.sub(sequencePattern, seqReplacePattern, tweet)
        
                tweetwords = ''
                for word in tweet.split():
                    # Checking if the word is a stopword.
                    #if word not in stopwordlist:
                    if len(word)>1:
                        # Lemmatizing the word.
                        word = wordLemm.lemmatize(word)
                        tweetwords += (word+' ')
                    
                processedText.append(tweetwords)
                
            return processedText
        processedtext = preprocess(text_check)
        news_title = []
        for i in news_check:
            print(i)
            article = Article(i)
            article.download()
            article.parse()
            news_title.append(article.title)
        processednews = preprocess(news_title)
        
        # load the model for Hate Speech from server:
        filename = 'hatespeech_model.sav'
        hatespeech_model = pickle.load(open(filename, 'rb'))
        vect2=pickle.load(open('hate_speech_vector.pickle',"rb"))
        processedtext_features = vect2.transform(processedtext)
        hate_pred = pd.DataFrame(hatespeech_model.predict(processedtext_features))
        twit_nun = len(hate_pred)
        hate_pred_per = round(float(100 - (sum(hate_pred[0]==1)/len(hate_pred))*100),2)

        
        # load the model for Fake news from server & calculate %:
        filename = 'fakenews_model.sav'
        fakenews_model = pickle.load(open(filename, 'rb'))
        vect1=pickle.load(open('fake_vector.pickle',"rb"))
        processednews_features = vect1.transform(processednews)
        fake_pred = pd.DataFrame(fakenews_model.predict(processednews_features))
        fake_news_per = round(float(100 - (sum(fake_pred[0]==1)/len(fake_pred))*100),2)

        
        return hate_pred_per, fake_news_per, twit_nun
    
        
        
        
        
        
        
        
        
        
        