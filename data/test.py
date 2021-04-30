
from bs4 import BeautifulSoup
import numpy as np
import time
import json
import requests as rq
import talib

class crawling_price():
    def __init__(self,code_number,day,sday):
        self.day =[]
        self.close_price = []
        self.open_price = []
        self.low_price = []
        self.high_price = []
        self.volume = []

        url = 'https://finance.naver.com/item/sise_day.nhn?code=' + code_number
        for page in range(1, 500):
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
                    iden = col.find('td', attrs={'class': 'num'})
                    if iden is not None:
                        if self.identi(tds[0].find('span').get_text(), sday) == 1:
                            continue
                        if self.return_stock(tds[0].get_text(),day) == 1:
                            return
                        self.day.append(tds[0].find('span').get_text())  # 날짜
                        self.close_price.append(tds[1].find('span').get_text().replace(',',''))  # 종가
                        self.open_price.append(tds[3].find('span').get_text().replace(',',''))  # 시가
                        self.high_price.append(tds[4].find('span').get_text().replace(',',''))  # 고가
                        self.low_price.append(tds[5].find('span').get_text().replace(',',''))  # 저가
                        self.volume.append(tds[6].find('span').get_text().replace(',',''))  # 거래량

    def identi(self,now,sday):
        if now > sday:
            return 1
        return 0
    def return_stock(self,now,day):
        if day > now:
            self.day.reverse()
            self.close_price.reverse()
            self.open_price.reverse()
            self.low_price.reverse()
            self.high_price.reverse()
            self.volume.reverse()
            return 1
        return 0
    def get_data(self):
        self.index_value = 0
        msg = "day: {:>3} - close: {:>3} - open: {:>3}  - high: {:>3} - low: {:>3}- volume: {:>3}"
        for index in range(self.index_value,len(self.day)): 
            print(msg.format(self.day[index],self.close_price[index],self.open_price[index],self.high_price[index],self.low_price[index],self.volume[index]))
        return self.day[self.index_value:],self.open_price[self.index_value:],self.close_price[self.index_value:],self.high_price[self.index_value:],self.low_price[self.index_value:],self.volume[self.index_value:]

    def technical(self):
        rate = []
        #####################################
        for index in range(0,len(self.day)):
            if int(self.open_price[index]) == 0: rate.append(int(self.close_price[index])/int(self.close_price[index-1]) -1)
            else : rate.append(int(self.close_price[index])/int(self.open_price[index]) -1)
        
        return rate

def company_crawling(code,text):
    temp_dict = {}
    price = crawling_price(code,"2009.08.01","2019.12.31")
    day,open_price,close_price,high_price,low_price,volume = price.get_data()
    rate = price.technical()
    print(text)
    for a in range(len(day)):
        price_dict = {'day':day[a],'rate':rate[a],'open_price':int(open_price[a]),'close_price':int(close_price[a])
                                ,'high_price':int(high_price[a]),'low_price':int(low_price[a]),'volume':int(volume[a])}

        temp_dict[day[a]] = {'price':price_dict}
    json_file = './json/'+text+'.json'
    print(json_file)
    with open(json_file, 'w', encoding='utf-8') as file :
        json.dump(temp_dict, file, ensure_ascii=False, indent='\t')

#company_crawling("KPI200","KPI200") finance.naver.com/sise/sise_index.nhn
#company_crawling("006390","현대시멘트")


code = ["034020","011200","025980","017800","001550","001260","009270","026040","049630","005010","048470","025860",
        "010820","056080","000490","006260"]
text = ["두산중공업","현대해상","아난티","한일현대엘리베이","조비","남광토건","신원","인지컨트롤","재영솔루텍","휴스텍","대동스틸","남해화학",
        "퍼스텍","유진로봇","대동공업","LS"]
for i in range(len(code)):
    company_crawling(code[i],text[i])

code = ["039610","017480","071090","000910","004980","013580","065950","025950"]
text = ["화성밸브","삼현철강","하이스틸","유니온","성신양회","계룡건설","웰크론","동신건설"]
for i in range(len(code)):
    company_crawling(code[i],text[i])

code = ["011390","014790","026150","039980","028100","037370","071950","008250","004090","010120"]
text = ["부산산업","한라","특수건설","리노스","동아지질","EG","코아스","이건산업","한국석유","LS산전"]
for i in range(len(code)):
    company_crawling(code[i],text[i])
"""
company.append(["현대상선","현대엘리베이","아난티"],["남광토건","신원","인지컨트롤","제이에스티나","좋은사람들","재영솔루텍"])
company.append(["휴스틸","동양철관","삼현철강","화성밸브","대동스틸","하이스틸"],["조비","남해화학","효성오앤비"])
company.append(["퍼스텍","유진로봇","웰크론"],["한국제지","선창산업","대유에이텍","이건산업","한솔홈데코"],["대동공업","동양물산","LS"])
# 금강산(현대상선, 현대엘리베이, 아난티)
code.appned(["011200", "017800", "025980"])
# 개성공단(남광토건, 신원, 인지컨트롤, 제이에스티나, 좋은사람들, 재영솔루텍)
code.appned(["001260", "009270", "023800", "026040", "033340", "049630"])
# 가스관(휴스틸, 동양철관, 삼현철강, 화성밸브, 대동스틸, 하이스틸)
code.appned(["005010", "008970", "017480", "039610", "048470", "071090"])
# 비료(조비, 남해화학, 효성오앤비)
code.appned(["001550", "025860", "097870"])
# 지뢰제거(퍼스텍, 유진로봇, 웰크론)
code.appned(["010820", "056080", "065950"])
# 농기계
code.appned(["000490", "002900", "006260"])
"""

