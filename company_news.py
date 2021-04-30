from bs4 import BeautifulSoup
import requests as rq
from time import sleep
import re
import csv
from urllib.parse import quote
import press as pr

def get_data(url,press_company):
    crawling_content = pr.press_crawling()
    if 'news.naver.com' in url : content,category,day,day_time = crawling_content.naver(url)
    elif press_company == '국민일보': content,category,day,day_time = crawling_content.kook(url)
    elif press_company == '연합뉴스': content,category,day,day_time = crawling_content.yna(url)
    elif press_company == '한겨레': content,category,day,day_time = crawling_content.han(url)
    elif press_company == '동아일보': content,category,day,day_time = crawling_content.dong(url)
    elif press_company == '조선일보': content,category,day,day_time = crawling_content.chosun(url)
    elif press_company == '중앙일보': content,category,day,day_time = crawling_content.joong(url)
    elif press_company == '파이낸셜뉴스': content,category,day,day_time = crawling_content.fnnews(url)
    elif press_company == '머니투데이': content,category,day,day_time = crawling_content.mt(url)
    elif press_company == '매일경제': content,category,day,day_time = crawling_content.mk(url)
    #elif press_company == '서울신문': content,category,day,day_time = crawling_content.seoul(url)
    elif press_company == '서울경제': content,category,day,day_time = crawling_content.sedaily(url)
    elif press_company == '이데일리': content,category,day,day_time = crawling_content.edaily(url)
    else : return '0','0','0','0' 
    return day,day_time,category,content

def naver_news(sdate,edate,query):
    print(query)
    URL_BEFORE_KEY = "https://search.naver.com/search.naver?where=news&query="
    URL_BEFORE_SDATE = "&sm=tab_srt&sort=1&photo=3&field=0&reporter_article=&pd=3&ds="
    URL_BEFORE_EDATE = "&de="
    URL_BEFORE_PAGE = "&start="
    news = []
    for i in range(0, 2500000):
        page = (10*i)+1
        url = URL_BEFORE_KEY + quote(query) + URL_BEFORE_SDATE + sdate + URL_BEFORE_EDATE + edate + URL_BEFORE_PAGE + str(page)     
        print(url)
        r = rq.get(url) #해당 url의 정보 요청

        sleep(1)
        soup = BeautifulSoup(r.content,'lxml')
        
        news_list = soup.find('ul',attrs={'class':'type01'})
        if news_list is None:
            break
        if i == 0: index = soup.find('div',attrs={'class':'title_desc'}).find('span').get_text()[7:20].replace('건','').replace(',','')
        print(index)
        if page > int(index) : break
        for company,url in zip(news_list.select('dd.txt_inline > span._sp_each_source'),news_list.select('dl > dt > a._sp_each_title')):
            address = url.get('href')
            title = url.get_text()
            if '기업공시' in title : continue
            press_company = ''.join(company(text=True)).replace('언론사 선정','')
            print(address)
            print(press_company)
            day,day_time,category,content = get_data(address,press_company)
            category = category.replace('\n','')
            day_time = day_time.replace('\n','')
            print(day)
            if day == '0':continue
            news.append([query,day,day_time,category,title,content])
    return news   

news = naver_news( '2010.01.01', '2019.12.31', '대북주')
filename = '/home/user/stockprice/data/news/대북주.csv'
f = open(filename,'w')
wr = csv.writer(f)
wr.writerow(['키워드','날짜','시간','카테고리','제목','본문'])
for row in news:
    wr.writerow(row)
sleep(100)


"""
text1 = ["2010.11.15","2010.11.01","2010.10.15","2010.10.01","2010.09.15","2010.09.01","2010.08.15","2010.08.01","2010.07.15","2010.07.01"]
text2 = ["2010.11.30","2010.11.14","2010.10.31","2010.10.14","2010.09.30","2010.09.14","2010.08.31","2010.08.14","2010.07.31","2010.07.14"]
#text1 = ["2010.08.01","2010.07.15","2010.07.01"]
#text2 = ["2010.08.14","2010.07.31","2010.07.14"]

for index in range(len(text1)):
   
    news = naver_news( text1[index], text2[index], '북한')
    filename = '/home/user/stockprice/data/지면기사/북한'+str(index+200)+'.csv'
    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['회사','날짜','시간','카테고리','제목','본문'])
    for row in news:
        wr.writerow(row)
    sleep(100)


text1 = ["2010.06.15","2010.06.01","2010.05.15","2010.05.01","2010.04.15","2010.04.01","2010.03.15","2010.03.01","2010.02.15","2010.02.01","2010.01.15","2010.01.01"]
text2 = ["2010.06.30","2010.06.14","2010.05.31","2010.05.14","2010.04.30","2010.04.14","2010.03.31","2010.03.14","2010.02.29","2010.02.14","2010.01.31","2010.01.14"]
#text1 = ["2010.04.01","2010.03.15","2010.03.01","2010.02.15","2010.02.01","2010.01.15","2010.01.01"]
#text2 = ["2010.04.14","2010.03.31","2010.03.14","2010.02.29","2010.02.14","2010.01.31","2010.01.14"]

for index in range(len(text1)):
   
    news = naver_news( text1[index], text2[index], '북한')
    filename = '/home/user/stockprice/data/포토/북한'+str(index+12)+'.csv'
    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['회사','날짜','시간','카테고리','제목','본문'])
    for row in news:
        wr.writerow(row)
    sleep(100)

#"현대엘리베이","조비","남광토건","제이에스티나","재영솔루텍","휴스틸","대동스틸","남해화학","퍼스텍","유진로봇",
text = ["LS","현대상선"]
for query in text:
    news = naver_news('2010.01.01', '2010.12.31', query)
    filename = '/home/user/stockprice/data/'+query+'.csv'
    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['회사','날짜','시간','카테고리','제목','본문'])
    for row in news:
        wr.writerow(row)
    sleep(100)

text = ["화성밸브","삼현철강","하이스틸","유니온","성신양회","계룡건설","웰크론","동신건설","도화엔지니어","LS산전"]
for query in text:
    news = naver_news('2010.01.01', '2010.12.19', query)
    filename = '/home/user/stockprice/data/'+query+'.csv'
    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['회사','날짜','시간','카테고리','제목','본문'])
    for row in news:
        wr.writerow(row)
    sleep(100)

text = ["부산산업","한라","특수건설","리노스","동아지질","EG","코아스","이건산업","한국석유"]
for query in text:
    news = naver_news('2010.01.01', '2010.12.19', query)
    filename = '/home/user/stockprice/data/'+query+'.csv'
    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['회사','날짜','시간','카테고리','제목','본문'])
    for row in news:
        wr.writerow(row)
    sleep(100)

text = ["삼성전자","SK하이닉스","NAVER","삼성바이오로직스","현대차","현대모비스","셀트리온","LG화학","신한지주",
        "POSCO","KB금융","LG생활건강","SK텔레콤","삼성물산","SK","한국전력","기아차","삼성SDI"]
for query in text:
    news = naver_news('2010.01.01', '2010.12.19', query)
    filename = '/home/user/stockprice/data/'+query+'.csv'
    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['회사','날짜','시간','카테고리','제목','본문'])
    for row in news:
        wr.writerow(row)
    sleep(100)
"""
