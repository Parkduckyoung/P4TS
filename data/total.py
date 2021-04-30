import csv
import json

with open('./json/두산중공업.json',"r",encoding='utf-8') as f:
        price = json.load(f)
day = []
for row in price:
    day.append(row)

def check(category):
    category_list = ['전체','국제','정치','외교','청와대','기획·연재 ','경제','종합','정치','종목·투자전략']
    for row in category_list:
        if row in category: return 1
    return 0
categorys = []
temp = []


filename = '북한.csv'
f = open(filename,'r')
rd = csv.reader(f)
r = list(rd)
for row in r:
    if row[1] in day and int(row[2]) >900 and int(row[2]) <1430 : temp.append(row)



"""
for i in range(212):
    filename = './news/북한'+str(i)+'.csv'
    f = open(filename,'r')
    rd = csv.reader(f)
    r = list(rd)
    for row in r:
        row[2] = row[2].replace('\n','')
        row[3] = row[3].replace('\n','')
        if check(row[3]) == 1: temp.append(row)
        else:   
            if row[3] not in categorys: categorys.append(row[3])
"""        

f = open('북한_result.csv','w')
wr = csv.writer(f)

for i in range(len(temp)):
    wr.writerow(temp[i])
f.close()

#f = open('technical.csv','w')
#wr = csv.writer(f)


