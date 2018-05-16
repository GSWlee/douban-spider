import urllib.request
import urllib.error
import requests
import re
import random
from bs4 import BeautifulSoup
import codecs

class Douban_Spider():
    def __init__(self):
        self.url="https://movie.douban.com/subject/"
        
    def getheaders(self):
        user_agent_list = [ 
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" ,
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", 
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", 
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", 
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", 
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", 
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", 
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", 
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", 
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        UserAgent=random.choice(user_agent_list)
        headers = {'User-Agent': UserAgent}
        return headers

    def get_page(self,url):
        try:
            headers=self.getheaders()
            requests=urllib.request.Request(url=url,headers=headers)
            html=urllib.request.urlopen(requests)
        except urllib.error.HTTPError as e:
            print(e.code)
            html=None
        return html

    def get_info(self,html,mid,mids,finsh_mids):
        if html!=None:
            soup=BeautifulSoup(html,'html.parser')
            name=soup.find("span", {"property":"v:itemreviewed"}).get_text()   # 片名
            end=name.find(" ")
            if end==-1:
                cn_name=name
                real_name=name
            else:
                cn_name=name[0:end]
                real_name=name[end+1:]
            print("正在爬取",real_name,"\n...")
            try:
                release_time=soup.find("span",{"class":"year"}).get_text()         # 上映时间
                release_time=release_time[1:-1]
                score=soup.find("strong",{"class":"ll rating_num"}).get_text()     # 评分
                pic_url=soup.find("div",{"id":"mainpic"}).find("img")["src"]       # 海报url
                
                info=soup.find("div",{"id":"info"})
                temp=info.findAll("a",{"rel":"v:directedBy"})                      # 导演
                directors=list()
                for item in temp:
                    directors.append(item.get_text())

                temp=info.findAll("span",{"property":"v:genre"})                   # 类型
                movie_type=[]
                for item in temp:
                    movie_type.append(item.get_text())
                actors=[]                                                          # 演员
                temp=info.find("span",{"class":"actor"})
                q=temp.findAll("a",{"rel":"v:starring"})
                for item in q:
                    actors.append(item.get_text())
                sheet_length=info.find("span",{"property":"v:runtime"})["content"] # 片长
                tar_nation=r'<span class="pl">制片国家/地区:</span> (.*?)<br/>'
                tar_language=r'<span class="pl">语言:</span> (.*?)<br/>'
                tar_another_name=r'<span class="pl">又名:</span>(.*?)<br/>'
                nation =re.findall(tar_nation,str(info),re.S|re.M)                 # 国家
                nations="".join(nation)
                language=re.findall(tar_language,str(info),re.S|re.M)              # 语言
                languages="".join(language)
                another_name=re.findall(tar_another_name,str(info),re.S|re.M)      # 别名

                brief=soup.find("span",{"property":"v:summary"}).get_text()        # 简介
                tar=r'<a href="https://movie.douban.com/subject/([0-9]+?)/'
                info=soup.find("div",{"class":"recommendations-bd"})
                item=info.findAll("a")
                for i in item:
                    temp_num=re.findall(tar,str(i),re.S|re.M)
                    if len(temp_num)!=0 :
                        string="".join(temp_num)
                        if mids.count(string)==0 and finsh_mids.count(string)==0:
                            mids.append(string)
                return mid,cn_name,real_name,release_time,score,pic_url,directors,movie_type,actors,sheet_length,nations,languages,another_name,brief
            except Exception:
                print("获取出错\n")
                return 1
        return tuple()

    def begin(self,mid,mids,finsh_mids):
        temp_url=self.url+mid
        html=self.get_page(temp_url)
        temp_info=self.get_info(html,mid,mids,finsh_mids)
        return temp_info
