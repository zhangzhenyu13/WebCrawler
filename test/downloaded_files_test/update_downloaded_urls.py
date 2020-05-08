import os
import json
from agentcrawler import data_path
from agentcrawler.utils.manage_downloaded_files import save_downloaded_urls, get_downloaded_urls

downloaded_urls_file_name="downloaded_urls.txt"
def get_json_files():
    files=[]
    for file_name in os.listdir(data_path):
        if file_name!=downloaded_urls_file_name:
            files.append(file_name)
    
    return files

def extract_downloaded_urls(data_file):
    if not os.path.exists(data_file):
        print(data_file, "not found")
        return 
    
    size=len(downloaded_urls)
    with open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            url=json.loads(line)["url"]
            downloaded_urls.add(url)

    print("current file %s, total %d urls extracted"%(data_file, len(downloaded_urls)-size) )

if __name__ == "__main__":
    files= get_json_files()
    downloaded_urls=set()
    downloaded_urls.clear()
    for file_name in files:
        extract_downloaded_urls(os.path.join(data_path, file_name))

    save_downloaded_urls(downloaded_urls)    

    downloaded_urls=get_downloaded_urls()
    print("downloaded", len(downloaded_urls), "urls")
    print(list(downloaded_urls)[:5])

