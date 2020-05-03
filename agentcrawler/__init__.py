import os
import json
project_path="/home/zhangzy/WebCrawler"
config_path=os.path.join(project_path,"config")
data_path=os.path.join(project_path,"data")

class CrawlerConfig:
    def __init__(self, config_file=None):
        self.config={}
        if config_file:
            self.loadConfig(config_file=config_file)

    def loadConfig(self,config_file):
        with open(config_file, "r", encoding="utf-8") as f:
           config=json.load(f) 
        
        self.config=config
        #print(type(self.config), self.config, self.config.items())
        def loadConfigCore(config_dict):

            for k, v in self.config.items():
                if type(v)==dict():
                    setattr(self, k, loadConfigCore(v))
                else:
                    setattr(self, k, v)

        loadConfigCore(self.config)

if __name__ == "__main__":
    config_file=os.path.join(config_path,"req_config.json")
    print(CrawlerConfig(config_file))