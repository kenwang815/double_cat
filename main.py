# -*- coding: UTF-8 -*-
import logging.config
import logging_config
import config
import main_page
import image_page
import os
import click
import configparser
import utils


log = logging.getLogger(__name__)


@click.group()
@click.option("--page_url", type=str, help="select a main page url")
@click.option("--category_url", type=str, help="select a category page url")
def cli(page_url, category_url):
    if not os.path.exists(config.export_folder):
        os.makedirs(config.export_folder)
    if not os.path.exists(config.download_folder):
        os.makedirs(config.download_folder)


def download_page_image(page, link, page_count):
    log.debug("main page={0}/{1} link={2}\n".format(page + 1, page_count, link))
    category_list = main_page.get_category_list(link)

    save_folder_path = "{0}/{1}".format(config.download_folder, page)
    category_count = category_list.__len__()
    for index, category in enumerate(category_list):
        log.debug("category={0}/{1} name={2}\n".format(index + 1, category_count, category["name"]))
        image_page.download_image(category, save_folder_path)


def download_category_image(page, link, category_url):
    category_list = main_page.get_category_list(link)

    save_folder_path = "{0}/{1}".format(config.download_folder, page)
    category_count = category_list.__len__()
    for index, category in enumerate(category_list):
        if category["link"] == category_url:
            log.debug("category={0}/{1} name={2}\n".format(index + 1, category_count, category["name"]))
            image_page.download_image(category, save_folder_path)
            break


@click.command()
@click.option("--page_url", type=str, help="select a main page url")
@click.option("--category_url", type=str, help="select a category page url")
def start(page_url, category_url):
    page_links = main_page.get_all_page_link()

    page_count = page_links.__len__()
    if page_url is not None:
        for page, link in enumerate(page_links):
            if link == page_url:
                download_page_image(page, link, page_count)
                break
    elif category_url is not None:
        for page, link in enumerate(page_links):
            download_category_image(page, link, category_url)
    else:
        for page, link in enumerate(page_links):
            download_page_image(page, link, page_count)


@click.command()
def pack():
    page_links = main_page.get_all_page_link()
    image_page.pack(page_links)


@click.command()
def download():
    for dirPath, dirNames, fileNames in os.walk(config.export_folder):
        for f in fileNames:
            img_cfg = os.path.join(dirPath, f)
            log.debug(img_cfg)
            config_parser = configparser.ConfigParser()
            config_parser.read(img_cfg)

            save_path = config_parser.get("Path", "download")
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            count = int(config_parser.get("Other", "Count"))
            for index in range(0, count):
                url = config_parser.get("Image", str(index))
                img_path = "{0}/{1}.{2}".format(save_path, index + 1, url.split(".")[-1])
                utils.download(img_path, url)
                log.debug("save {}".format(img_path))

            os.remove(img_cfg)

cli.add_command(start)
cli.add_command(pack)
cli.add_command(download)


if __name__ == "__main__":
    logging.config.dictConfig(logging_config.DEV)
    cli()
