#自动化2003 王开 0122005690211 2022-4-27
from concurrent.futures import ThreadPoolExecutor
from distutils.log import error
from itertools import count
from collections import Counter
from nturl2path import url2pathname
from pprint import pprint
from string import printable
from threading import main_thread
from xml.etree.ElementTree import Comment
from django.db import reset_queries
from joblib import PrintTime
from pyecharts.globals import ThemeType
import matplotlib.pyplot as plt
from tkinter.tix import TList
from unittest import result
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import pandas as pd
from jieba import analyse
import jieba 
import operator
from urllib import response
from django.urls import re_path
from matplotlib.pyplot import title
from numpy import append, dtype, printoptions
from pip import main
from pyecharts.charts import Bar,Grid,Line,Pie
import requests
import re
import json
from lxml import etree
from bs4 import BeautifulSoup
from pyecharts import options as opts
from threading import Thread
import csv
Dict={}#所搜视频字典
time_dt={}#评论时间字典
ct_us,ct_ms,ct_lk,ct_sx,ct_tm=[],[],[],[],[]#评论数据列表
Lt=[]#所以视频的列表
maxtime,Flag = 0, 0
lt_name=['label','introduction','up_name','timelength','part','fans','Title','view','bili','like','coin','collect','share']
label = 0 ;introduction = 1;timelength = 3;part = 4;Title = 6;view = 7;bili = 8;like = 9 ;coin = 10;collect = 11;share = 12 ;up_name = 2;fans = 5

def BV2AV(BV):
    table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr={}
    for i in range(58):
        tr[table[i]]=i
    s=[11,10,3,8,4,6]
    xor=177451812
    add=8728348608
    r=0
    for i in range(6):
        r+=tr[BV[s[i]]]*58**i
    return (r-add)^xor
def get_info(BV):
    url = f'https://www.bilibili.com/video/{BV}'
    resp = requests.get(url)
    #print(resp)
    with open('data1.csv','w',encoding='utf-8') as file:   #resp.text  ==>  <class 'str'>
        file.write(resp.text) 
    resp.close()

def get_fans(mid):
    url = f'https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp'
    resp = requests.get(url)
    dt = json.loads(resp.text)
    return dt['data']['follower']
def op_info():
    ''' 目标数据： 1.标签、简介 、时长、分区
        2.视频名字、总播放量、弹幕数、发布时间、发布时间、点赞数、投硬币枚数、收藏人数、转发、up主名字、up主粉丝数'''
    with open('data1.csv','r',encoding='utf-8') as file:
        data1 = file.read()
        RE  =  re.compile(r'<meta data-vue-meta="true" itemprop="keywords" name="keywords" content="(?P<title_and_label>.*?)">.*?'#视频名和标签组成的字符串（以，分割
                    r'true" itemprop="description" name="description" content="(?P<introduction>.*?)".*?'#视频简介 -表示无
                    r'name="author" content="(?P<up_name>.*?)".*?'#up主名字
                    r',"timelength":(?P<timelength>.*?),".*?' #视频时长 单位是ms
                    r',"part":"(?P<part>.*?)",".*?' #分区
                    r'"article":.*?,"attentions":.*?,"fans":(?P<fans>.*?),"friend":.*?,.*?'
                    r'title="(?P<title>.*?)" class.*?'      #视频名字
                    r'<span title="总播放数(?P<view>.*?)" class="view".*?' #总播放量
                    r'</span><span title="历史累计弹幕数(?P<bili>.*?)" class="dm">.*?' #弹幕数
                    r'<span title="点赞数(?P<like>.*?)" class="like">.*?' #点赞数
                    r'</span><span title="投硬币枚数" class="coin">.*?</i>(?P<coin>.*?)</span>.*?' #投硬币枚数
                    r'<span title="收藏人数.*?</i>(?P<collect>.*?)</span>.*?' #收藏人数
                    r'<span title="分享" class="share"><i class="van-icon-videodetails_share"></i>(?P<share>.*?)<!----></span></div><div class="more">.*?' #转发 会有空格和回车
                    ,re.S)

    result =  RE.findall(data1)
    #print(result)
    Self=[]#数据类型转化 含元组的列表-->列表
    for i in result[0]:
        Self.append(i)
    lt=Self[label].split(',')#处理数据 删去 title_and_label中无用的 删去share的回车空格
    lt.remove(Self[Title])
    lt.remove('哔哩哔哩')
    lt.remove('Bilibili')
    lt.remove('B站')
    lt.remove('弹幕')
    Str=''
    for i in lt:
        Str += i + ' '
    Self[label] = Str
    Self[share] = Self[share].strip()
    Self[up_name] = Self[up_name].strip()
    Self[coin] = Self[coin].strip()
    Self[collect] = Self[collect].strip()
    Self[share] = Self[share].strip()
    #print(Self)
    S_time=int(int(Self[timelength])/1000)#创造所搜索视频的字典,并描述
    time_description=''
    time_description += str(int(S_time/60))
    time_description += ':'
    if len(str((S_time-(int(S_time/60))*60))) == 0 :
        time_description += '00'
    elif len(str((S_time-(int(S_time/60))*60))) == 1 :
        time_description += '0'+str((S_time-(int(S_time/60))*60))
    elif len(str((S_time-(int(S_time/60))*60))) == 2 :
        time_description += str((S_time-(int(S_time/60))*60)) 
    print(f'视频名称：{Self[Title]},时长：{time_description},该视频所属的分区：{Self[part]}')
    if Self[introduction] != '-':
        print(f'视频简介：{Self[introduction]}')
    else:
        print(f'这个up很懒,没写简介')
    print(f'视频标签：{Self[label]}')
    print(f'该视频播放量：{Self[view]},弹幕量：{Self[bili]},点赞量：{Self[like]},投币量：{Self[coin]},收藏量：{Self[collect]},转发量：{Self[share]}')
    print(f'该视频由{Self[up_name]}发布,粉丝数为{Self[fans]}')
    for i in range(len(lt_name)):
        Dict[lt_name[i]] = Self[i]
    #print(Dict)
def get_fans(mid):
    url = f'https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp'
    resp = requests.get(url)
    dt = json.loads(resp.text)
    return dt['data']['follower']

def draw_compare():
    with open('data1.csv','r',encoding='utf-8') as file:
        data1 = file.read()
    #html = etree.HTML(data1, etree.HTMLParser(encoding="utf-8")) #一定要编码！！！
    #name = html.xpath("/html/body/div[2]/div[4]/div[2]/div[5]/div[1]/div/div/div[2]/a/span/text()")
    #value = html.xpath("/html/body/div[2]/div[4]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]/text()")
    #tl = html.xpath('//*[@id="reco_list"]/div[1]/div[3]/div/div[1]/div[1]/span[2]/text()')
                #//*[@id="reco_list"]/div[1]/div[3]/div/div[1]/div[1]/span[2]
                #/html/body/div[2]/div[4]/div[2]/div[5]/div[1]/div[2]/div/div[1]/div[1]/span[2]
    RE  =  re.compile(r'{"aid":.*?,"cid":.*?,"bvid":".*?","duration":(?P<tl>.*?),"pic":.*?,"title":"(?P<title>.*?)","owner":{"name":"(?P<up>.*?)","mid":(?P<mid>.*?)},"stat":{"danmaku":(?P<bili>.*?),"view":(?P<view>.*?)},"season_id":.*?,"season_type":.*?}',re.S)
    result =  RE.findall(data1)
    Lt=[]
    for i in result:#把列表嵌套元组转化成列表
        fans = get_fans(i[-3])#得到粉丝数量
        lt=[]
        for j in range(len(i)):
            if j != 3:
                lt.append(i[j])
            else :
                lt.append(fans)
        Lt.append(lt)
    for i in range(len(Lt)):#把播放量转化成int类型来排序
        Lt[i][-1] = int(Lt[i][-1])
    Lt=sorted(Lt,key = lambda x:x[-1],reverse=True)
    maxn = 5#与主视频一起画图的其他视频数量
    x_lt,y_timelength,y_bili_lt,y_view_lt,y_fans,y_ttl=[],[],[],[],[],[]
    y_fans.append(Dict["like"]);y_timelength.append(int(int(Dict["timelength"])/1000));y_bili_lt.append(Dict["bili"]);y_view_lt.append(Dict["view"]);y_ttl.append(len(Dict["Title"]))
    for i in range(0,maxn):
        y_timelength.append(Lt[i][0])
        y_bili_lt.append(Lt[i][-2])
        y_view_lt.append(Lt[i][-1])
        y_fans.append(Lt[i][3])
        y_ttl.append(len(Lt[i][1]))
    x_lt.append("主视频")
    for i in range(1,maxn+1):
        x_lt.append(f'推荐视频{i}')
    bar = (
        Bar()
        .add_xaxis(x_lt)
        .add_yaxis(
            "播放量",
            y_view_lt, 
            yaxis_index=0,
            color="#d14a61", 
        )
        .add_yaxis(
            "弹幕量", 
            y_bili_lt,
            yaxis_index=1,
            color="#5793f3", 
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="弹幕数量", 
                type_="value",
                position="right",  
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="时长",
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} s"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, 
                    linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="粉丝数",
                position="right",
                offset=160,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=False, 
                    linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="标题长度",
                position="right",
                offset=240,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=False, 
                    linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="观看量",
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            ),
            title_opts=opts.TitleOpts(title="主视频数据与推荐视频对比"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )
    line = (
        Line()
        .add_xaxis(x_lt)
        .add_yaxis(
            "时长",
            y_timelength,
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            "粉丝数",
            y_fans,
            yaxis_index=3,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            "标题长度",
            y_ttl,
            yaxis_index=4,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
        
    )
    bar.overlap(line) 
    grid = Grid()
    grid.add(
        bar, 
        opts.GridOpts(
            pos_left="5%",
            pos_right="20%"), 
            is_control_axis_index=True
            )
    grid.render("time.html")
def get_cid(av):
    url = f'https://api.bilibili.com/x/player/pagelist?aid={av}&jsonp=jsonp'
    res = requests.get(url)
    dt = json.loads(res.text)
    return dt["data"][0]["cid"]
def draw_cloud(av):
    cid = get_cid(av)
    url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
    #print(url)
    res = requests.get(url)
    data = res.content.decode("utf-8")
    #print(data)
    RE = re.compile (r'<d p=".*?">(?P<timelength>.*?)</d>',re.S)
    result = RE.findall(data)
    #print(result)
    text=str()
    for i in result:
        text += i
    #print(text)
    alice_coloring = np.array(Image.open('b.jpg'))
    wc = WordCloud(font_path = 'simhei.ttf',background_color='white', max_words=50,width=1000,height=1000,mask=alice_coloring)
    wc.generate_from_text(text)
    wc.generate(text)
    plt.imshow(wc)
    plt.axis("off")  
    plt.show()

def get_one_page(bv,page,av):
    global maxtime,Flag
    if Flag == 1 :
        return 
    url = f'https://api.bilibili.com/x/v2/reply/main?&jsonp=jsonp&next={page}&type=1&oid={av}&mode=3'
    print(f'正在获取第{page}页.....flag:{Flag}')
    #ct_us,ct_ms,ct_sx,ct_lk=[],[],[],[]
    resp = requests.get(url)
    data = json.loads(resp.text)
    if data['data']['replies'] == None:
        Flag = 1
    for i in range(len(data['data']['replies'])):
        ct_us.append(data["data"]["replies"][i]["member"]["uname"])
        ct_ms.append(data["data"]["replies"][i]["content"]["message"].strip('\n'))
        ct_sx.append(data["data"]["replies"][i]["member"]["sex"])
        ct_lk.append(int(data["data"]["replies"][i]["like"]))
        if '天前发布' in data["data"]["replies"][i]["reply_control"]["time_desc"]:
            ct_tm.append(data["data"]["replies"][i]["reply_control"]["time_desc"].strip('天前发布'))
        else:
            ct_tm.append(0)
        if int(data["data"]["replies"][i]["reply_control"]["time_desc"][:-4]) >= maxtime:
            maxtime = int(data["data"]["replies"][i]["reply_control"]["time_desc"][:-4]) 
        '''if  data.get(data["data"]["replies"][i]["reply_control"]["time_desc"][:-4]) == None:
            time_dt[data["data"]["replies"][i]["reply_control"]["time_desc"][:-4]] = 1
        else:
            time_dt[data["data"]["replies"][i]["reply_control"]["time_desc"][:-4]] += 1'''
        '''  with open('comment2.csv','a',encoding='utf-8') as f:
            f.write(f'{data["data"]["replies"][i]["member"]["uname"]}\001{data["data"]["replies"][i]["content"]["message"]}\001{data["data"]["replies"][i]["member"]["sex"]}\001{int(data["data"]["replies"][i]["like"])}\n')'''
    #dataframe = pd.DataFrame({'user':ct_us,'comment':ct_ms,'sex':ct_sx,'like':ct_lk})
    #dataframe.to_csv('comment.csv',index=False,sep='\001',mode='a',encoding='utf-8')
def get_all_comment(av,bv):
    with ThreadPoolExecutor(200) as t:
        for i in range(1,100000):
            if Flag == 1 :
                break
            t.submit(get_one_page,bv,i,av) 
    print('OK!')
def draw_cmt_bar(bv):
    Top = 20#(Top参数可调，表示着展示热评前几名)
    '''Data = []
    with open('comment.csv',"rb") as myfile:
        #header = myfile.readline().decode('utf-8').replace('\r\n', '').split(',')
        #print(header)
        for line in myfile:
            row = line.decode('utf-8', errors='ignore').replace('\r\n', '').split('\001')
            #print(row)
            if len(row) == 4:
                Data.append(row)'''
    #data = pd.DataFrame(data=Data, columns = ['user','comment','sex' ,'like'])
    data = pd.DataFrame({'user':ct_us,'comment':ct_ms,'sex':ct_sx,'like':ct_lk})
    data.to_csv('comment.csv',index=False,sep='\001',mode='w',encoding='utf-8')
    #filename = open('comment.csv', encoding='utf-8')
    #data = pd.read_csv('comment.csv',sep='\001',encoding='utf-8',engine='python',error_bad_lines=False)
    data = data[(data.user!='user')]
    #print(data['like'])
    data = data.dropna(axis = 0)
    #print(data['like'].tolist())
    data['like']=data['like'].astype(int)
    data1 = data.sort_values(by="like",ascending=False).head(Top)
    #print(data1.columns.tolist())
    #print(data1.values)
    bar=(
        Bar()
        .add_xaxis(data1["comment"].tolist())
        .add_yaxis("点赞数",data1["like"].tolist())
        .set_global_opts(
            title_opts = opts.TitleOpts(title=f'热评Top{Top}'),
            datazoom_opts = [opts.DataZoomOpts(),opts.DataZoomOpts(type_='inside')])
    )
    bar.render("like.html")
def draw_cmt_pie(bv):
    '''Data = []
    with open('comment.csv',"rb") as myfile:
        #header = myfile.readline().decode('utf-8').replace('\r\n', '').split(',')
        #print(header)
        for line in myfile:
            row = line.decode('utf-8', errors='ignore').replace('\r\n', '').split('\001')
            #print(row)
            if len(row) == 4:
                Data.append(row)
    data = pd.DataFrame(data=Data, columns = headers)'''
    x_data = ['男', '女', '保密']
    data = pd.DataFrame({'user':ct_us,'comment':ct_ms,'sex':ct_sx,'like':ct_lk})
    #print(data['sex'].tolist())
    y_data = [int(data['sex'].value_counts()['男']), int(data['sex'].value_counts()['女']), int(data['sex'].value_counts()['保密'])]#一定要把<class 'numpy.int64'>转化成int形式！！！！！
    dt = [i for i in zip(x_data, y_data)]
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
        .add("性别",data_pair=dt, radius=['40%', '55%'])
        .set_global_opts(
            title_opts=opts.TitleOpts(title='评论区性别情况'),
            tooltip_opts=opts.TooltipOpts(formatter='{a} </br> {b}:{c} ({d}%)'),
            legend_opts=opts.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%'),
        )
        .render("sex.html"))
def draw_time_change():
    freq = 10#(freq参数可调，表示着x轴列表长度，可改变时间跨度)
    sepp = int(maxtime / freq )
    x = [maxtime]
    #print(maxtime)
    for i in range(1,freq):
        x.append(maxtime - i*sepp)
    #print(x)
    y = [0] * freq 
    for i in range(len(ct_tm)) :
        if int(ct_tm[i]) <= x[-1]:
            wch = freq-1
        elif (int(ct_tm[i]) - x[-1]) % sepp == 0:
            wch =freq - (int((int(ct_tm[i]) -  x[-1])/sepp))-1
        else:
            wch =freq - (int((int(ct_tm[i]) -  x[-1])/sepp)+1)-1
        y[wch] +=1
    '''for key,value in time_dt.items():
        print(key)
        if int(key) <= x[-1]:
            wch = freq-1
        elif (int(key) - x[-1]) % sepp == 0:
            wch =freq - (int((int(key) -  x[-1])/sepp))-1
        else  :
            wch =freq - (int((int(key) -  x[-1])/sepp)+1)-1
        y[wch] += int (time_dt[key])'''
    xx=[]
    for i in range(len(x)-1) :
        xx.append  (f'{x[i]}~{x[i+1]}天前')
    xx.append(f'{x[-1]}~0天')
    #print(xx)
    line=(
        Line()
        .add_xaxis(xx)
        .add_yaxis("",y)
        .set_global_opts(opts.TitleOpts(title='视频评论数据随时间变化'),xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 15}))
        .render("ct_time.html")
    )
if __name__ == '__main__':
    BV=input('请输出你要查询的BV号：')#BV='BV1x54y1e7zf'  'BV1KF411J7Ri'
    #BV='BV1x54y1e7zf'
    AV=BV2AV(BV)#输入的BV号转为AV号.
    #print(AV)
    get_info(BV)#视频自身信息爬取 (通过网站自身源代码)并存入文件
    op_info()#从文件1中读取、处理数据，最终得到本视频的信息
    draw_compare()#从文件1中读取本视频下面推荐视频的数据，并绘图比较  maxn===>同时画图对比的推荐视频数量
    get_all_comment(AV,BV)#得到评论信息
    draw_cmt_bar(BV)#绘制热评柱状图 
    draw_cmt_pie(BV)#绘制评论性别饼图
    draw_time_change()#绘制自视频发布以来评论数量变化  freq===>折线图横轴数量
    draw_cloud(AV)#画弹幕词云