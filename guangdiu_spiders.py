from bs4 import BeautifulSoup
import requests
import time
import re

import smtplib
import email.mime.multipart
import email.mime.text




class guangdiu_spiders():
    """优惠商品订阅系统"""
    uesd_url=[]

    def __init__(self):
        self.keywords=["神价格","手慢无","BUG","战术"]  #订阅的关键字,如须更多关键字,可继续添加列表.
        self.email="117971371@qq.com"   #订阅者邮箱


        self.mian()

    def get_html(self,url):
        #请求网页的通用模板
        try:
            r=requests.get(url,timeout=3)
            r.raise_for_status()
        except requests.Timeout as e:
            print("连接服务器超时,3秒后自动重试.")
            time.sleep(3)
        except requests.HTTPError as e:
            print("连接服务器出错,3秒后自动重试.")
            time.sleep(3)
        except Exception as e:
            print("未知错误:",e)
            time.sleep(3)
        else:
            r.encoding=r.apparent_encoding
            return r

    def spiders(self):
        #网页爬取
        r = self.get_html("http://guangdiu.com/index.php?c=all")
        if r:
            soup = BeautifulSoup(r.text,"xml")
        else:
            return
        gooditems = soup.find_all("div",class_="gooditem withborder ")
        for item in gooditems:
            for i in self.keywords:
                url="http://www.guangdiu.com/" +item.find("a",class_="goodname").get("href")
                if len(re.findall(i,str(item),re.IGNORECASE))>0 and url not in self.uesd_url:
                    return item
        return None

    def parser(self,item):
        #网页数据解析
        items={}
        items["title"] = item.find("a",class_="goodname").get("title")
        items["url"] = "http://www.guangdiu.com/"+item.find("a", class_="goodname").get("href")
        items["into"] = item.find("a", class_="innergototobuybtn").get("href")
        if items["into"].startswith("go.php?id="):
            items["into"] = "http://www.guangdiu.com/" + items["into"]
        items["content"] = item.find("a",class_="abstractcontent").text
        items["img"] = item.find("img").get("src")
        print("获取到新内容:",items)
        return items


    def send_email(self,items):
        #email 发送模块
        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = '18638163010@163.com'
        msg['to'] = self.email
        msg['subject'] = items["title"]
        content = '''''<p style="white-space: normal;">
            <span style="font-size: 18px;">%s</span>
        </p>
        <p>
            <img src="%s"/>
        </p>
        <p>
            产品描述:%s
        </p>
        <p>
            更多详情:%s
        </p>
        <p>
            产品链接:%s
        </p>'''%(items["title"],items["img"],items["content"],items["url"],items["into"])
        txt = email.mime.text.MIMEText(content,'html')
        msg.attach(txt)

        smtp = smtplib
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com', '25')
        smtp.login('18638163010@163.com', 'qq117971371')          #-0- 请不要修改密码!!
        smtp.sendmail('18638163010@163.com', self.email, str(msg))
        smtp.quit()
        return True

    def mian(self):
        #调度端
        while True:
            if time.strftime("%H:%M", time.localtime()) < "07:00":
                print("大家都睡了,程序也要休息了!")
                time.sleep(7*60*60)      #凌晨不运行
            try:
                item=self.spiders()
                if item:
                    items=self.parser(item)
                    if items:
                        if self.send_email(items):
                            self.uesd_url.append(items["url"])
                time.sleep(30)
            except Exception as e:
                print("主程序出错:",e,"/n10秒后进行重试.")
                time.sleep(10)


if __name__ == '__main__':
    spider=guangdiu_spiders()

