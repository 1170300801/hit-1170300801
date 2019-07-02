#_*_ coding:utf-8 _*_
#__date__='2018-08-27'
#爬取wallhaven上的的图片，支持自定义搜索关键词，自动爬取并该关键词下所有图片并存入本地电脑。
import os
import requests
import time
from progressbar import *
from lxml import etree
from threading import Thread

print('This software is for those who dig high-resolution wallpapers.\nBy inputing the keyword and pages you wanna download, breathtaking(or pantsdropping LOL) pictures will be automatically downloaded to your computer.\nIt will be located where this program located.\nDo enjoy! \n')
print('\n')
print('这个软件是为那些喜欢高像素壁纸的人服务的。通过输入关键词和想下载的页数，你就能将大量的高质量图片下到你的电脑中。默认存储地点是该程序所在地址。')
print('\n')
print('By J.Zehao\n')
print('\n')
print('-h : get help(获取帮助)\n')
print('\n')
print('-t : get tags(获取提示标签)\n')
print('\n')

tf = 1
while(tf == 1):
    keyWord = input(f"{'Please input the keywords that you want to download : '}")
    keyWord = keyWord.lower()
    print('\n')
    if keyWord == '-h':
        print('You can input keyword(tags) to download what you like. \nThen it will show how many images are there available for you to download.\ninput how many pages you wanna download. Normally, there will be 24 pics per page.')
        print('\n')
        print('你可以输入想下载的内容的关键词(标签)。软件将告诉你有多少张图片供下载。输入你想下载的页面数(一个页面有24张)')
        print('\n')
    elif keyWord == '-t':
        print('Here are some exemples: (rank by popularity, * is restricted content)')
        print('\n')
        print('这里是一些标签的例子(按热门度排行，标*的为限制级内容)')
        print('\n')
        print('women (People)')
        print('model (People)')
        print('nature (Nature)')
        print('brunette (People)')
        print('blonde (People)')
        print('landescape (Nature)')
        print('long hair (People)')
        print('anime (Anime&Manga)')
        print('anime girls (Anime&Manga)')
        print('ass (People)*')
        print('digital art (Art&Design)')
        print('women outdoors (People)')
        print('artwork (Art&Design)')
        print('trees (Nature)')
        print('looking at viewer (People)')
        print('boobs (People)*')
        print('video games (Entertainment)')
        print('leaves (Nature)')
        print('nude (People)*')
        print('portrait (Art&Design)')
        print('depth of field (Art&Design)\n')
    else:
        tf = 0


keyWord1 = keyWord
    
class Spider():
    def __init__(self):        
        self.headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
        }
        self.proxies = {
		"http": "http://61.178.238.122:63000",
	    }
        if (os.name == 'nt'):
            self.filePath = ('.\\'+ keyWord + "\\" ) # Here to change the location(Windows Edition)
        else:
            self.filePath = ('./'+ keyWord + "/" ) # Here to change the location(Mac Edition)
    def creat_File(self):
        filePath = self.filePath
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    def get_pageNum(self):
        total = ""
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc").format(keyWord1)
        html = requests.get(url,headers = self.headers,proxies = self.proxies)
        selector = etree.HTML(html.text)
        pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')
        string = str(pageInfo[0])
        numlist = list(filter(str.isdigit,string))
        for item in numlist:
            total += item
        totalPagenum = int(total)
        return totalPagenum

    def main_fuction(self):
        self.creat_File()
        count = self.get_pageNum()
        print("We have found:{} images!\n".format(count))
        time.sleep(1)
        times = input(f"{'How many pages do you wanna download? (24 pics per page) '}")
        print('\n')
        print('Cool! ', 24 * int(times), 'photos will be downloaded for you. Sit tight, have a cup of coffee. It will finish in no time.')
        print('\n')
        print('好哒！', 24 * int(times), '张照片将很快下载到您的电脑上。稍安勿躁，很快就能下完！')
        print('\n')
        j = 1
        times = int(times)
        start = time.time()
        widgets = ['Progress: ',Percentage(), ' ', Bar('>'),' ', Timer()]
        pbar = ProgressBar(widgets=widgets, maxval=100).start()
        cc = 0
        for i in range(times):
            pic_Urls = self.getLinks(i+1)
            threads = []
            for item in pic_Urls:
                t = Thread(target = self.download, args = [item,j])
                t.start()
                threads.append(t)
                j += 1
               
            for t in threads:
                cc += 100/(24 * times)
                if cc > 100:
                    cc = 100
                t.join() 
                pbar.update(cc)
        pbar.finish()
        end = time.time()

    def getLinks(self,number):
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc&page={}").format(keyWord1,number)
        try:
            html = requests.get(url,headers = self.headers,proxies = self.proxies)
            selector = etree.HTML(html.text)
            pic_Linklist = selector.xpath('//a[@class="jsAnchor thumb-tags-toggle tagged"]/@href')
        except Exception as e:
            print(repr(e))
        return pic_Linklist

    def download(self,url,count):
        string = url.strip('/thumbTags').strip('https://alpha.wallhaven.cc/wallpaper/')
        html = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string + '.jpg'
        pic_path = (self.filePath + keyWord + str(count) + '.jpg' )
        try:
            pic = requests.get(html,headers = self.headers)
            f = open(pic_path,'wb')
            f.write(pic.content)
            f.close()
        except Exception as e:
            print(repr(e))


spider = Spider()
spider.main_fuction()
print('This software will automatically exit in 5 seconds.\n')
print('本软件将于5秒后自动关闭。')
time.sleep(6)