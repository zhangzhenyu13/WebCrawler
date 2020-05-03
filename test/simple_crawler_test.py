from agentcrawler.simple_crawler import SimpleCrawler
import functools
import logging
import os
from agentcrawler import data_path
from urllib.parse import urljoin, urldefrag
from html.parser import HTMLParser
import json
logging.getLogger().setLevel(logging.INFO)



def write_data_file():
    for line in cached_html:
        f.write(line)
        f.flush()

class BaikemyCrawler(SimpleCrawler):
    def crawlStrategy(self, node_url):
        cached_html.clear()
        max_cache_size=0

        def push_html(url,html):
            logging.info("downloaded data from {} :\n{}...".format( url, html[:50]) )
            line=json.dumps({"url": url, "html": html})
            cached_html.append(line)
            if len(cached_html)>max_cache_size:
                write_data_file()
                cached_html.clear()

        def get_links_from_url(url):
            response = self.get(url)
            if not response:
                logging.warn("failed to fetch {}".format(url))
                return []
            logging.info("fetched %s" % url)
            
            #html = response.body.decode(errors="ignore")
            html= response.text
            push_html(url, html)
            return get_links(html)

        def remove_fragment(url):
            pure_url, frag = urldefrag(url)
            return pure_url

        def get_links(html):
            class URLSeeker(HTMLParser):
                def __init__(self):
                    HTMLParser.__init__(self)
                    self.urls = []

                def handle_starttag(self, tag, attrs):
                    href = dict(attrs).get("href")
                    if href and tag == "a":
                        href=urljoin(node_url, remove_fragment(href) )
                        if href.startswith(start_with):
                            self.urls.append(href)

            url_seeker = URLSeeker()
            url_seeker.feed(html)
            return url_seeker.urls

        return get_links_from_url(node_url)

if __name__ == "__main__":
    base_url="https://www.baikemy.com/disease/list/0/0?diseaseContentType=A"
    start_with="https://www.baikemy.com/disease/detail/"
    root_url="https://www.baikemy.com"

    data_category="disease"

    #open file to write
    cached_html=[]

    f=open(os.path.join(data_path, data_category+".json" ), "w", encoding="utf-8")

    BaikemyCrawler().startCrawler(base_url=base_url)

    write_data_file()

    #close file
    f.close()
