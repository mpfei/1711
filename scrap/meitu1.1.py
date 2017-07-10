#coding=utf-8
#可以爬取百度贴吧任意贴吧指定页数的帖子中指定页数的所有图片
#42行可以设置爬取帖子的页数
#65行可以设置爬去的帖子中的页数
#delay指定间隔时间，可以解注释37行和61行进行时间延时
import urllib2
import re
import Queue
import lxml
from bs4 import BeautifulSoup
import time

num = 0
#存储帖子地址的队列
tieq = Queue.Queue()
delay = 3
height = 0
width = 0
#打开起始链接，识别其中的帖子链接，并将其放入tieq这个队列中进行存储
#百度贴吧中，帖子的链接class为j_th_tit 
def startScrap(url):
    global height
    print "start downloading page:%d"%height
    try:
        web = urllib2.urlopen(url)
        content = web.read()
        html = lxml.etree.HTML(content)
    except Exception as e:
        print "error with:%s"%e.message
        return
    result = html.xpath('//a[@class="j_th_tit "]')
    for u in result:
        tieurl = "https://tieba.baidu.com%s"%u.get('href')
        tieq.put(tieurl)
    while not tieq.empty():
        findimage(tieq.get())
        #time.sleep(delay)
    nextResult = html.xpath('//a[@class="next pagination-item "]')
    if nextResult is not None:
        for u in nextResult:
            nextUrl = "https:%s"%u.get('href')
            if height < 2:
                height+=1
                startScrap(nextUrl)
#将发现的帖子链接传入，打开帖子后，识别其中的图片链接
#百度贴吧的中，帖子里的图片class属性为BDE_Image
def findimage(url):
    global width
    print "downloading bbs page:%d"%width
    try:
        web = urllib2.urlopen(url)
        content = web.read()
        html = lxml.etree.HTML(content)
    except Exception as e:
        print "error with:%s"%e.message
        return
    result = html.xpath('//img[@class="BDE_Image"]')
    for u in result:
        picurl = u.get('src')
        downloadPic(picurl)
        #time.sleep(delay)
    nextResult = html.xpath('//a')
    for u in nextResult:
        if u.text == u"下一页":
            if width < 2:
                print "find next page!"
                width += 1
                findimage("https://tieba.baidu.com%s"%u.get('href'))
            else:
                width = 0
#将图片的链接地址传入，下载图片到指定文件中
def downloadPic(url):
    global num
    print "downloading:%s..."%url
    try:
        response = urllib2.urlopen(url)
        content = response.read()
    except Exception as e:
        print "downloading error reasion is:%s"%e.message
        return
    try:
        filename = "%d.%s"%(num,re.findall(r'(jpg| jpeg|JPG|JPEG|PNG|GIT|png|gif)+',url)[0])
        num+=1
        f = open(filename,"w")
        f.write(content)
    except IOError:
        print "file error"

#起始的url
starturl = 'https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%9B%BE&ie=utf-8'
startScrap(starturl)






