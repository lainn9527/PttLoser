import sys
import requests
import urllib
from requests_html import HTML

def parse_entry(entry):
    link = entry.find('div.title > a', first=True)
    if link == None:
        return None
    else:
        link = link.attrs['href']
    push = entry.find('div.nrec', first=True).text
    if push == "":
        push = 0
    return {
        'title': entry.find('div.title', first=True).text,
        'push': push,
        'date': entry.find('div.date', first=True).text,
        'author': entry.find('div.author', first=True).text,
        'link': 'https://www.ptt.cc' + link
    }

def get_page_info(url, pagenum):
    the_url = url
    post_info = []
    for i in range(pagenum):
        resp = requests.get(the_url)
        html_text = HTML(html = resp.text)
        post_entries = html_text.find('div.r-ent')
        for entry in post_entries:
            info = parse_entry(entry)
            if info != None:
                post_info.append(info)
            
        control_bar = html_text.find('.action-bar a.btn.wide')
        prevpage_link = control_bar[1].attrs['href']
        the_url = urllib.parse.urljoin('https://www.ptt.cc/', prevpage_link)
    return post_info

def print_info(info):
    for i in info:
        pattern = '{:<5}{:40}{:<6}{:<20}'
        print(pattern.format(i['push'], i['title'], i['date'], i['author']))


if __name__ == '__main__':
    url = sys.argv[1]
    page_num = int(sys.argv[2])
    info = get_page_info(url, page_num)
    print_info(info)