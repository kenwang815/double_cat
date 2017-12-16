# -*- coding: UTF-8 -*-
import logging
import config
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import configparser
import time

log = logging.getLogger(__name__)


def get_all_page_link():
    links = list()
    links.append(config.url)

    bs_obj = BeautifulSoup(urlopen(config.url), "html.parser")
    page_table = bs_obj.find("div", {"id": "page_switch"})
    for link in page_table.find_all("a"):
        if "href" in link.attrs:
            links.append(config.url + link.attrs["href"])

    return links


def get_category_list(link):
    category_list = list()
    html = urlopen(link)
    bs_obj = BeautifulSoup(html, "html.parser")
    category_tag = bs_obj.find_all("div", {"class": "grid"})

    for category in category_tag:
        category_list.append(_parser_category(category))

    return category_list


def _parser_category(category):
    category_info = dict()
    title = category.find("span", {"class": "title"}).get_text()
    if title == "無標題":
        category_info["name"] = category.find("span", {"class": "name"}).get_text()
    else:
        category_info["name"] = title

    category_info["name"] = category_info["name"].replace("/", " ")

    try:
        links = category.find_all("a", {"href": re.compile("res=[^#]*$")})
        category_info["url"] = config.url + links[0].attrs["href"]
    except KeyError as e:
        log.debug(e)
        category_info["url"] = None

    category_info["count"] = 0

    return category_info
