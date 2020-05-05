import os
from agentcrawler import data_path

urls_file=os.path.join(data_path, "downloaded_urls.txt")

def get_downloaded_urls():
    urls=set()

    if not os.path.exists(urls_file):
        return urls

    with open(urls_file, "r", encoding="utf-8") as f:
        for line in f:
            if line:
                urls.add(line.strip("\n"))
    return urls

def save_downloaded_urls(urls): 
    def line_check(line):
        if not "".endswith("\n"):
            line+="\n"
        return line
    with open(urls_file, "w", encoding="utf-8") as f:
        
        urls=filter(lambda s: s ,map(line_check, urls) )
        f.writelines(urls)