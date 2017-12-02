# -*- coding: UTF-8 -*-
import config
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re
import time
import requests
import shutil


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


def _get_image_link(url):
    img_dataset = set()

    bs_obj = BeautifulSoup(urlopen(url), "html.parser")
    replys_obj = bs_obj.find_all("div", {"class": "reply"})
    for index, reply in enumerate(replys_obj):
        image_links = reply.find_all("a", {"href": re.compile("src/\d+\.[a-zA-Z]+$")})
        for link in image_links:
            if "href" in link.attrs:
                img_dataset.add("http:" + link['href'])

    return img_dataset


def _download(path, url):
    print("path={0} url={1}".format(path, url))
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def collect_image(category_info):
    all_img_dataset = set()

    print(category_info)
    page_links = _get_all_page_link(category_info['link'])
    for page, link in enumerate(page_links):
        print("page={0} link={1}".format(page, link))
        all_img_dataset.update(_get_image_link(link))
        time.sleep(1)

    save_path = "{0}/{1}".format(category_info['page_path'], category_info['name'])
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for index, url in enumerate(all_img_dataset):
        extension = url.split(".")[-1]
        img_path = "{0}/{1}.{2}".format(save_path, index, extension)
        _download(img_path, url)
        time.sleep(2)
