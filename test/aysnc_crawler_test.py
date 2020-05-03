from agentcrawler.async_crawler import AsyncCrawler
import uuid
from tornado import ioloop
import functools
import logging
import os
from agentcrawler import data_path
from urllib.parse import urljoin, urldefrag
from html.parser import HTMLParser

def create_uid():
    return str(uuid.uuid1())+".html"
def write_data_file():
    for html in cached_html:
        with open(os.path.join(data_path, create_uid()), "w", encoding="utf-8") as f:
            f.write(html)

class BaikemyCrawler(AsyncCrawler):
    async def crawlStrategy(self, node_url):
        cached_html=[]
        max_cache_size=100
        
        async def push_html(html):
            cached_html.append(html)
            if len(html)>max_cache_size:
                write_data_file()

        async def get_links_from_url(url):
            response = await self.get(url)
            logging.info("fetched %s" % url)
            
            html = response.body.decode(errors="ignore")
            await push_html(html)
            return [urljoin(url, remove_fragment(new_url)) for new_url in get_links(html)]

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

                        self.urls.append(href)

            url_seeker = URLSeeker()
            url_seeker.feed(html)
            return url_seeker.urls

if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    base_url="https://www.baikemy.com/disease/list/0/0?diseaseContentType=A"
    start_with="https://www.baikemy.com/disease/"
    root_url="https://www.baikemy.com"

    cached_html=[]

    run_func=functools.partial(BaikemyCrawler.startCrawler, concurrency=10, base_url=base_url)
    io_loop.run_sync(run_func)

    write_data_file()