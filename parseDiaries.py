from bs4 import BeautifulSoup
import urllib 
import urllib.request
from pprint import pprint
import csv
import re
from collections import defaultdict
import inspect
import json
import os


# script read the file that contain the url for each money diaries web page
# then parse each page and put the data in a json file


def parseMoneyDiari(url_diary):
    
    data_dict = defaultdict()
    # get the bs4 for the page
    html_text = urllib.request.urlopen(url_diary).read()

    # We want a markdown-interpreted (structured) version of the html using BeautifulSoup:
    page = BeautifulSoup(html_text, 'html.parser')


    divs_standard_stories = page.find('body').find_all('div',{'class':'section-container section-text-container'})

    for divs in divs_standard_stories:
        
        divs_section_text = divs.find_all('div', {'class' : 'section-text'})
        

        for div in divs_section_text:
            for data in div.find_all(re.compile('^strong|[a-zA-Z0-9\$]$')):
                if data.name == 'strong':
                    #clean up the result to get only what we can use as data
                    if (re.search('[a-zA-Z0-9!]', data.name) and data.nextSibling  is not None ) and (re.search('[a-zA-Z0-9!]', data.name) and data.nextSibling.string is not None):
                        data_dict[data.text] = data.next_sibling
    
    # now let's do some clean up
    data_dict_temp = defaultdict()
    
    for component, value in data_dict.items():
        str_component = component
        str_value = value
        try:
            #let's keep the initial data
            data_dict_temp[str_component.strip()] = str_value.strip()

            #parse the $$$ for futher analisys
            dollar_amounts = re.findall(r"\$[0-9]+,[0-9]+|\$[0-9]+|$[0-9]+,[0-9]+.[0-9]",str_value.strip())
            if len(dollar_amounts) > 0:
                value = {}
                data_dict_temp[str_component.strip() + 'parse $$$'] = dollar_amounts

        except TypeError as excpt:
            print(excpt)
            print('could not insert the value in dict for url {}, key {}, value {}'.format(url_diary, component, value))

    return dict(data_dict_temp)


        

# url_diary = 'https://www.refinery29.com/en-us/prairies-canada-911-dispatcher-salary-money-diary'
# url_diary = 'https://www.refinery29.com/en-us/independent-pr-consultant-toronto-salary-money-diary'
#url_diary = 'https://www.refinery29.com/en-us/analyst-denver-co-salary-money-diary'
#parseMoneyDiari(url_diary)
#pprint(parseMoneyDiari(url_diary))


unique_page_list = set()
single_page_dict = {}

with open('data/money_diaries.csv', 'r') as file_handler:
    urls = csv.reader(file_handler)
    
    for i, url in enumerate(urls):
        #build a unique list of urls
        unique_page_list.add(url[0])
        
# parse all the urls
print(('urls to be parsed:', len(unique_page_list)))
for i, url in enumerate(unique_page_list):
    single_page_dict[url] = parseMoneyDiari(url)
    print('urls parsed:', i)
    #single_page_json = json.dump(single_page_dict)
    with open('data/money_diaries.json', 'a') as file_handler:
        json.dump(dict(single_page_dict), file_handler)
    single_page_dict = {}
# import os
# os.remove("data/money_diaries.json") 

# with open('data/money_diaries.json', 'a') as file_handler:
#     json.dump(single_page_dict, file_handler)