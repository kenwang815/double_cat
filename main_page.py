# -*- coding: UTF-8 -*-
import config
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def get_all_page_link():
    links = list()
    links.append(config.url)

    bs_obj = BeautifulSoup(urlopen(config.url), "html.parser")
    page_table = bs_obj.find("div", {"id": "page_switch"})
    for link in page_table.find_all("a"):
        if "href" in link.attrs:
            links.append(config.url + link.attrs["href"])

    return links


def parser_category(page, category, page_path):
    category_info = dict()
    category_info["page"] = page
    category_info["page_path"] = page_path
    category_info["name"] = category.find("span", {"class": "title"}).get_text()

    try:
        links = category.find_all("a", {"href": re.compile("res=[^#]*$")})
        category_info["link"] = config.url + links[0].attrs["href"]
    except KeyError as e:
        print(e)
        category_info["link"] = None

    return category_info
