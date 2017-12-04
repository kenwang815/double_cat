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
        category_info["link"] = config.url + links[0].attrs["href"]
    except KeyError as e:
        log.debug(e)
        category_info["link"] = None

    return category_info


def pack(page_links):
    config_parser = configparser.RawConfigParser()

    config_parser.add_section("Page")
    for index, link in enumerate(page_links):
        config_parser.set("Page", str(index), link)

    config_parser.add_section("Other")
    config_parser.set("Other", "Count", len(page_links))
    config_parser.set("Other", "Timestamp", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    save_path = "{0}/main_page.cfg".format(config.export_folder)
    with open(save_path, 'w') as configfile:
        config_parser.write(configfile)
