import praw
import config
import time
import os
import requests
import re

def bot_login():
    print ("Logging in to Reddit...")
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "URL shortener v0.1")
    print ("Logged in!")

    return r

def run_bot(r, comments_replied_to):
    print ("Grabbing 10 Comments...")

    found_url = ""

    for comment in r.subreddit('test').comments(limit = 10):
        if "!shortenurl" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
            print ("String with \"!shortenurl\" found in comment " + comment.id)
                
            comment_reply = "You requested to shorten your URL! Here is the new URL:\n\n"

            found_url = (re.search("(?P<url>https?://[^\s]+)", comment.body).group("url"))

            new_url = requests.get('https://api.shrtco.de/v2/shorten?url=' + found_url).json()['result']['full_short_link']

            comment_reply += ">" + new_url + "\n\n Credit to [Shrtcode](https://shrtco.de/docs/)"

            comment.reply(comment_reply)
            print ("Replied to comment " + comment.id)

            comments_replied_to.append(comment.id)

            with open ("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print ("Sleeping for 10 seconds")
    time.sleep(10)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")

    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print (comments_replied_to)

while True:
    run_bot(r, comments_replied_to)