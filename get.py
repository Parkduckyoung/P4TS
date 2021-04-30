
from bs4 import BeautifulSoup
import numpy as np
import time
import csv
import requests as rq
import os
from datetime import datetime

class crawling_price():
    def __init__(self,code_number,day):
        self.c_time =[]
        self.price = []
        self.sell = []
        self.buy = []
        self.volume = []
        self.variance = []
        url = 'https://finance.naver.com/item/sise_time.nhn?code='+code_number+'&thistime='+day
        for page in range(1, 50):
            price_url = url + "&page="+str(page)
            r = rq.get(price_url)  # 해당 url의 정보 요청
            time.sleep(0.1)
            soup = BeautifulSoup(r.content, 'lxml')
            r.close()
            table = soup.find_all('table', attrs={'class': 'type2'})
            if table is None:
                break
            for item in table:
                for col in item.find_all('tr'):
                    tds = col.find_all('td')
                    iden = col.find('span', attrs={'class': 'tah'})
                    if iden is not None:
                        self.c_time.append(tds[0].find('span').get_text().replace(':',''))  # 
                        self.price.append(tds[1].find('span').get_text().replace(',',''))  # 종가
                        self.sell.append(tds[3].find('span').get_text().replace(',',''))  # 시가
                        self.buy.append(tds[4].find('span').get_text().replace(',',''))  # 고가
                        self.volume.append(tds[5].find('span').get_text().replace(',',''))  # 저가
                        self.variance.append(tds[6].find('span').get_text())  
    def return_stock(self):
        self.c_time.reverse()
        self.price.reverse()
        self.sell.reverse()
        self.buy.reverse()
        self.volume.reverse()
        self.variance.reverse()
        return 0

    def get_data(self):
        self.return_stock()
        msg = "time: {:>3} - price: {:>3} - sell: {:>3}  - buy: {:>3} - volume: {:>3}- variance: {:>3}"
        return self.c_time,self.price,self.sell,self.buy,self.volume,self.variance

def north_korea_company(code,text,day):
    day_time = day+'1530'
    price = crawling_price(code,day_time)
    filename = '/home/user/stockprice/data/north_korea/'+day+'/'+text+'.csv'

    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['체결시각','체결가','매도','매수','거래량','변동량'])

    c_time,price,sell,buy,volume,variance = price.get_data()
    for i in range(len(c_time)):
        wr.writerow([c_time[i],price[i],sell[i],buy[i],volume[i],variance[i]])
    f.close()

def kospi_company(code,text,day):
    day_time = day+'1530'
    price = crawling_price(code,day_time)
    filename = '/home/user/stockprice/data/kospi/'+day+'/'+text+'.csv'

    f = open(filename,'w')
    wr = csv.writer(f)
    wr.writerow(['체결시각','체결가','매도','매수','거래량','변동량'])

    c_time,price,sell,buy,volume,variance = price.get_data()
    for i in range(len(c_time)):
        wr.writerow([c_time[i],price[i],sell[i],buy[i],volume[i],variance[i]])
    print(text)
    f.close()

#company_crawling("KPI200","KPI200") finance.naver.com/sise/sise_index.nhn
#company_crawling("c","현대시멘트")
#now = datetime.now()
#day = '%s%s%s' % (now.year, now.month, now.day)
#days = ['20200102','20200103','20200106','20191205','20191206','20191129','20191128','20191127']
day = '20200106'
print(day)
os.system('mkdir /home/user/stockprice/data/north_korea/'+day)
os.system('mkdir /home/user/stockprice/data/kospi/'+day)
code = ["011200","025980","017800","001550","001260","009270","026040","049630","005010","048470","025860",
        "010820","056080","000490","006260"]
text = ["현대상선","아난티","현대엘리베이","조비","남광토건","신원","제이에스티나","재영솔루텍","휴스틸","대동스틸","남해화학",
        "퍼스텍","유진로봇","대동공업","LS"]
for i in range(len(code)):
    north_korea_company(code[i],text[i],day)

code = ["039610","017480","071090","000910","004980","013580","065950","025950","002150","010120"]
text = ["화성밸브","삼현철강","하이스틸","유니온","성신양회","계룡건설","웰크론","동신건설","도화엔지니어","LS산전"]
for i in range(len(code)):
    north_korea_company(code[i],text[i],day)

code = ["011390","014790","026150","039980","028100","037370","071950","008250","004090"]
text = ["부산산업","한라","특수건설","리노스","동아지질","EG","코아스","이건산업","한국석유"]
for i in range(len(code)):
    north_korea_company(code[i],text[i],day)


code = ["005930","000660","035420","207940","005380","012330","068270","051910","055550",
        "005490","105560","051900","017670","028260","034730","015760","000270","006400"]
text = ["삼성전자","SK하이닉스","NAVER","삼성바이오로직스","현대차","현대모비스","셀트리온","LG화학","신한지주",
        "POSCO","KB금융","LG생활건강","SK텔레콤","삼성물산","SK","한국전력","기아차","삼성SDI"]
for i in range(len(code)):
    kospi_company(code[i],text[i],day)


