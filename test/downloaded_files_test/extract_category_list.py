from agentcrawler.utils.content_list import load_list_urls
import logging
logging.getLogger(__name__).setLevel(logging.ERROR)

def test_url_list(root_url, data_category, start_with):
    
    urls=load_list_urls(data_category,start_with,root_url)
    print("{}: {} urls".format(data_category,len(urls)))
    print(urls[:10])

    print("="*100)

if __name__ == "__main__":
    #medicines
    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="medicines",
        start_with="https://www.baikemy.com/medicine/detail/"
    )
    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="medicineguide",
        start_with="https://www.baikemy.com/medicine/detail/"
    )

    #diseases
    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="diseases",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="symptoms",
        start_with="https://www.baikemy.com/disease/detail/"
    )


    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="checkover",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="treatments",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="chinesemedicine",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="prevention",
        start_with="https://www.baikemy.com/disease/detail/"
    )

    test_url_list(
        root_url="https://www.baikemy.com/",
        data_category="care",
        start_with="https://www.baikemy.com/disease/detail/"
    )