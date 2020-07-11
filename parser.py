import requests
import urllib
import json
from lxml import etree
from requests_html import HTML
from multiprocessing import Pool

def get_page_info(url, pagenum):
    def parse_page(page_text):
        post_info = []
        post_entries = page_text.find('div.r-ent')
        for entry in post_entries:
            info = parse_entry(entry)
            if info != None:
                post_info.append(info)
        return post_info

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
    
    the_url = url
    post_info = []
    for i in range(pagenum):
        resp = requests.get(the_url)
        html_text = HTML(html = resp.text)
        post_info += parse_page(html_text)

        control_bar = html_text.find('.action-bar a.btn.wide')
        prevpage_link = control_bar[1].attrs['href']
        the_url = urllib.parse.urljoin('https://www.ptt.cc/', prevpage_link)
    return post_info


def parse_thread(thread_url):
    resp = requests.get(thread_url)
    et_html = etree.HTML(resp.text)
    return et_html.xpath('//*[@id="main-content"]/text()') # neglect outside url, i.e. photo, yt link

def get_thread_info(url, pagenum):    
    def get_thread_urls(info):
        return [entry['link'] for entry in info]
                
    infos = get_page_info(url, pagenum);
    thread_urls = get_thread_urls(infos)
    with Pool(processes = 4) as pool:
        text_contents = pool.map(parse_thread, thread_urls)
    for i in range(len(infos)):
        infos[i]['text_content'] = text_contents[i]
    
    return infos

def print_info(info):
    for entry in info:
        pattern = '{:<5}{:40}{:<6}{:<20}'
        print(pattern.format(entry['push'], entry['title'], entry['date'], entry['author']))
        for i in entry['text_content']:
            print(i)
        print("\n\n")

def save_json(full_info):
    with open('ptt.json', 'w', encoding='utf-8') as fp:
        json.dump(full_info, fp, ensure_ascii=False)
