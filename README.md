# DoubanSpider
v 0.8
## Description
+ 基于个人兴趣，试图分析友邻之间的友好关系、兴趣重合程度等，故开发此项目。
+ 主要抓取数据包括用户、关注、图书、影视、音乐、游戏和舞台剧；
+ 评分之间的相似度暂时未完成。
+ 因为豆瓣于19.10.05被粉红击沉，动态功能被关闭。经验证发现书影音、日志、相册、广播等功能都正常，可以发布。于是紧急添加一项抓取动态的功能，帮助大家自行抓取友邻动态生成网页，达到自救效果。
+ 最后更新时间：2019.10.09

## Requirements
+ Python 3.6+
+ lxml
+ BeautifulSoup
+ requests

## Quick Start
### Install
+ 假设环境中已经有git和Python；
+ 在命令行界面输入：
```bash
git clone https://github.com/MagShadow/DoubanSpider.git
pip install beautifulsoup4
pip install requests
pip install lxml
```

## Reference
+ 一个已经存在的同名项目(https://github.com/lanbing510/DouBanSpider)，以作品为出发点，抓取豆瓣上的高分好书。