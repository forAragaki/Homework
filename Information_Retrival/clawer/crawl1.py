from bs4 import BeautifulSoup
import re
import requests 
import csv

def getHtmlText(url, code = 'utf-8'):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""
    

def getlist(lst, furl,x = 4, flag = True):
    html = getHtmlText(furl)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            if flag:
                if re.findall(r'\d+/', href)[0]=='':
                    continue
                lst.append(furl+re.findall(f'^\d{{{x}}}/', href)[0])
            else:
                if re.findall(r'.*html$', href)[0] == '':
                    continue
                lst.append(re.findall(r'.*html$', href)[0])
        except:
            continue
    return lst

def getInfo(lst, furl, fpath):
    count = 0
    # year = re.findall(r'\d{4}', furl)[0].strip()
    # month = re.findall(r'/\d{2}/', furl)[0][1:-1].strip()
    # day = re.findall(r'/\d{2}/$', furl)[0][1:-1].strip()
    with open(fpath, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        for m in lst:
            url = furl + m
            html = getHtmlText(url)
            try:
                if html=='':
                    continue
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.find_all('h1')[0].text.strip()
                mess = soup.find_all('tr',{'id':True})
                # save('./mess1.txt',mess)
                for i in mess:
                    # time = i.find('a',{'class':'time'}).text.strip()
                    # save('./time1.txt', i.find('a',{'class': 'time'}).text)
                    try: 
                        # save('./speaker1.txt', i.find('th',{'class': 'nick'}))
                        speaker = i.find('th',{'class': 'nick'}).text.strip()
                        count += 1
                    except:
                        continue
                #     tex = i.find('td', {'class':'text'}).text
                #     # save('./text.txt',tex)
                #     receiver=''
                #     if re.findall(r'^.+: ', tex) != []:
                #         receiver = re.findall(r'^.+: ', tex)[0].strip()
                #         receiver = '' if ' ' in receiver[:-1] else receiver
                #         tex = tex.replace(receiver,'')
                #     tex = tex.replace('\xa0;',' ')
                #     tex = tex.replace('\xa0',' ').strip()
                #     # save('./text1.txt',tex)
                #     csv_writer.writerow([year,month,day,time,speaker,receiver[:-1],tex])
                csv_writer.writerow([title, count])
                # count += 1    
                print('\r{}/{} '.format(title, count), end='')       
            except:
                print('error')
                # count += 1
                print('\r{}/{}'.format(title, count), end='')
                continue


def save(fpath, lst):
    with open(fpath, 'a', encoding='utf-8') as f:
        f.write(str(lst)+'\n')

def main():
    raw_url = "https://irclogs.ubuntu.com/"
    output_file = './Info.csv'
    data_file = './data.txt'
    datas = []
    lst = []
    # getlist(lst, 'https://irclogs.ubuntu.com/2004/09/12/', flag=False)
    # getInfo(lst, 'https://irclogs.ubuntu.com/2004/09/12/', output_file)
    with open(data_file,'r', encoding='utf-8') as f:
        for data in f.readlines():
            data = data.strip()
            datas.append(data)

    with open(output_file, 'w', encoding='utf-8',newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['doc','line_number'])
    # with open(output_file, 'w', encoding='utf-8',newline='') as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerow(['year','month','day','time','speaker','receiver','text'])
    for data in datas:
        getlist(lst, data, flag=False)
        getInfo(lst, data, output_file)
        lst.clear()
    # year = []
    # month = []
    # datas = []
    # getlist(year, raw_url,4)
    # for i in year:
    #     getlist(month, i,2)
    # year.clear()
    # for i in month:
    #     getlist(datas, i,2)
    # month.clear()
    # save(data_file, data)
    # getInfo(lst, raw_url, output_file)


if __name__ == '__main__':
    main()