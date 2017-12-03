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
  --help  Show this message and exit.

Commands:
  download
  pack
  start
```

- pack
get all image url, and save to src folder.
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

- download
load src folder to download images.
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

- start
search url and download image.
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
image=3/52 save images/0/饅饅來祭/2.jpg
image=4/52 save images/0/饅饅來祭/3.jpg
image=5/52 save images/0/饅饅來祭/4.png
image=6/52 save images/0/饅饅來祭/5.jpg
image=7/52 save images/0/饅饅來祭/6.jpg
image=8/52 save images/0/饅饅來祭/7.png
...
...
```