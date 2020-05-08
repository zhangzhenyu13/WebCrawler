import os
from agentcrawler import data_path
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag
import logging
content_folder=os.path.join(data_path, "content_list")

def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url
class URLSeeker(HTMLParser):
        def __init__(self, root_url, start_with):
            HTMLParser.__init__(self)
            self.urls = []
            self.root_url=root_url
            self.start_with=start_with

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get("href")
            if href and tag == "a":
                href=urljoin(self.root_url, remove_fragment(href) )
                    
                if href.startswith(self.start_with):
                    self.urls.append(href)
                else:
                    logging.debug("{} not match prefix {}".format(href,self.start_with))

def load_list_urls(data_category, start_with, root_url):
    file=os.path.join(content_folder, data_category+".html")
    url_seeker=URLSeeker(root_url, start_with)
    with open(file, "r", encoding="utf-8") as f:
        html_str=f.read()
        url_seeker.feed(html_str)
    
    return url_seeker.urls

def load_meta_category(category_data:dict):
    category_metadata={}
    for category, urls in category_data.items():
        category_metadata.update(
            {url:category for url in urls}
        )
    return category_metadata
