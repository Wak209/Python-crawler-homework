# Python-crawler-homework


功能1：对指定视频的数字数据（点赞、观看量等）进行获取：
分析视频源码可知，其网页代码经过了js渲染，而且所需要的数据有json格式的也有html格式的，最后选用正则表达式提取

···
 RE  =  re.compile(r'<meta data-vue-meta="true" itemprop="keywords" name="keywords" content="(?P<title_and_label>.*?)">.*?'#视频名和标签组成的字符串（以，分割
                    r'true" itemprop="description" name="description" content="(?P<introduction>.*?)".*?'#视频简介 -表示无
                    r'name="author" content="(?P<up_name>.*?)".*?'#up主名字
                    r',"timelength":(?P<timelength>.*?),".*?' #视频时长 单位是ms
                    r',"part":"(?P<part>.*?)",".*?' #分区
                    r'"article":.*?,"attentions":.*?,"fans":(?P<fans>.*?),"friend":.*?,.*?'
                    r'title="(?P<title>.*?)" class.*?'      #视频名字
                    r'<span title="总播放数(?P<view>.*?)" class="view".*?' #总播放量
                    r'</span><span title="历史累计弹幕数(?P<bili>.*?)" class="dm">.*?' #弹幕数
                    r'<span title="点赞数(?P<like>.*?)" class="like">.*?' #点赞数
                    r'</span><span title="投硬币枚数" class="coin">.*?</i>(?P<coin>.*?)</span>.*?' #投硬币枚数
                    r'<span title="收藏人数.*?</i>(?P<collect>.*?)</span>.*?' #收藏人数
                    r'<span title="分享" class="share"><i class="van-icon-videodetails_share"></i>(?P<share>.*?)<!----></span></div><div class="more">.*?' #转发 会有空格和回车
                    ,re.S)···


并把这些数据存入字典方便之后处理。

功能2：获取该视频的推荐视频并绘制图片对比：
在对推荐视频数据获取时最开始计划使用xpath获取，但是发现html格式中数据不全，缺少观看量、弹幕数量
    #html = etree.HTML(data1, etree.HTMLParser(encoding="utf-8")) #一定要编码！！！
    #name = html.xpath("/html/body/div[2]/div[4]/div[2]/div[5]/div[1]/div/div/div[2]/a/span/text()")
    #value = html.xpath("/html/body/div[2]/div[4]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[2]/text()")
    #tl = html.xpath('//*[@id="reco_list"]/div[1]/div[3]/div/div[1]/div[1]/span[2]/text()')
最后选择正则表达式获取js格式中的推荐视频
RE  =  re.compile(r'{"aid":.*?,"cid":.*?,"bvid":".*?","duration":(?P<tl>.*?),"pic":.*?,"title":"(?P<title>.*?)","owner":{"name":"(?P<up>.*?)","mid":(?P<mid>.*?)},"stat":{"danmaku":(?P<bili>.*?),"view":(?P<view>.*?)},"season_id":.*?,"season_type":.*?}',re.S)

之后进行指定视频与其旁边的推荐视频对比绘图，希望能直接发现影响视频热度（观看量，弹幕数量）因素，所选的因素有up主粉丝数量、视频时长、视频标题长度
在指定视频的源码中不具有推荐视频up主的粉丝数量，还需要爬虫获取
def get_fans(mid):
    url = f'https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp'
    resp = requests.get(url)
    dt = json.loads(resp.text)
    return dt['data']['follower']




(maxn参数可调，表示着一次对比中推荐视频数量)


功能3：对视频文字数据分析：
用网站的抓包工具可以找到请求弹幕、评论数据的url，弹幕的url需要cid，评论需要oid，而且还发现oid就是aid、cid是可以通过请求获得的（但也需要aid），所以通过指定视频bv获得aid（av号）也就成了关键。
Aid获取https://www.zhihu.com/answer/1099438784
弹幕词云绘制只需要把获取的弹幕连成一个字符串再调用jieba分词、统计词频功能即可。
评论数据处理最开始考虑写入文件，在之后需要时再读取文件，但是我虽然使用df.to_csv存储和readcsv读取时都使用了utf-8编码处理，但是在读取时仍存在编码错误，在网上查询发现好像是在文件内容过大（176281条评论）时就会出现编码问题，之后还考虑逐行读取、然后忽略编码问题处理
    '''Data = []
    with open('comment.csv',"rb") as myfile:
        #header = myfile.readline().decode('utf-8').replace('\r\n', '').split('\001')
        #print(header)
        for line in myfile:
            row = line.decode('utf-8', errors='ignore').replace('\r\n', '').split('\001')
            #print(row)
            if len(row) == 4:
                Data.append(row)
    data = pd.DataFrame(data=Data, columns = headers)'''
但是发现评论信息中有的存在回车，会导致错位，但是我又想保留原评论的格式，所以最后考虑使用全局变量，在记录和读取时使用同一个dataframe，在读取完毕后再写入文件
评论爬取时，考虑到数据量大，我还采用了多进程爬取。
功能4：绘制图像分析文字数据
词云绘制（反映视频大致内容与b站用户关注点），这部分存在bug，如BV1KF411J7Ri中有几千弹幕但是词云中元素却少的可怜，由于词云绘制基本上都是依靠jieba，我猜测可能是弹幕中的字符可能导致jieba分词或者词频出了问题

热门评论数据可视化

(Top参数可调，表示着展示热评前几名)


评论中账户性别数据可视化


通过评论数量随时间变化反映视频热度变化



(freq参数可调，表示着x轴列表长度，可改变时间跨度)

[简单数据分析]
在对多个视频数据可视化观察后，发现b站视频热度跟up粉丝数量有很大关系，跟时长与标题的关系十分微弱
在视频评论数据随时间变化分析可发现视频热度随时间涨幅节点，如黑神话第二只预告发出后，第一只预告视频的评论新增数量明显上升
