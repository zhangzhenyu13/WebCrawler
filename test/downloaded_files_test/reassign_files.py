from agentcrawler.utils.manage_downloaded_files import re_assign_data
from agentcrawler.utils.content_list import load_list_urls, load_meta_category


category_data={}

def add_content_source(root_url, data_category, start_with):
    
    urls=load_list_urls(data_category,start_with,root_url)
    category_data[data_category]=urls

def load_category_data():

    #medicines
    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="medicines",
        start_with="https://www.baikemy.com/medicine/detail/"
    )
    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="medicineguide",
        start_with="https://www.baikemy.com/medicine/detail/"
    )

    #diseases
    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="diseases",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="symptoms",
        start_with="https://www.baikemy.com/disease/detail/"
    )


    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="checkover",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="treatments",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="chinesemedicine",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="prevention",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    add_content_source(
        root_url="https://www.baikemy.com/",
        data_category="care",
        start_with="https://www.baikemy.com/disease/detail/"
    )

