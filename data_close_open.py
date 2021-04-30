from konlpy.tag import Mecab
import numpy as np
import gensim
import os
import json
import csv

mecab = Mecab()

class data_set():
    def __init__(self,Vector_size,company,s_day1,e_day1,s_day2,e_day2):
        self.Vector_size = Vector_size
        self.w2v = word_vector(Vector_size)
        self.company = company
        self.train_s_day = s_day1
        self.train_e_day = e_day1
        self.test_s_day = s_day2
        self.test_e_day = e_day2

    def call_data(self):
        f = open('./data/북한_result.csv','r')
        self.news_data = list(csv.reader(f))
        with open('./data/json/'+self.company+'.json',"r",encoding='utf-8') as f:
                self.price = json.load(f)
    
    def change(self,rate):
        technical = rate["technical"]
        result = [float(rate["previous_rate"])]
        result.extend(technical["tech"])
        
        return result

    def get_sentiment(self,rate):
        if float(rate) > 0 : return 1
        else: return 0

    def technical(self):
        train = []
        test = []
        for value in self.train_docs:
            train.append(value[1])
        for value in self.test_docs:
            test.append(value[1])
        return train, test
    def get_csv(self,s_day,e_day):
        docs = []
        sentiment = self.get_sentiment(self.price[e_day]["price"]["open_price"] - self.price[s_day]["price"]["close_price"]) #전일 종가 대비 당일 시가
        for row in self.news_data:
            temp_list = []
            if row[1] > e_day : break
            if row[1] < s_day: continue
            if row[1] == e_day and int(row[2]) > 830 : continue
            if row[1] == s_day and int(row[2]) < 1500 : continue

            temp_list = [self.w2v.tokenize(row[5])]
            temp_list.append(sentiment)

            if temp_list[0] == []: continue
            docs.append(temp_list)

        return docs
    def json_extract(self,s_day,e_day):
        day = []; docs = []
        for row in self.price:
            if row > e_day : break
            if row < s_day : continue
            docs.append(self.get_csv(row,row))
            day.append(row)

        for i in range(len(day)-2):
            temp_list = self.get_csv(day[i],day[i+1])
            
            docs.extend(temp_list)
        return docs

    def docs_data(self):
        self.call_data()
        self.train_docs= self.json_extract(self.train_s_day,self.train_e_day)
        self.test_docs = self.json_extract(self.test_s_day,self.test_e_day)

        with open('train_doc_time.json', 'w', encoding="utf-8") as make_file:
            json.dump(self.train_docs, make_file, ensure_ascii=False, indent="\t")
        with open('test_doc_time.json', 'w', encoding="utf-8") as make_file:
            json.dump(self.test_docs, make_file, ensure_ascii=False, indent="\t")

        return self.train_docs, self.test_docs
    
        """
    def get_csv2(self,s_day,e_day):
        docs = []; days = []
        news = ''
        for row in self.news_data:
            temp_list = []
            if row[1] > e_day : break
            if row[1] < s_day: continue
            if news == '': day = row[1]; news = row[4]
            if day != row[1]:
                temp_list.append(self.w2v.tokenize(news))
                temp_list.append(self.get_sentiment(self.price[day]["price"]["rate"]))
                days.append(day)
                news = row[4]; day = row[1]
                docs.append(temp_list)
            else : 
                if news != row[4] : news = news+' '+row[4]
        return docs,days
    """

class word_vector():
    
    def __init__(self,Vector_size):
        self.Vector_size = Vector_size

    def tokenize(self,doc):
        vector = []
        for t in mecab.pos(doc):
            if "V" in t[1] and "+" in t[1] or t[1] is "XR":
                vector.append(t[0])
            #if "NNB" not in t[1] and "J"not in t[1]:
            if "IC" not in t[1] :   #and "S"not in t[1]
                    #if "E" not in t[1] and "X"not in t[1]:
                vector.append(t[0])
        return vector


    def read_data(self, filename):
        with open(filename, 'r',encoding='utf-8') as f:
            data = [line.split('\t') for line in f.read().splitlines()]
            data = data[1:]
        return data  
    
    def Convert2Vec(self, model_name, doc):  ## Convert corpus into vectors
        word_vec = []
        y = []
        model = gensim.models.word2vec.Word2Vec.load(model_name)
        for sent in doc:
            sub = []

            for word in sent[0]:
                if(word in model.wv.vocab):
                    #arr = model.wv[word]
                    #sub.append(np.append(arr,sent[1]))
                    sub.append(model.wv[word])
                else:
                    #arr = np.append(np.random.uniform(-0.25,-0.25,300),sent[1])
                    #sub.append(arr) ## used for OOV words
                    sub.append(np.random.uniform(-0.25,0.25,self.Vector_size))
            word_vec.append(sub)
            y.append(float(sent[1]))

        x = np.array(word_vec)
        y = np.array(y).astype('float32')
        return x,y
    
    def Zero_padding(self, batch_X, Maxseq_length):
        zero_pad = np.zeros((len(batch_X), Maxseq_length, self.Vector_size))
        for i in range(len(batch_X)):
            zero_pad[i,:np.shape(batch_X[i])[0],:np.shape(batch_X[i])[1]] = batch_X[i]
        return zero_pad
