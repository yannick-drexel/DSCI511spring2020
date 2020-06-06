import argparse
from refinery_29_comment_scraper import get_refinery29_urls, create_json_file

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", type=int,
                    help="number of posts")
parser.add_argument("-d", "--data", type=str,
                    help="data to be returned. options: all, post_data, refinery_comments, reddit_comments")
args = parser.parse_args()

links = get_refinery29_urls()

if args.number is not None and 0 < args.number < 31:
    links = links[0 : args.number]

if args.data is None or args.data == 'all':
    print("Saving Refinery29 Comments to refinery29_comments_output.json")
    create_json_file(links)
