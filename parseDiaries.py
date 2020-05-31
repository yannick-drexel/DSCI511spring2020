from bs4 import BeautifulSoup
import urllib 
import urllib.request
from pprint import pprint
import csv
import re

with open('data/money_diaries.csv', 'r') as file_handler:
    urls = csv.reader(file_handler)

    for url in urls:
        print(url)
data_dict = {}
def parseMoneyDiari(url_diary):

    html_text = urllib.request.urlopen(url_diary).read()

    # We want a markdown-interpreted (structured) version of the html using BeautifulSoup:
    page = BeautifulSoup(html_text, 'html.parser')


    divs_standard_stories = page.find('body').find_all('div',{'class':'section-container section-text-container'})

    for divs in divs_standard_stories:
        #print(divs)
        divs_section_text = divs.find_all('div', {'class' : 'section-text'})
        

        for div in divs_section_text:
            for data in div.find_all(re.compile('^strong|[a-zA-Z0-9\$]$')):
                if data.name == 'strong':
                    #clean up the result to get only what we can use as data
                    if re.search('[a-zA-Z0-9!]', data.name) and (data.nextSibling != None or data.nextSibling != '<br/>'):
                        data_dict[data.text] = data.nextSibling

    pprint(data_dict)            
        

url_diary = 'https://www.refinery29.com/en-us/prairies-canada-911-dispatcher-salary-money-diary'

parseMoneyDiari(url_diary)