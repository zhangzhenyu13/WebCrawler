import os
from agentcrawler import data_path
import json

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


def re_assign_data(data:list, metadata_categories:dict, categories:list):
    files={
        category: open(os.path.join(data_path, category+".json"), "r", encoding="utf-8") for category in categories
    }
    files["other"]=open(os.path.join(data_path, "others.json"), "r", encoding="utf-8")

    for line in data:
        record=json.loads(line)
        url=record["url"]
        if url in metadata_categories:
            category=metadata_categories[url]
            files[category].write(line)

    [f.close() for f in files.values()]
    