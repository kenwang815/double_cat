# -*- coding: UTF-8 -*-
import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

log = logging.getLogger(__name__)
origin_url = "http://rthost.cr.rs/sd/"


# --------- main page ---------
def get_all_page_link():
    links = list()
    links.append(origin_url)

    bs_obj = BeautifulSoup(urlopen(origin_url), "html.parser")
    page_table = bs_obj.find("div", {"id": "page_switch"})
    for link in page_table.find_all("a"):
        if "href" in link.attrs:
            links.append(origin_url + link.attrs["href"])

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
        category_info["url"] = origin_url + links[0].attrs["href"]
    except KeyError as e:
        log.debug(e)
        category_info["url"] = None

    category_info["count"] = 0

    return category_info


# --------- category page ---------
def _parser_obj(obj):
    img_info = dict()
    image_links = obj.find("a", {"href": re.compile("src/\d+\.[a-zA-Z]+$")})
    if image_links is None:
        return None

    # 無標題 名稱: 無名氏 [17/12/17(日)16:21 ID:5W6YyzKY/c/BS] No.383786  檔名：1513498904473.jpg-(367 KB, 800x3436) [以預覽圖顯示]
    pattern = r"檔名：(?P<name>\d+?)\.(?P<extension>\w+?)-\((?P<size>\d+?) (?P<unit>\w+?), (?P<width>\w+?)x(?P<height>\w+?)\)"
    img_info.update(re.search(pattern, obj.get_text()).groupdict())

    if len(image_links) > 1:
        for link in image_links:
            if "href" in link.attrs:
                img_info["url"] = "http:" + link['href']
    else:
        if "href" in image_links.attrs:
            img_info["url"] = "http:" + image_links['href']

    return img_info


def _get_image_link(url):
    img_dataset = list()

    bs_obj = BeautifulSoup(urlopen(url), "html.parser")
    title_obj = bs_obj.find("div", {"id": "threads"})
    link = _parser_obj(title_obj)
    if link is not None:
        img_dataset.append(link)

    replys_obj = bs_obj.find_all("div", {"class": "reply"})
    for reply in replys_obj:
        link = _parser_obj(reply)
        if link is not None:
            img_dataset.append(link)

    return img_dataset


def _get_all_page_link(url):
    links = list()

    bs_obj = BeautifulSoup(urlopen(url), "html.parser")
    page_table = bs_obj.find("div", {"id": "page_switch"}).td.next_sibling
    for link in page_table.find_all("a", {"href": re.compile("[0-9]$")}):
        if "href" in link.attrs:
            links.append(url + link.attrs["href"])

    current_page = "{0}&page_num={1}".format(url, page_table.find("b").get_text())
    links.append(current_page)

    return links


def collect_image_link(category_info):
    all_img_dataset = list()

    page_links = _get_all_page_link(category_info['url'])
    page_count = page_links.__len__()
    log.debug("collect all image link")
    for index, link in enumerate(page_links):
        log.debug("image page={0}/{1} link={2}".format(index + 1, page_count, link))
        all_img_dataset.extend(_get_image_link(link))

    return all_img_dataset


if __name__ == "__main__":
    collect_image_link({"url": "http://rthost.cr.rs/sd/pixmicat.php?res=383048"})
