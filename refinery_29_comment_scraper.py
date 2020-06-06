from datetime import datetime

import requests
import json
from bs4 import BeautifulSoup
import urllib
import re


def get_refinery29_urls():
    refinery29_links = []
    for i in range(2, 10):
        # This just downloads the html text with full markdown
        html_text = urllib.request.urlopen('https://www.refinery29.com/en-us/money-diary?page=' + str(i)).read()

        # We want a markdown-interpreted (structured) version of the html using BeautifulSoup:
        page = BeautifulSoup(html_text, 'html.parser')

        divs_standard_stories = page.find('body').find_all('div', {'class': 'card standard'})

        for stories in divs_standard_stories:
            links = stories.find_all('a')
            for link in links:
                domain_link = 'https://www.refinery29.com' + str(link['href'])
                refinery29_links.append(domain_link)
        return refinery29_links


def get_refinery_29_post_id(url):
    html_text = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_text, 'html.parser')
    html_with_ids = soup.find_all("div", "ad native-ad")
    if html_with_ids is not None and len(html_with_ids) > 0:
        jsonify = json.loads(html_with_ids[0]["data-targeting"])
        return jsonify["entityid"]


def get_refinery_29_comments(post_id):
    headers = {
        'x-post-id': "entry_" + str(post_id),
        'user-agent': '',
        'content-type': 'application/json; charset=ISO-8859-1',
        'x-spot-id': 'sp_rexLo99v',
    }

    data = '{"sort_by":"best","offset":0,"count":1000,"depth":1}'

    response = requests.post('https://api-2-0.spot.im/v1.0.0/conversation/read', headers=headers, data=data)
    return json.loads(response.content.decode("utf8"))


def parse_refinery29_comments(comments):
    all_comments = comments['conversation']['comments']
    all_comments_text = []
    for comment in all_comments:
        comment_text = comment['content'][0]['text'].replace("\n", " ")
        comment_clean = re.sub("<*>", " ", comment_text)
        all_comments_text.append(comment_clean.replace("\n", " "))
    return all_comments_text


def create_refinery29_comment_dict(comments):
    if comments['conversation'] is not None:
        all_comments = comments['conversation']['comments']
        all_comments_dict = []
        for comment in all_comments:
            comment_dict = {}
            comment_text = comment['content'][0]['text'].replace("\n", " ")
            comment_clean = re.sub("<*>", " ", comment_text)
            comment_dict["comment_text"] = comment_clean
            comment_dict["user"] = comment["user_id"]
            comment_dict["up_votes"] = comment["rank"]["ranks_up"]
            comment_dict["down_votes"] = comment["rank"]["ranks_down"]
            comment_dict["time_scraped"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            all_comments_dict.append(comment_dict)
        return all_comments_dict


def create_json_file(links):
    refinery29_data = {}
    for i in range(0, len(links)):
        link = links[i]
        post_id = get_refinery_29_post_id(link)
        if post_id is not None:
            comments = get_refinery_29_comments(post_id)
            if comments is not None:
                refinery29_data[link] = create_refinery29_comment_dict(comments)
    json_data = json.dumps(refinery29_data, ensure_ascii=False, indent=4)
    open("refinery29_comments_output.json", "w").write(json_data)

