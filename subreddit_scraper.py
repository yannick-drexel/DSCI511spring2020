import json

import praw
import requests
from praw.models import MoreComments
from collections import defaultdict


def get_reddit_comments(urls):
    reddit = praw.Reddit(client_id='A9UAtvollb2rLg', \
                         client_secret='VXw8b4vjjoA_jybYNpTgNC2mHQE', \
                         user_agent='ScrapeSubReddit', \
                         username='smpascua', \
                         password='Kanchi123')

    # print(Refinery29links)
    subreddit_dict = {}
    for link in urls:
        url = "https://api.pushshift.io/reddit/search/submission/?subreddit=MoneyDiariesActive&q=" + link  # a variable that contains the API url + the Refinery29 link
        # print(url)
        resp = requests.get(url)  # create a get request using url and assign to resp variable
        results = resp.json()  # convert the resp to json
        if len(results["data"]) != 0:  # skip any results["data"] that is empty
            post_id = results["data"][0]["id"]  # get the subreddit id from th url(API + Refinery link) is assigned to post_id
            submission = reddit.submission(id=post_id)  # use the reddit api to get a post using post_id
            comments = []
            for top_level_comment in submission.comments:  # iteration to read all the comments in submission and assign to top_level_comment
                if isinstance(top_level_comment, MoreComments):  # skipped if the comment undet "more comments"
                    continue  # skip the current iteration and does not skip the loop
                comments.append(top_level_comment.body)
            subreddit_dict[link] = {}
            subreddit_dict[link]["comments"] = comments
    json_data = json.dumps(subreddit_dict, ensure_ascii=False, indent=4)
    open("data/reddit_comments_output.json", "w").write(json_data)


