from typing import Type
from datetime import datetime
import praw
import time
import json
import requests

url = "https://www.reddit.com/r/botEverywhere/new.json?sort=new"
quote = "https://api.quotable.io/random"
post = []
commented_post = []

def fetch_recent(): 
    req = requests.get(url, headers={'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'})
    json_data = req.text
    parsed_json = (json.loads(json_data))
    distro = parsed_json['data']['children']
    for eachSubmission in distro:
        data = eachSubmission['data']['name']
        title = eachSubmission['data']['title']
        if data not in post:
            if title in ['quote','motivate','Motivate','Quote']:
                post.append(data)
    return

def submission_comment(post_id):
    reddit = praw.Reddit(
    client_id="Your client ID",
    client_secret="Your Seceret ID",
    password="Your Account Password",
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    username="Your Username",
)
    reddit.validate_on_submit = True
    commented_post.append(post_id)
    Submission = reddit.submission(id=post_id)
    # print(type(Submission.author.name))
    comment = quote_fetch()
    print("Commented on : "+ Submission.author.name+" Post")
    Submission.reply(comment)

def split_post():
    for single_post in post:
        single_post = single_post.split("_")
        post_id = single_post[1]
        if post_id not in commented_post:
            submission_comment(post_id)

def quote_fetch():
    req = requests.get(quote, headers={'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'})
    json_data = req.text
    parsed_json = (json.loads(json_data))
    quoted = parsed_json['content'] +" - "+parsed_json['author']
    return quoted

while True:    
    fetch_recent()
    split_post()
    time.sleep(6)