from tornado import httpclient, httputil, queues, gen
import asyncio
import requests
from agentcrawler.crawler import BasicCrawler
import logging, time
import collections
from datetime import timedelta

class AsyncCrawler(BasicCrawler):
    async def get(self,url,params,timeout,proxy=None,num_retries=6):
        time_wait=self.req_config["time_wait"]

        for _ in range(num_retries, 0, -1):
            UA, IP= self.random_select()
            if UA:
                header={"User-Agent":UA}
            if IP:
                proxy={"http":IP}

            try:
                response= await httpclient.AsyncHTTPClient().fetch(url,params=params,headers=header,proxies=proxy,timeout=timeout)
                time_wait=self.req_config["time_wait"]
                asyncio.sleep(time_wait)
                return response
            except:
                logging.warn("failed to access web, left trial times: %d"%(num_retries-1))
                time_wait=int(self.req_config["factor"]*time_wait)
                await asyncio.sleep(time_wait)
        
        logging.error("error requesting from {} with params as\n{}".format(url, params))
        return None

    async def crawlStrategy(self, node_url):
        raise NotImplementedError

    async def startCrawler(self,concurrency=10,base_url=""):
        #use Level Traverse via the tornado async queue to walk the web pages of base_url
        #concurrency is the number of workers/coroutines to run 

        q = queues.Queue()
        start = time.time()
        fetching, fetched, dead = set(), set(), set()
        
        async def fetch_url(current_url):
            if current_url in fetching or current_url in fetched:
                return

            print("fetching %s" % current_url)
            fetching.add(current_url)
            urls = await self.crawlStrategy(current_url)
            fetched.add(current_url)

            for new_url in urls:
                # Only follow links beneath the base URL
                if new_url.startswith(base_url):
                    await q.put(new_url)

        async def worker():
            async for url in q:
                if url is None:
                    return
                try:
                    await fetch_url(url)
                except Exception as e:
                    logging.error("Exception: %s %s" % (e, url))
                    dead.add(url)
                finally:
                    q.task_done()

        await q.put(base_url)

        # Start workers, then wait for the work queue to be empty.
        workers = gen.multi([worker() for _ in range(concurrency)])
        await q.join(timeout=timedelta(seconds=self.req_config["time_wait"]))
        assert fetching == (fetched | dead)
        logging.info("Done in %d seconds, fetched %s URLs." % (time.time() - start, len(fetched)))
        logging.info("Unable to fetch %s URLS." % len(dead))

        # Signal all the workers to exit.
        for _ in range(concurrency):
            await q.put(None)
        await workers