import argparse

from getMoneyDiariPages import get_refinery29_links
from parseDiaries import write_refinery29_post_data
from refinery_29_comment_scraper import write_refinery29_comments
from subreddit_scraper import get_reddit_comments


def get_urls(args):
    if args.number is not None and 0 < args.number < 31:
        return get_refinery29_links(args.number)
    elif args.number is not None and (args.number < 0 or args.number > 30):
        raise Exception("Issue with -n argument. Number of posts must be above 0 and less than or equal to 30")
    else:
        return get_refinery29_links(30)

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--number", type=int,
                    help="number of posts")

args = parser.parse_args()

print("Retrieving Refinery29 Urls and writing them to data/money_diaries.csv")
links = get_urls(args)

print("Retrieving Refinery29 Post Data and writing it to data/money_diaries.json")
write_refinery29_post_data(links)

print("Retrieving Refinery29 Comments and writing them to data/refinery29_comments_output.json")
write_refinery29_comments(links)

print("Retrieving Reddit Comments and writing them data/reddit_comments_output.json")
get_reddit_comments(links)



