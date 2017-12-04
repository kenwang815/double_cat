# Double Cat
For research ai to collect images, and enjoy your world.

## Python env dependency
1. python >= 3.6.2
1. pip install -r requirements.txt

# Save image path
```
double_cat/images/
```

# Save pack file path
```
double_cat/src/
```

# Command Line
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --page_url     TEXT  select a main page url
  --category_url TEXT  select a category page url
  --help         Show this message and exit.

Commands:
  download
  pack
  start
```

- pack - get all image url, and save to src folder.
```
python main.py pack

main page=1/54 link=http://rthost.cr.rs/sd/

category=1/15 name=饅饅來祭

collect all image link
image page=1/2 link=http://rthost.cr.rs/sd/pixmicat.php?res=383048&page_num=0
image page=2/2 link=http://rthost.cr.rs/sd/pixmicat.php?res=383048&page_num=1
category=2/15 name=無名氏
...
...
```

- download - load src folder to download images.
```
python main.py download

src/0/饅饅來祭.cfg
save images/0/饅饅來祭/1.jpg
save images/0/饅饅來祭/2.jpg
save images/0/饅饅來祭/3.jpg
save images/0/饅饅來祭/4.png
save images/0/饅饅來祭/5.jpg
save images/0/饅饅來祭/6.jpg
...
...
```

- start - search all url and download all image.
```
python main.py start

main page=1/54 link=http://rthost.cr.rs/sd/
category=1/15 name=饅饅來祭
collect all image link
image page=1/2 link=http://rthost.cr.rs/sd/pixmicat.php?res=383048&page_num=0
image page=2/2 link=http://rthost.cr.rs/sd/pixmicat.php?res=383048&page_num=1
save image in images/0/饅饅來祭
image=1/52 save images/0/饅饅來祭/0.png
image=2/52 save images/0/饅饅來祭/1.jpg
...
...
```

- start - select one page download.
```
python main.py start --page_url http://rthost.cr.rs/sd/pixmicat.php?page_num=28

00:53:55 - 69650:MainThread - __main__ - DEBUG - main page=29/54 link=http://rthost.cr.rs/sd/pixmicat.php?page_num=28
00:53:55 - 69650:MainThread - __main__ - DEBUG - category=1/15 name=腦殘記者祭
00:53:56 - 69650:MainThread - image_page - DEBUG - collect all image link
00:53:56 - 69650:MainThread - image_page - DEBUG - image page=1/1 link=http://rthost.cr.rs/sd/pixmicat.php?res=356759&page_num=0
00:53:56 - 69650:MainThread - image_page - DEBUG - save image in images/28/腦殘記者祭
00:53:56 - 69650:MainThread - image_page - DEBUG - image=1/8 save images/28/腦殘記者祭/0.jpg
00:53:56 - 69650:MainThread - urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): rths.cf
00:53:57 - 69650:MainThread - urllib3.connectionpool - DEBUG - http://rths.cf:80 "GET /sd/src/1439745949621.jpg HTTP/1.1" 200 108603
00:53:57 - 69650:MainThread - image_page - DEBUG - image=2/8 save images/28/腦殘記者祭/1.jpg
...
...
```

- start - select one category download.
```
python main.py start --category_url http://rthost.cr.rs/sd/pixmicat.php?res=294406

01:38:52 - 71517:MainThread - __main__ - DEBUG - category=8/15 name=啟萌祭
01:38:52 - 71517:MainThread - image_page - DEBUG - collect all image link
01:38:52 - 71517:MainThread - image_page - DEBUG - image page=1/6 link=http://rthost.cr.rs/sd/pixmicat.php?res=294406&page_num=0
01:38:52 - 71517:MainThread - image_page - DEBUG - image page=2/6 link=http://rthost.cr.rs/sd/pixmicat.php?res=294406&page_num=1
01:38:53 - 71517:MainThread - image_page - DEBUG - image page=3/6 link=http://rthost.cr.rs/sd/pixmicat.php?res=294406&page_num=2
01:38:53 - 71517:MainThread - image_page - DEBUG - image page=4/6 link=http://rthost.cr.rs/sd/pixmicat.php?res=294406&page_num=3
01:38:53 - 71517:MainThread - image_page - DEBUG - image page=5/6 link=http://rthost.cr.rs/sd/pixmicat.php?res=294406&page_num=4
01:38:54 - 71517:MainThread - image_page - DEBUG - image page=6/6 link=http://rthost.cr.rs/sd/pixmicat.php?res=294406&page_num=5
01:38:54 - 71517:MainThread - image_page - DEBUG - save image in images/11/啟萌祭
01:38:54 - 71517:MainThread - image_page - DEBUG - image=1/150 save images/11/啟萌祭/0.gif
01:38:54 - 71517:MainThread - urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): rths.cf
```