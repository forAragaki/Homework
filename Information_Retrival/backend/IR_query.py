import pandas as pd
import nltk
from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *
import re, string, json

# Split session
# data = pd.read_csv('Info/Info.csv',chunksize=1000000)
# small = None
# ct = 0
# for dt in data:
#     small = dt
#     ct+=1
#     print(f'This is {ct} chunk')
#     break
# small['second']= small.time.map(str_time)
# small['diff'] = small.second.diff()
# small.loc[0,'diff'] = 0
# session = []
# ct = 0
# for i in small['diff'].values:
#     session.append(ct)
#     if i>30:
#         ct+=1
# small['session'] = session


def str_time(s):
    if s=="" or s==None:
        return 0
    ss = s.split(":")
    time = int(ss[0])*60+int(ss[1])
    return time
def get_dict(tempdf):
    dic = {}
    text = tempdf['text'].values
    # here do something normalize
    for text_ind, tx in enumerate(text):
        if str(tx)=='nan':
            continue
        temp = handletext(tx)
        for k,item in enumerate(temp):
            if item=="":
                continue
            if item not in dic:
                dic[item] = {}
            if text_ind not in dic[item]:
                dic[item][text_ind] = []
            dic[item][text_ind].append(k)
    return dic

def get_user_dict(tempdf):
    dic = { 'speaker': tempdf['speaker'].unique(),'receiver':tempdf['receiver'].unique() }
    speaker = tempdf['speaker'].unique()
    receiver = tempdf['receiver'].unique()
    return dic
characters = ['..',' ',',', '.','DBSCAN', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','-','...','^','{','}']

# 去掉URL
def _replace_urls(text):
    url_regex = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    text = re.sub(url_regex, "<URL>", text)
    return text


def delete_characters(token_words):
    '''
        去除特殊字符、数字
    '''
    words_list = [word for word in token_words if word not in characters and not is_number(word)]
    return words_list

def to_lower(token_words):
    '''
        统一为小写
    '''
    words_lists = [x.lower() for x in token_words]
    return words_lists
    
def handletext(text):
    p_stemmer = PorterStemmer()
    # def nltk_process(text):
        #Tokenization
        
    
    nltk_tokenList = word_tokenize(text)
    # 去掉url
    url_token = []
    for word in nltk_tokenList:
        word = _replace_urls(word)
        # 去掉数字
        word = re.sub(r'(([.,\-,*]*)[0-9]+)+([.,\-,*]*)[0-9]*', '',word)
#         if word!="":
        url_token.append(word)
    
    # 去掉分隔符
    # "-,=,/"
    rmlist = []
    for k, word in enumerate(url_token):
        if len(word)>15:
            rmlist.append("")
        else:
            tempword = re.split(r"\.|\-|\/|\=|\\|\*|\+",word)
            for tp in tempword:
                rmlist.append(tp)

    # Stemming
    nltk_stemedList = []
    for word in rmlist:
        nltk_stemedList.append(p_stemmer.stem(word))
    #Lemmatization
    # wordnet_lemmatizer = WordNetLemmatizer()
    # nltk_lemmaList = []
    # for word in nltk_tokenList:
    #     nltk_lemmaList.append(wordnet_lemmatizer.lemmatize(word))
#     print("Lemmatization")
#     print(nltk_lemmaList)
    #Filter stopword
    filtered_sentence = []
    nltk_stop_words = set(stopwords.words("english"))
    for w in nltk_stemedList:  
        if w not in nltk_stop_words:  
            filtered_sentence.append(w)
        else:
            filtered_sentence.append("")
    #Removing Punctuation
    punctuations="?:!.,;*):"
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)
    
    # 去掉* _ 
    
    mv = ['*','_','^','~',')','(','..','...']
    filtered_sentence = delete_characters(filtered_sentence)
    filtered_sentence = to_lower(filtered_sentence)
    for k,word in enumerate(filtered_sentence):
        for sss in mv:
            if sss in word:
                word_temp = word.replace(sss,'')
                filtered_sentence[k] = word_temp
    return filtered_sentence
	

	
import os
def create_html():
    for fs in os.listdir('IRC/'):
        path = 'IRC/' + fs
        tempd = pd.read_csv(path)
        tex = '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>text</title>
</head>
<body>
<table>
    <tbody>
    <tr>
        <th>Speaker</th>
        <th>Receiver</th>
        <td>Text</td>
    </tr>
'''
        end = '''
    </tbody>
</table>
</body>
</html>
        '''
        add= ""
        for i in range(tempd.shape[0]):
            text = tempd.loc[i,'text']
            spe = tempd.loc[i,'speaker']
            rec = tempd.loc[i,'receiver']
            add += f'<tr><th>{spe}</th><th>{rec}</th><td>{text}</td></tr>'
        fntext = tex + add + end
        with open(f'E:WebstormProjects/IR/logs/{fs[:-4]}.html','w',encoding='utf8') as fff:
            fff.write(fntext)
# create_html()

# session is docID
# 将session保存在文件中
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm_notebook
finalpositon_list = {}

small = None

ALL_ID = 0
cx = 0

final__reciver_user_table = {}
final_sender_user_table = {}

data = pd.read_csv('Info/Info.csv',chunksize=1000000)
for dt in data:
    small = dt
    cx+=1
    print(f'This is {cx} chunk')
    small['second']= small.time.map(str_time)
    small['diff'] = small.second.diff()
    small.loc[0,'diff'] = 0
    session = []
    ct = 0
    for i in small['diff'].values:
        session.append(ct)
        if i>30:
            ct+=1
    small['session'] = session
    
    for ids in tqdm_notebook(small.session.unique()):
        tempp = small[small.session==ids]
        tempp.to_csv(f'IRC/{ALL_ID}.csv',index=False)
        
        position_list = get_dict(tempp)
        for wo in position_list:
            if wo not in finalpositon_list:
                finalpositon_list[wo] = {}
            finalpositon_list[wo][ALL_ID] = position_list[wo]
        
        user_dic = get_user_dict(tempp)
        for us in user_dic['speaker']:
            us = str(us).lower()
            if us not in final_sender_user_table:
                final_sender_user_table[us] = []
            final_sender_user_table[us].append(ALL_ID) 
        for us in user_dic['receiver']:
            us = str(us).lower()
            if us not in final__reciver_user_table:
                final__reciver_user_table[us] = []
            final__reciver_user_table[us].append(ALL_ID)
        ALL_ID += 1
            #         if ids>100:
#             break
    break
# 对于每个session

# 返回docID列表

# "root or account or a"

def handle_or(input_str):
    input_str = input_str.lower()
    inp = input_str.split(" or ")
    docid = []
    getsent = inp[0].strip()
    for item in inp:
        item = item.strip()
        if item not in finalpositon_list:
#             fuzz(item)
            return []
        else:
            docid.append(item)
    
    final = list(finalpositon_list[docid[0]].keys())
    for item in docid[1:]:
        start = final
        end = list(finalpositon_list[item].keys())
        final = list(set(start).union(set(end)))
    fndic = {}
    for fn in final:
        for item in inp:
            item = item.strip()
            tt = finalpositon_list[getsent]
            if fn in tt:
                fndic[fn] = list(finalpositon_list[getsent][fn].keys())
                break
    return fndic

# "root and account"
def handle_and(input_str):
    input_str = input_str.lower()
    inp = input_str.split("and")
    docid = {}
    
    getsent = inp[0].strip()
    for item in inp:
        item = item.strip()
        if item not in finalpositon_list:
#             fuzz(item)
            return []
        else:
            docid[item] = len(finalpositon_list[item])
            
    # 按照长度排序
    order = sorted(docid.items(), key=lambda item:item[1])
    
    final = list(finalpositon_list[order[0][0]].keys())
#     print(order)
#     end = finalpositon_list[order[1][0]]
#     final = []
    for item in order[1:]:
        start = final.copy()
        final = []
        end = list(finalpositon_list[item[0]].keys())
#         print(start,end)
        p = 0
        q = 0
        while p<len(start) and q<len(end):
            if start[p]<end[q]:
                p+=1
            elif start[p]>end[q]:
                q+=1
            else:
                final.append(start[p])
                p+=1
                q+=1
    
    re = {}
    for s in final:
        re[s] = list(finalpositon_list[getsent][s].keys())
    return re

def handle_not(input_str):
    input_str = input_str.lower()
    inp = input_str.split("not")
    docid = []
    
    getsent = inp[0].strip()
    
    for item in inp:
        item = item.strip()
        if item not in finalpositon_list:
#             fuzz(item)
            return []
        else:
            docid.append(item)
    
    final = list(finalpositon_list[docid[0]].keys())
    
    for item in docid[1:]:
        start = final
        end = list(finalpositon_list[item].keys())
        final = list(set(start).difference(set(end)))
    
    fndic = {}
    for fn in final:
        fndic[fn] = list(finalpositon_list[getsent][fn].keys())
    return fndic
#     return final

# "root account" 一个句子内
# 单词 - session - 句子
def handle_phrase(input_str):
    input_str = input_str.lower()
    pts = input_str.split(" ")
    if 'and' in pts or 'or'in pts or 'not' in pts:
        return "inputs error"

# /s 3
def handle_sentence(input_str):
    input_str = input_str.lower()
    inp = input_str.split("/s")
    reinput = "and".join(inp[:-1])
    num = int(inp[-1])
    inp = inp[:-1]
    print(inp)
    
    inp = [x.strip() for x in inp]
    
    docid = handle_and(reinput)
    
    if len(docid)==0:
        return []
    
    ks = list(docid.keys())
    sens = {}
    # 所有item共有的句子
    for item in docid:
        final = list(finalpositon_list[inp[0]][item].keys())
#         final = list(fnb.keys())
        for it in inp[1:]:
            start = final
            end = list(finalpositon_list[it][item].keys())
            final = list(set(start).intersection(set(end)))
        if len(final)!=0:
            sens[item] = final
    
#     print(sens)
    # sens: session:[句子]
    fnsens = {}
    for fn in sens:
        
#         final_senid = list(finalpositon_list[inp[0]][fn].keys())
        # 某个session的句子列表
        final_senid = sens[fn]
    
    
        # 该单词某个session
        st = finalpositon_list[inp[0]][fn]
        
        
        for it in inp[1:]:
            en = finalpositon_list[it][fn]
            fnss = []
            for sen_id in final_senid:
                std = st[sen_id]
                end = en[sen_id]
                p = 0
                q = 0
                while p<len(std) and q<len(end):
                    if std[p]+num<end[q]:
                        p+=1
                    elif std[p]>end[q]+num:
                        q+=1
                    else:
                        fnss.append(sen_id)
                    break
            final_senid = fnss
            st = en
        if len(final_senid)!=0:  
            fnsens[fn] = final_senid
    return fnsens

	
import numpy as np
finalpositon_list = np.load('final_list.npy')
finalpositon_list = finalpositon_list.item()

import pandas as pd
def get_json(doclist):
# {64:[12,13]}
    res = {}
    for k,ids in enumerate(doclist):
        iids = ids
        ids = str(ids)
        res[ids] = {'text':[],'len':0,'time':0}
        tempp = pd.read_csv(f'IRC/{ids}.csv')
        temp_text = []
        senlist = doclist[iids]
        for id_sen in senlist:
            temp_sen = tempp.loc[int(id_sen)]
            temp_text.append([str(temp_sen['text']),str(temp_sen['speaker']),str(temp_sen['receiver'])])
#         res[ids]['sen'] = doclist[iids][0]
        res[ids]['sen'] = 0
        res[ids]['text'] = temp_text
        res[ids]['len'] = tempp.shape[0]
        fr = tempp.loc[0]
        res[ids]['year'] = fr['year']
        res[ids]['month'] = fr['month']
        res[ids]['day'] = fr['day']
        if k>20:
            break
#     print(res)
    return res

# 构建单词倒排表
import Levenshtein
nums = [str(x) for x in range(10)]
allkeys = list(finalpositon_list.keys())
inverted_word = {}
for key in allkeys:
    if any(x in key for x in nums):
        continue
    orikey = key
    key = "$" + key + "$"
    for ss in range(len(orikey)):
        tempk = key[ss:ss+2]
        if tempk not in inverted_word:
            inverted_word[tempk] = []
        inverted_word[tempk].append(orikey)

def handle_spell(word):
    orikey = word
    key = "$" + word + "$"
    candidate = {}
    for ss in range(len(orikey)):
        tempk = key[ss:ss+2]
        for wd in inverted_word[tempk]:
            if wd not in candidate:
                candidate[wd] = 0
            candidate[wd] += 1
    final = []
    for wo in candidate:
        if candidate[wo]>=2:
            dis = Levenshtein.distance(word,wo)
            if dis<=1:
                final.append(wo)
    return final

def handle_speaker(input_str):
    input_str = input_str.lower()
    inp = input_str.split(" ")
    if len(inp)==1:
        name = inp[0].split(":")[1]
        isp = inp[0].split(":")[0]
        if isp=='speaker':
            final =  final_sender_user_table[name]
        else:
            final =  final__reciver_user_table[name]
    else:
        speaker = inp[0].split(":")[1]
        recei = inp[1].split(":")[1]

        st = final_sender_user_table[speaker]
        en = final__reciver_user_table[recei]

        final = list(set(st).union(set(en)))
    res = {}
    for fn in final:
        res[fn] = [1]
    
    return res
def handle_mid(inputs):
    if 'and' in inputs:
        return handle_and(inputs)
    if 'or' in inputs:
        return handle_or(inputs)
    if 'not' in inputs:
        return handle_not(intputs)
    if '\s' in inputs:
        return handle_sentence(intputs)
    if len(inputs.split(" "))==1:
        return finalpositon_list[str(inputs.split(" ")[0]).lower()]

		
from flask import Flask
from flask import *
from flask_cors import *

app = Flask(__name__)

CORS(app, supports_credentials=True)

import numpy as np
# finalpositon_list = np.load('final_list.npy')
# finalpositon_list = finalpositon_list.item()
import json

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
@app.route('/check',methods=['GET','POST'])
def hello():
    if request.method == 'GET':
        data = request.args.get('query')
    else:
        return "error"
    finalre = {}
    data = str(data).lower()
    
    inps = data.split(' ')
    words = [x for x in inps if x not in ['and','or','not','/s','/p','0','1','2','3','4','5','6','7','8','9']]
    
    if '(' in data or ')' in data:
        left = re.search('\(',data).span(0)[0]
        right = re.search('\)',data).span(0)[1]
        mid = data[left+1:right-1]
        doclistmid = handle_mid(mid)
        
        ttp = data[:left-1].split(' ')
        ttb = data[right+1:].split(' ')
        fl = ttp[-1]
        bl = ttb[0]

        front = ttp[:-1]
        back = ttb[1:]
        
        doc1 = handle_mid(' '.join(front))
        doc2 = handle_mid(' '.join(back))
        fn1 = {}

        for dc in doclistmid:
            tps = []
            if dc in doc1:
                if fl=='and': 
                    tps = list(set(doclistmid[dc]).intersection(set(doc1[dc])))
                elif f1=='or':
                    tps = list(set(doclistmid[dc]).union(set(doc1[dc])))
                elif f1=='not':
                    tps = list(set(doclistmid[dc]).difference(set(doc1[dc])))
            if len(tps)!=0:
                fn1[dc] = tps
    
        doclist = {}
        for dc in fn1:
            tps = []
            if dc in doc2:
                if fl=='and': 
                    tps = list(set(fn1[dc]).intersection(set(doc2[dc])))
                elif f1=='or':
                    tps = list(set(fn1[dc]).union(set(doc2[dc])))
                elif f1=='not':
                    tps = list(set(fn1[dc]).difference(set(doc2[dc])))
            if len(tps)!=0:
                doclist[dc] = tps
                
        ret = get_json(doclist)
        pdre = json.dumps(ret,cls=MyEncoder)
        finalre['result'] = pdre
        return pdre
        
    if "speaker" in data or "receiver" in data:
        doclist = handle_speaker(data)
        ret = get_json(doclist)
        pdre = json.dumps(ret,cls=MyEncoder)
        finalre['result'] = pdre
        return pdre
    else:
        if len(inps)==1:
            if words[0] not in finalpositon_list:
                news = handle_spell(words[0])
                inps = ' or '.join(news)
                print(inps)
                doclist = handle_or(inps)
                ret = get_json(doclist)
                finalre['result'] = ret
                finalre['spell'] = news
                pdre = json.dumps(finalre,cls=MyEncoder)
                return pdre
            elif words[0] in final_sender_user_table:
                doclist = {}
                tempdoc = final_sender_user_table[words[0]]
                for fn in tempdoc:
                    doclist[fn] = [1]
                ret = get_json(doclist)
                finalre['result'] = ret
                pdre = json.dumps(finalre,cls=MyEncoder)
                return pdre
            elif words[0] in final__reciver_user_table:
                doclist = {}
                tempdoc = final__reciver_user_table[words[0]]
                for fn in tempdoc:
                    doclist[fn] = [1]
                ret = get_json(doclist)
                finalre['result'] = ret
                pdre = json.dumps(finalre,cls=MyEncoder)
                return pdre
            else:
                doclist = finalpositon_list[words[0]]
                ret = get_json(doclist)
                finalre['result'] = ret
                pdre = json.dumps(finalre,cls=MyEncoder)
                return pdre
        else:
            newinput = {}

            flag = False
            print(words)
            for wo in words:
                if wo not in finalpositon_list:
                    news = handle_spell(wo)
                    newinput[wo] = news
                    flag = True
            if flag:
                mentions = []
                for wo in newinput:
                    for it in newinput[wo]:
                        mentions.append(data.replace(wo,it))

                rrr = {'spell':mentions}
                return json.dumps(rrr,cls=MyEncoder)
            else:
                
                if 'and' in data:
                    doclist = handle_and(data)
                elif 'or' in data:
                    doclist = handle_or(data)
                elif '/s' in data:
                    doclist = handle_sentence(data)
                elif 'not' in data:
                    doclist = handle_not(data)
                else:
                    newinps = "/s ".join(inps) + " /s" + " 1"
                    doclist = handle_sentence(newinps)
    #     if len(doclist) == 0:
    #         return                                                                                                                                                                                                                                                                        doclist
    
    # 处理获取的数据, 返回指定json格式
                ret = get_json(doclist)
                pdre = json.dumps(ret,cls=MyEncoder)
                finalre['result'] = pdre
                return pdre

# if __name__ == "__main__":
app.run(debug=True,use_reloader=False,port=1234)
