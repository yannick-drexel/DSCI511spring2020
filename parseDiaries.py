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
    # iterator for daily expense data
    i = 1
    for divs in divs_standard_stories:
        
        divs_section_text = divs.find_all('div', {'class' : 'section-text'})
        for div in divs_section_text:
            
            for data in div.find_all(re.compile('^strong|[a-zA-Z0-9\$]$')):
                
                if data.name == 'strong':
                    #clean up the result to get only what we can use as data
                    if (re.search('[a-zA-Z0-9!]', data.name) and data.nextSibling  is not None ) and (re.search('[a-zA-Z0-9!]', data.name) and data.nextSibling.string is not None):
                        data_dict[data.text] = data.next_sibling
                    try:    
                        if (re.search('[Daily Total:] \$[a-zA-Z0-9!]+', data.next)):
                            search_obj = re.findall("\$[0-9]+,[0-9]+|\$[0-9]+|$[0-9]+,[0-9]+.[0-9]", data.next)
                            #search_obj = re.match("^\$[0-9]+", data.next)
                            data_dict['Day ' + str(i)] = search_obj[0]
                            i += 1
                    except TypeError as excpt:
                        print(excpt)
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




def write_refinery29_post_data(urls):
    single_page_dict = {}
    for url in urls:
        single_page_dict[url] = parseMoneyDiari(url)
        #print('urls parsed:', i)
        #single_page_json = json.dump(single_page_dict)

        # append the json file with each page
    with open('data/money_diaries.json', 'a') as file_handler:
        json.dump(dict(single_page_dict), file_handler)


