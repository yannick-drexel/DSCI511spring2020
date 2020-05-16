import requests
import json
from bs4 import BeautifulSoup
import urllib

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
    all_comments_text.append(comment['content'][0]['text'].replace("\n", ""))
  return all_comments_text

post_id = get_refinery_29_post_id("https://www.refinery29.com/en-us/design-engineer-san-jose-ca-salary-money-diary")
comments = get_refinery_29_comments(post_id)
parsed_comments = parse_refinery29_comments(comments)

parsed_comments
