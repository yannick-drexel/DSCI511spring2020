# DSCI511Spring2020

This code gets the data about Refinery29 money diaries, a list of comments on Refinery29 for each 
money diary and a list of comments from the Reddit r/moneydiariesactive subbreddit post about that money diary.

Run_refinery29_data_scraper.py saves the following four files in the data directory:
1. money_diary_urls.csv: This csv file contains a list of the scraped money diary urls.
2. money_diaries.json: This json file contains data about each money diary post. Each key is a money diary url. Each value contains data about that post.
3. refinery29_comments_output: This json file contains the refinery29 comments for each money diary post. Each key is a money diary url. Each value contains a list of comment data.
r. reddit_comments_output: This json file contains the reddit comments for each money diary post. Each key is a money diary url. Each value contains a list of comment data.

To run the code, you can use the following command:
python run_refinery29_data_scraper.py
This will return 30 posts worth of data.

To run for less than 30 days of data, you can use the following command:
python run_refinery29_data_scraper.py -n <desired number of posts - must be less than 30>

Link to more information about this project:
https://colab.research.google.com/drive/1V0FRCqgCRdlFQMY6CJhBeyn3fg5HI6yd?usp=sharing
