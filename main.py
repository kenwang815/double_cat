# -*- coding: UTF-8 -*-
import config
import main_page
import image_page
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time


if __name__ == "__main__":
    if not os.path.exists(config.download_folder):
        os.makedirs(config.download_folder)

    page_links = main_page.get_all_page_link()

    page_count = page_links.__len__()
    for page, link in enumerate(page_links):
        print("main page={0}/{1} link={2}\n".format(page + 1, page_count, link))
        html = urlopen(link)
        bs_obj = BeautifulSoup(html, "html.parser")
        category_list = bs_obj.find_all("div", {"class": "grid"})

        page_path = "{0}/{1}".format(config.download_folder, page)
        category_count = category_list.__len__()
        for index, category in enumerate(category_list):
            category_info = main_page.parser_category(page, category, page_path)
            print("category={0}/{1} name={2}\n".format(index + 1, category_count, category_info["name"]))
            image_page.collect_image(category_info)

#        time.sleep(5)
        print("\n")
