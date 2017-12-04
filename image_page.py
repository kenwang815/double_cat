# -*- coding: UTF-8 -*-
import logging
import config
import main_page
import utils
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re
import configparser
import time


log = logging.getLogger(__name__)


def _get_all_page_link(url):
    links = list()

    bs_obj = BeautifulSoup(urlopen(url), "html.parser")
    page_table = bs_obj.find("div", {"id": "page_switch"}).td.next_sibling
    for link in page_table.find_all("a", {"href": re.compile("[0-9]$")}):
        if "href" in link.attrs:
            links.append(config.url + link.attrs["href"])

    current_page = "{0}&page_num={1}".format(url, page_table.find("b").get_text())
    links.append(current_page)

    return links


def parser_obj(obj):
    img_link = None
    image_links = obj.find("a", {"href": re.compile("src/\d+\.[a-zA-Z]+$")})
    if image_links is None:
        return img_link

    if len(image_links) > 1:
        for link in image_links:
            if "href" in link.attrs:
                img_link = "http:" + link['href']
    else:
        if "href" in image_links.attrs:
            img_link = "http:" + image_links['href']

    return img_link


def _get_image_link(url):
    img_dataset = set()

    bs_obj = BeautifulSoup(urlopen(url), "html.parser")
    title_obj = bs_obj.find("div", {"id": "threads"})
    link = parser_obj(title_obj)
    if link is not None:
        img_dataset.add(link)

    replys_obj = bs_obj.find_all("div", {"class": "reply"})
    for reply in replys_obj:
        link = parser_obj(reply)
        if link is not None:
            img_dataset.add(link)

    return img_dataset


def collect_image_link(category_info):
    all_img_dataset = set()

    page_links = _get_all_page_link(category_info['link'])
    page_count = page_links.__len__()
    log.debug("collect all image link")
    for index, link in enumerate(page_links):
        log.debug("image page={0}/{1} link={2}".format(index + 1, page_count, link))
        all_img_dataset.update(_get_image_link(link))

    return all_img_dataset


def download_image(category_info, save_folder_path):
    all_img_dataset = collect_image_link(category_info)

    save_path = "{0}/{1}".format(save_folder_path, category_info['name'])
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    log.debug("save image in {0}".format(save_path))
    img_count = all_img_dataset.__len__()
    for index, url in enumerate(all_img_dataset):
        extension = url.split(".")[-1]
        img_path = "{0}/{1}.{2}".format(save_path, index, extension)
        log.debug("image={0}/{1} save {2}".format(index + 1, img_count, img_path))
        utils.download(img_path, url)


def pack(page_links):
    page_count = page_links.__len__()
    for page, link in enumerate(page_links):
        log.debug("main page={0}/{1} link={2}\n".format(page + 1, page_count, link))
        category_list = main_page.get_category_list(link)

        save_folder_path = "{0}/{1}".format(config.export_folder, page)
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)

        category_count = category_list.__len__()
        for index, category in enumerate(category_list):
            log.debug("category={0}/{1} name={2}\n".format(index + 1, category_count, category["name"]))
            image_links = collect_image_link(category)
            config_parser = configparser.RawConfigParser()

            config_parser.add_section("Page")
            config_parser.set("Page", "index", str(page))
            config_parser.set("Page", "link", link)

            config_parser.add_section("Category")
            config_parser.set("Category", "index", str(index))
            config_parser.set("Category", "name", category["name"])
            config_parser.set("Category", "link", category["link"])

            config_parser.add_section("Image")
            for index, link in enumerate(image_links):
                config_parser.set("Image", str(index), link)

            config_parser.add_section("Path")
            config_parser.set("Path", "download", "{0}/{1}/{2}".format(config.download_folder, page, category["name"]))

            config_parser.add_section("Other")
            config_parser.set("Other", "Count", image_links.__len__())
            config_parser.set("Other", "Timestamp", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            save_path = "{0}/{1}.cfg".format(save_folder_path, category["name"])
            with open(save_path, 'w') as configfile:
                config_parser.write(configfile)
