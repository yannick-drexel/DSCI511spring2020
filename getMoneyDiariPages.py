from bs4 import BeautifulSoup
import urllib 
import urllib.request

def get_refinery29_links(max_number):

    links = []

    for i in range(2, 10):

        links = list(set(links))
        if len(links) > max_number:
            max_links = links[0: max_number]
            write_csv_file(max_links)
            return max_links

        # This just downloads the html text with full markdown
        html_text = urllib.request.urlopen('https://www.refinery29.com/en-us/money-diary?page=' + str(i)).read()

        # We want a markdown-interpreted (structured) version of the html using BeautifulSoup:
        page = BeautifulSoup(html_text, 'html.parser')

        divs_standard_stories = page.find('body').find_all('div', {'class': 'card standard'})

        for stories in divs_standard_stories:
            new_links = stories.find_all('a')
            for new_link in new_links:
                #print('https://www.refinery29.com', link['href'])
                domain_link = 'https://www.refinery29.com' + str(new_link['href'])
                links.append(domain_link)


def write_csv_file(links):
    with open('data/money_diary_urls.csv', 'w') as file_handler:
        for link in links:
            file_handler.write(link + '\n')



# TO DO: check if the list of urls is unique after runing the script.
