from bs4 import BeautifulSoup
import urllib 
import urllib.request
from pprint import pprint


for i in range(2,10):
    # This just downloads the html text with full markdown
    html_text = urllib.request.urlopen('https://www.refinery29.com/en-us/money-diary?page='+ str(i)).read()

    # We want a markdown-interpreted (structured) version of the html using BeautifulSoup:
    page = BeautifulSoup(html_text, 'html.parser')


    divs_standard_stories = page.find('body').find_all('div',{'class':'card standard'})

    for stories in divs_standard_stories:
        links = stories.find_all('a')
        for link in links:
            
            print('https://www.refinery29.com',link['href'])
            domain_link =  'https://www.refinery29.com' + str(link['href'])

            with open('data/money_diaries.csv','a') as file_handler:
                file_handler.write(domain_link + '\n')
