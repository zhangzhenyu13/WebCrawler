'''
how do a web try to anti-crawler:
1) limit the visist frequency of certain ip=> disconnect the connection when the connection frequency is too high, so we can try to sleep
2) block certain agent access after its visiting threshold is too high, ususally not adopted by webs due to its high error occurance
3)analysis cookies, usually not adopted by web
'''
import requests
import random
import time
from agentcrawler import config_path
import json
import os
import logging
from multiprocessing.dummy import Pool as ThreadPool
import collections

class BasicCrawler(object):

    def __init__(self):
        self.ip_list=[]
    
        with open(os.path.join(config_path,"ip_proxy"),"r") as f:
            for line in f:
                self.ip_list.append(line)

        self.user_agent_list=[]
        with open(os.join(config_path,"user_agent"),"r") as f:
            for line in f:
                self.user_agent_list.append(line)

        self.req_config=json.load(os.path.join(config_path,"req_config.json"))

        logging.info( "init with %d proxy ips and %d user agents"%(len(self.ip_list), len(self.user_agent_list) ) )

    def random_select(self):
        UA, IP= None, None
        if self.user_agent_list:
            UA=random.choice(self.user_agent_list)
        if self.ip_list:
            IP="".join(str(random.choice(self.ip_list)).strip())
        return UA, IP
    def get(self,url,params,timeout,proxy=None,num_retries=6):
        time_wait=self.req_config["time_wait"]

        for _ in range(num_retries, 0, -1):
            UA, IP= self.random_select()
            if UA:
                header={"User-Agent":UA}
            if IP:
                proxy={"http":IP}

            try:
                response=requests.get(url,params=params,headers=header,proxies=proxy,timeout=timeout)
                time_wait=self.req_config["time_wait"]
                time.sleep(time_wait)
                return response
            except:
                logging.warn("failed to access web, left trial times: %d"%(num_retries-1))
                time_wait=int(self.req_config["factor"]*time_wait)
                time.sleep(time_wait)
        
        logging.error("error requesting from {} with params as\n{}".format(url, params))

        return None

    def crawlStrategy(self, node_url):
        # get sub page links from node url
        raise NotImplementedError

    def startCrawler(self, concurrency=10, base_url=""):
        # concurrency is the threads number to run
        # workers=ThreadPool(concurrency)
        factor=5
        workers=ThreadPool(concurrency)
        fetching, fetched, dead= set(), set(), set()
        q=[]
        q.append(base_url)

        def push_urls(node_url):
            urls=self.crawlStrategy(node_url)
            for url in urls:
                if url is None or url in fetched or url in fetching:
                    continue
                q.append(url)

        while len(q)>0:
            if len(q)<concurrency*factor:
                node_url=q[0]
                del q[0]
                
                push_urls(node_url)
            else:
                batch=q[:factor*concurrency]
                q=q[factor*concurrency:]

                workers.map(push_urls, batch)

        workers.join()
        workers.close()
        