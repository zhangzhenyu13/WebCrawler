'''
how do a web try to anti-crawler:
1) limit the visist frequency of certain ip=> disconnect the connection when the connection frequency is too high, so we can try to sleep
2) block certain agent access after its visiting threshold is too high, ususally not adopted by webs due to its high error occurance
3)analysis cookies, usually not adopted by web
'''

from agentcrawler.crawler import CrawlerBase
import requests
import random
import time
from agentcrawler import config_path
import json
import os
import logging
import collections
from agentcrawler import CrawlerConfig

class SimpleCrawler(CrawlerBase):

    def __init__(self):
        self.ip_list=[]
    
        with open(os.path.join(config_path,"ip_proxy"),"r") as f:
            for line in f:
                self.ip_list.append(line)

        self.user_agent_list=[]
        with open(os.path.join(config_path,"user_agent"),"r") as f:
            for line in f:
                self.user_agent_list.append(line)

        self.req_config=CrawlerConfig(config_file=os.path.join(config_path,"req_config.json") )

        logging.info( "simple crawler init with %d proxy ips and %d user agents"%(len(self.ip_list), len(self.user_agent_list) ) )

    def _random_select(self):
        UA, IP= None, None
        if self.user_agent_list:
            UA=random.choice(self.user_agent_list)
        if self.ip_list:
            IP="".join(str(random.choice(self.ip_list)).strip())
        return UA, IP

    def get(self,url):
        time_wait=self.req_config.time_wait
        header, proxy= None, None
        for left_retry in range(self.req_config.num_retry, 0, -1):
            UA, IP= self._random_select()
            if UA:
                header={"User-Agent":UA}
            if IP:
                proxy={"http":IP}

            try:
                response=requests.get(url,headers=header,proxies=proxy,timeout=self.req_config.timeout)
                time_wait=self.req_config.time_wait
                time.sleep(time_wait)
                return response
            except Exception as e:
                logging.warn("{},failed to access web, left trial times: {}".format(e.args ,left_retry-1))
                time_wait=int(self.req_config.factor*time_wait)
                time.sleep(time_wait)
        
        logging.error("error requesting from {}".format(url))

        return None

    def startCrawler(self, base_url):
        #start crawling data from a base url (init seed)
        fetching, fetched, dead= list(), set(), set()
        fetching.append(base_url)

        def push_urls(node_url):
            try:
                urls=self.crawlStrategy(node_url)
                for url in urls:
                    if url is None or url in fetched or url in fetching:
                        continue
                    fetching.append(url)

                fetched.add(node_url)
            except Exception as e:
                e.with_traceback()
                dead.add(node_url)

        while len(fetching)>0:
            node_url=fetching[0]
            del fetching[0]
            
            push_urls(node_url)
        
        logging.info("crawled urls \nfetched：{}， failed: {} ".format(len(fetched), len(dead)))
