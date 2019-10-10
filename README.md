# DoubanSpider
v 0.8.1

## Description
+ 基于个人兴趣，试图分析友邻之间的友好关系、兴趣重合程度等，故开发此项目。
+ 主要抓取数据包括用户、关注、图书、影视、音乐、游戏和舞台剧；
+ 评分之间的相似度暂时未完成。
+ 因为豆瓣于19.10.05被粉红击沉，动态功能被关闭。经验证发现书影音、日志、相册等除广播以外的功能都正常，可以发布。于是紧急添加一项抓取动态的功能，帮助大家自行抓取友邻动态生成网页，达到自救效果。
+ 最后更新时间：2019.10.10

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

### Config
+ 安装完成后在当前目录下应该有DoubanSpider文件夹，进入该文件夹；
+ 在src文件夹下建立config.json，格式如下：
```
{
    "user": "<user_id>",
    "email": "<email>",
    "pswd": "<password>",
    "waiting": 1
}
```
+ 各参数含义如下：
    + user: 你的用户ID。点击“我的豆瓣”后查看网址栏，在`/people/`后接着的那一串数字/字母就是你的ID。
    + email：登录使用的邮箱。
    + pswd：你的密码。
    + waiting：默认两次查询之间的等待间隔。单位是秒，建议不要小于1，否则可能因为查询太快被豆瓣判定为机器人。

### Usage
+ 在DoubanSpider目录下，使用以下命令运行程序：
```bash
python ./src/DBspider.py <option> <paras>
```
+ 其中option暂时只实现了三种，分别是：
    + "-h"：查看帮助。
    + "-i"：爬取用户资料。爬取内容包括关注/被关注列表，图书/影视/音乐/游戏/舞台剧的想看/在看/看过记录及评分。在-i后可以接目标用户id，如什么都不接则默认为爬取自己的资料。爬取后资料存储在`data/`文件夹下。
    + "-s"：爬取用户好友动态，模拟崩溃前的豆瓣首页。-s后可接用户id，如不接则默认为爬取自己的时间线。可加-t参数，此后接一个数字表示爬取的天数，默认为1。爬取后在`data/<user_id>/`文件夹下会生成一个html文件，打开即是你应当看到的主页时间线。
+ 例：
```bash
python ./src/DBspider.py -i
python ./src/DBspider.py -i chuapp
python ./src/DBspider.py -s -t 5
```

## Problems
+ 目前已知的未解决的问题有：
    + 爬取动态生成的网页中，“转发”按钮失灵；解决办法是先点回应/赞跳转到对应页面再进行转发。
+ 常见问题有：
    + 如果遇到爬取contact的时候报错，那么很可能是没有成功登录，可以检查一下login中间s.post()的返回值是否正常。

## Outlooks
+ 下一步会完成用户相似度比较和用户个人好友报表生成的功能。

## Reference
+ 一个已经存在的同名项目( https://github.com/lanbing510/DouBanSpider )，以作品为出发点，抓取豆瓣上的高分好书。