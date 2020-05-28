import requests
import json
from bs4 import BeautifulSoup
import urllib
import re
import xlwt


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
    jsonify = json.loads(soup.find_all("div", "ad native-ad")[0]["data-targeting"])
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


def write_comments_for_links(links):
    book = xlwt.Workbook()
    sheet = book.add_sheet("Refinery29 Comments")
    for i in range(0, len(links)):
        link = links[i]
        sheet.write(0, i, link)
        post_id = get_refinery_29_post_id(link)
        comments = get_refinery_29_comments(post_id)
        parsed_comments = parse_refinery29_comments(comments)
        for j in range(0, len(parsed_comments)):
            sheet.write(j+1, i, parsed_comments[j])
        book.save("data/refinery29_comments.xls")



links = get_refinery29_urls()
write_comments_for_links(links)
