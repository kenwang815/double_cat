# -*- coding: UTF-8 -*-
import config
import main_page
import image_page
import os
import click
import configparser
import utils


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

        save_folder_path = "{0}/{1}".format(config.download_folder, page)
        category_count = category_list.__len__()
        for index, category in enumerate(category_list):
            print("category={0}/{1} name={2}\n".format(index + 1, category_count, category["name"]))
            image_page.download_image(category, save_folder_path)


@click.command()
def pack():
    page_links = main_page.get_all_page_link()
    image_page.pack(page_links)


@click.command()
def download():
    for dirPath, dirNames, fileNames in os.walk(config.export_folder):
        for f in fileNames:
            img_cfg = os.path.join(dirPath, f)
            print(img_cfg)
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
                print("save {}".format(img_path))


cli.add_command(start)
cli.add_command(pack)
cli.add_command(download)


if __name__ == "__main__":
    cli()
