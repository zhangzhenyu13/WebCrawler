from agentcrawler.crawler import SimpleCrawler
from multiprocessing.dummy import Pool as ThreadPool

class MultiThreadCrawler(SimpleCrawler):
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
        