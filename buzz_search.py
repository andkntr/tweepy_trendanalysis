#https://qiita.com/haniokasai/items/9eba9e232a144a0f8805
import tweepy as tw
import json
from requests_oauthlib import OAuth1Session
import sqlite3
import pandas as pd

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOjUdQEAAAAAvjYt054151zXwQ4v4bvqXBPmiBA%3Dfhl0d0umE3LIJ9w22VB0YL4Hr00WMCimVwKYMJOkUKED3qiOH5"
API_KEY="dWxx3W860jXQRgJvd5iML8out"
API_SECRET = "InOTLkorYBabgpu5JTh7eJKqi0jvDwZmGmDoygCRQthcdrLqmX"
ACCESS_TOKEN = "1120544329217519616-IJpP7dnzyxns8PDgfdtGgqp1Go4Z4U"
ACCESS_TOKEN_SECRET = "cNwPbdC09j5AvbIUMe0hmoszJ4VQAMX7FgQpTynKHupFY"

#db_name = 'tehran.db'
#conn = sqlite3.connect(db_name)
#cur = conn.cursor()
#cur.execute('CREATE TABLE tehran_trend(date text,id text,tweet text )')
twitter = OAuth1Session(API_KEY,API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)



def trend_search(from_date,to_date, res=None):
    # Twitter Endpoint(検索結果を取得する)
    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/Dev.json'
    keyword = "mttag.com"
    params ={
             'query' : keyword ,  # 検索キーワード
             'maxResults':100,   # 取得するtweet数
             'fromDate' : from_date ,
             'toDate' : to_date,

            }
    if res is not None:
        params['next'] = res['next']
    result = twitter.get(url, params = params)
    req = twitter.get(url, params = params)
    twurl = []
    follow_count = []
    follower_count =[]
    url = []
    userid = []
    text = []
    rt_count = []
    quote = []
    like = []
    comment = []
    tweeted_time = []
    if req.status_code == 200:
        res = json.loads(req.text)
        for line in res['results']:
            if not "RT @" in line:
                if line['favorite_count'] >5000:
                    userid.append(line['user']['screen_name'])
                    twurl.append("https://twitter.com/"+line['user']['screen_name']+"/status/"+line['id_str'])
                    follow_count.append(line['user']['friends_count'])
                    follower_count.append(line['user']['followers_count'])
                    text.append(line['text'])
                    rt_count.append(line['retweet_count'])
                    quote.append(line['quote_count'])
                    like.append(line['favorite_count'])
                    comment.append(line['reply_count'])
                    tweeted_time.append(line['created_at'])
                    time.sleep
                else:
                    pass

    else:
        print("Failed: %d" % req.status_code)
    if 'next' in res:
        trend_search(from_date, to_date,res)

    df = pd.DataFrame({'user_id':userid,
                        'URL':twurl,
                        'フォロー数':follow_count,
                        'フォロワー数':follower_count,
                        '本文':text,
                        'RT数':rt_count,
                        '引用RT数':quote,
                        'いいね数':like,
                        'コメント数':comment,
                        'ツイート時間':tweeted_time})
    return df.to_excel('~/Downloads/buzz_tweet'+keyword+'.xlsx')


if __name__ == '__main__':
    twitter = OAuth1Session(API_KEY,API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    trend_search("202207010000", "202207150000")





"""
#データベース接続
db_name = "sqlite-tehran.db"
connection = sqlite3.connect(db_name)
"""
# Enedpointへ渡すパラメーター
