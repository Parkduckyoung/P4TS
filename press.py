from bs4 import BeautifulSoup
import numpy as np
import time
import pandas as pd
import requests as rq

class press_crawling():
    def __init__(self):
        return

    def check(self,attr):
        if attr is None: return ''
        else: return attr.get_text()

    def chosun(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')
    
        category = soup.find('meta', attrs={'property':'article:section'}).get('content')
        table = soup.find('div', attrs={'class': 'par'}).get_text()

        date = soup.find('div',attrs={'class':'news_date'})
        if date is None : return '0','0','0','0'
        else: date = date.get_text()
        day = date[3:13].replace('-','.')
        day_time = date[14:19].replace(':','')

        return table,category,day,day_time

    def han(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')

        if soup.find('meta', attrs={'property':'article:section'}) is None :  return '0','0','0','0'
        category = soup.find('meta', attrs={'property':'article:section'}).get('content')

        if soup.find('div', attrs={'class': 'text'}) is None :  return '0','0','0','0'
        table = soup.find('div', attrs={'class': 'text'}).get_text().replace('\xa0','').replace('\r','').replace('\n','')
        date = soup.find('p',attrs={'class':'date-time'}).get_text()

        day = date[4:14].replace('-','.')
        day_time = date[15:20].replace(':','')

        return table,category,day,day_time

    def joong(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')
      
        category = soup.find('meta', attrs={'property':'article:section'}).get('content')

        table = soup.find('div', attrs={'class': 'article_body'}).get_text()
        date = soup.find('div',attrs={'class':'byline'}).get_text()


        dele1 = self.check(soup.find('div', attrs={'class': 'ab_subtitle'}))
        dele2 = self.check(soup.find('div', attrs={'class': 'article_body'}).find('b'))
        dele3 = self.check(soup.find('div', attrs={'class': 'ab_photo'}))
        dele4 = self.check(soup.find('p', attrs={'class': 'caption'}))

        content = table.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')
        content = content.replace(dele1,'').replace(dele2,'').replace(dele3,'').replace(dele4,'')

        day = date[12:22].replace('-','.')
        day_time = date[23:28].replace(':','')

        return content,category,day,day_time

    def kook(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')
        
        if soup.find('div', attrs={'class': 'tx'}) is None: return '0','0','0','0'
        table = soup.find('div', attrs={'class': 'tx'}).get_text()
        date = soup.find('span',attrs={'class':'t11'}).get_text()


        dele1 = self.check(soup.find('div', attrs={'align': 'center'}))
        content = table.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')
        content = content.replace(dele1,'')
        day = date[0:10].replace('-','.')
        day_time = date[11:21].replace(':','')

        return content,'전체',day,day_time

        
    def dong(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')
       
        category = soup.find('div', attrs={'class':'location'})
        
        if category is None : return '0','0','0','0'
        else: category = category.get_text()

        contents = soup.find('div', attrs={'class': 'article_txt'})


        
        date = soup.find('span',attrs={'class':'date01'})
        if date is None : category = '전체'
        else: date = date.get_text()

        content = contents.get_text()
        dele1 = self.check(soup.find('div', attrs={'class': 'articlePhotoC'}))
        dele2 = self.check(soup.find('div', attrs={'class': 'btn_Journalist'}))
        dele3 = self.check(soup.find('div', attrs={'class': 'article_issue'}))
        dele4 = self.check(soup.find('ul', attrs={'class': 'relation_list'}))
        dele5 = self.check(soup.find('div', attrs={'class': 'bestnews_box'}))

        for row in contents.find_all('script'):
            content = content.replace(row.get_text(),'')

        content = content.replace(dele1,'').replace(dele2,'').replace(dele3,'')
        content = content.replace(dele4,'').replace(dele5,'')
        content = content.replace('\xa0','').replace('\r','').replace('\n','')
        content = content.replace('  ','').replace('창닫기','')

        day = date[3:13].replace('-','.')
        day_time = date[14:19].replace(':','')

        return content,category,day,day_time

    def seoul(self,url):
        company_info = rq.get(url,timeout=1)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')

        category = '전체'

        contents = soup.find('div', attrs={'class': 'v_article'})


        content = contents.get_text()
        for row in contents.find_all('script'):
            content = content.replace(row.get_text(),'')
        content = content.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')
        date = soup.find('p',attrs={'class':'v_days'}).find('span').get_text()


        day = date[0:10].replace('-','.')
        day_time = date[11:19].replace(':','')

        return content,category,day,day_time

    def yna(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')

        category = soup.find('meta', attrs={'property':'article:section'}).get('content')

        contents = soup.find('div', attrs={'class': 'article'})
        dele1 = self.check(contents.find('span', attrs={'class': 'cprgt'}))
        dele2 = self.check(contents.find('span', attrs={'class': 'pblsh'}))


        content = contents.get_text().replace(dele1,'').replace(dele2,'')
        date = soup.find('span',attrs={'class':'tt'}).get_text()
        content = content.replace('\xa0','').replace('\r','').replace('\n','')


        day = date[7:17].replace('-','.')
        day_time = date[18:23].replace(':','')

        return content,category,day,day_time

    def mt(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')

        category = '전체'

        contents = soup.find('div', attrs={'class': 'view_text'})
        if contents is None: return '0','0','0','0'
        content = contents.get_text()
        date = soup.find('li',attrs={'class':'date'}).get_text()


        dele1 = self.check(soup.find('div', attrs={'class': 'copyright'}))
        dele2 = self.check(soup.find('ul', attrs={'class': 'agree_type'}))
        dele3 = self.check(soup.find('ul', attrs={'class': 'profile_list'}))
        dele4 = self.check(soup.find('p', attrs={'class': 'txt'}))
        dele5 = self.check(contents.find('script'))

        content = content.replace(dele1,'').replace(dele2,'').replace(dele3,'')
        content = content.replace(dele4,'').replace(dele5,'')

        content = content.replace('\xa0','').replace('\r','').replace('\n','')

        day = date[0:10].replace('-','.')
        day_time = date[11:23].replace(':','')

        return content,category,day,day_time

    def mk(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')
       
        if soup.find('span',attrs={'class':'ft_org'}) is None or soup.find('h1') is None: return '0','0','0','0'

        category = soup.find('span',attrs={'class':'ft_org'}).get_text()

        contents = soup.find('div', attrs={'class': 'art_txt'})

        content = contents.get_text()
        date = soup.find('li',attrs={'class':'lasttime'}).get_text()

        for row in contents.find_all('script'):
            content = content.replace(row.get_text(),'')

        content = content.replace('\xa0','').replace('\r','').replace('\n','')

        day = date[5:15].replace('-','.')
        day_time = date[16:22].replace(':','')

        return content,category,day,day_time

    def fnnews(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')
        
        if soup.find('h1') is None or soup.find('h2', attrs={'class':'mg'}) is None :
            return '0','0','0','0'

        category = soup.find('h2', attrs={'class':'mg'}).get_text()

        contents = soup.find('div', attrs={'class': 'article_cont'})

        content = contents.get_text()
        date = soup.find('div',attrs={'class':'byline'}).get_text()


        dele1 = self.check(contents.find('div', attrs={'class': 'security'}))
        dele2 = self.check(contents.find('span'))
        content = content.replace(dele1,'').replace(dele2,'')

        content = content.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')

        day = date[14:25].replace('-','.')
        day_time = date[25:31].replace(':','')

        return content,category,day,day_time

    def sedaily(self,url):
        company_info = rq.get(url,timeout=10)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')
        if soup.find('div', attrs={'class':'sub_view'}) is None :
            return '0','0','0','0'
        view_top = soup.find('div', attrs={'class':'sub_view'})
        category = view_top.find('li', attrs={'class':'last'}).get_text()
        contents = view_top.find('div', attrs={'class': 'view_con'})

        content = contents.get_text()
        for row in contents.find_all('script'):
            content = content.replace(row.get_text(),'')

        date = view_top.find('li',attrs={'class':'letter'}).get_text()
        content = content.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')

        day = date[0:10].replace('-','.')
        day_time = date[11:16].replace(':','')

        return content,category,day,day_time

    def naver(self,url):

        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')

        if soup.find('h3', attrs={'id':'articleTitle'}) is None:
            return '0','0','0','0'
        category = '전체'

        contents = soup.find('div', attrs={'class': '_article_body_contents'})

        content = contents.get_text()
        for row in contents.find_all('script'):
            content = content.replace(row.get_text(),'')


        date = soup.find('span',attrs={'class':'t11'}).get_text()

        content = content.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')

        content = contents.get_text()
        for row in contents.find_all('script'):
            content = content.replace(row.get_text(),'')

        day = date[0:10].replace('-','.')
        
        
        content = content.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')

        if date[12:14] == '오후':
            a = int(date[15])+12
            day_time = str(a)+date[17:19]
        else: day_time = str(0)+date[15:19]
        day_time = day_time.replace(':','')

        return content,category,day,day_time

    def edaily(self,url):
        company_info = rq.get(url)
        time.sleep(1)
        soup = BeautifulSoup(company_info.content,'lxml')

        if soup.find('div', attrs={'class':'dates'}) is None:
            return '0','0','0','0'

        view_top = soup.find('div', attrs={'class':'news_titles'})
        category = '전체'

        contents = soup.find('div', attrs={'class': 'news_body'})

        content = contents.get_text()
        for row in contents.find_all('script'):
            content = content.replace(row.get_text(),'')

        date = view_top.find('div',attrs={'class':'dates'}).get_text()

        content = content.replace('\xa0','').replace('\r','').replace('\n','').replace('  ','')

        if date[17:19] == '오후':
            a = int(date[20])+12
            day_time = str(a)+date[22:24]
        else: day_time = str(0)+date[20:24]
        day = date[6:16].replace('-','.')
        day_time = day_time.replace(':','')

        return content,category,day,day_time

