# -*- coding: UTF-8 -*-
import config
import main_page
import image_page
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time
import click
import configparser


@click.group()
def cli():
    if not os.path.exists(config.export_folder):
        os.makedirs(config.export_folder)
    if not os.path.exists(config.download_folder):
        os.makedirs(config.download_folder)


@click.command()
def start():
    page_links = main_page.get_all_page_link()

    page_count = page_links.__len__()
    for page, link in enumerate(page_links):
        print("main page={0}/{1} link={2}\n".format(page + 1, page_count, link))
        category_list = main_page.get_category_list(link)

        page_path = "{0}/{1}".format(config.download_folder, page)
        category_count = category_list.__len__()
        for index, category in enumerate(category_list):
            category_info = main_page.parser_category(page, category, page_path)
            print("category={0}/{1} name={2}\n".format(index + 1, category_count, category_info["name"]))
            image_page.download_image(category_info)


@click.command()
def pop():
    config_parser = configparser.RawConfigParser()
    page_links = main_page.get_all_page_link()

    config_parser.add_section("Page")
    for index, link in enumerate(page_links):
        config_parser.set("Page", str(index), link)

    config_parser.add_section("Other")
    config_parser.set("Other", "Count", len(page_links))

    config_parser.add_section("Download")
    config_parser.set("Download", "Timestamp", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    save_path = "{0}/main_page.cfg".format(config.export_folder)
    with open(save_path, 'w') as configfile:
        config_parser.write(configfile)


@click.command()
def push():
    config_parser = configparser.ConfigParser()
    config_parser.read("{0}/main_page.cfg".format(config.export_folder))

    count = int(config_parser.get("Other", "Count"))
    for index in range(0, count):
        print(config_parser.get("Page", str(index)))


cli.add_command(start)
cli.add_command(pop)
cli.add_command(push)


if __name__ == "__main__":
    cli()
