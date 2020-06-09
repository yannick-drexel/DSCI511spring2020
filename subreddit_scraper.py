import json
from datetime import datetime
import praw
import requests
from praw.models import MoreComments


def get_reddit_comments(urls):

    #You need to create a Reddit app to run this code. You can create the App here: https://www.reddit.com/prefs/apps.
    # For more information on the client_id, client_secret and user_agent, see here: https://praw.readthedocs.io/en/latest/getting_started/authentication.html#oauth
    reddit = praw.Reddit(client_id='PERSONAL_USE_SCRIPT_14_CHARS',
                         client_secret='SECRET_KEY_27_CHARS ',
                         user_agent='YOUR_APP_NAME',
                         username='YOUR_REDDIT_USER_NAME',
                         password='YOUR_REDDIT_LOGIN_PASSWORD')

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
                comment = {}
                if isinstance(top_level_comment, MoreComments):  # skipped if the comment undet "more comments"
                    continue  # skip the current iteration and does not skip the loop
                comment["comment_text"] = top_level_comment.body
                if top_level_comment.author is not None:
                    comment["user"] = top_level_comment.author.name
                else:
                    comment["user"] = ""
                comment["up_votes"] = top_level_comment.ups
                comment["down_votes"] = top_level_comment.downs
                comment["time_scraped"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                comments.append(comment)
            subreddit_dict[link] = comments
    json_data = json.dumps(subreddit_dict, ensure_ascii=False, indent=4)
    open("data/reddit_comments_output.json", "w").write(json_data)


