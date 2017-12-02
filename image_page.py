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


def _download(path, url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def collect_image(category_info):
    all_img_dataset = set()

    page_links = _get_all_page_link(category_info['link'])
    page_count = page_links.__len__()
    print("collect all image link")
    for index, link in enumerate(page_links):
        print("image page={0}/{1} link={2}".format(index + 1, page_count, link))
        all_img_dataset.update(_get_image_link(link))
#        time.sleep(1)
    print("\n")

    save_path = "{0}/{1}".format(category_info['page_path'], category_info['name'])
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    print("save image in {0}".format(save_path))
    img_count = all_img_dataset.__len__()
    for index, url in enumerate(all_img_dataset):
        extension = url.split(".")[-1]
        img_path = "{0}/{1}.{2}".format(save_path, index, extension)
        print("image={0}/{1} from={2} destination={3}".format(index + 1, img_count, url, img_path))
        _download(img_path, url)
#        time.sleep(2)
    print("\n")
