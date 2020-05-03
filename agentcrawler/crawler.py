'''
Base Crawler Definition
'''

class CrawlerBase:
    def __init__(self,**kwargs):
        pass
    
    def get(self,**kwargs):
        raise NotImplementedError
    def crawlStrategy(self):
        # get sub page links from node url
        raise NotImplementedError
    def startCrawler(self,**kwargs):
        #start crawling data
        raise NotImplementedError

    

