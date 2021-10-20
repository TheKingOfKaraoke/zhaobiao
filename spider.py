"""爬关键词添加到队列"""

import threading

import redis
import requests
from lxml import etree
from proxy import proxies

SEARCH_URL = "https://s.zhaobiao.cn/s"
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
client = redis.Redis(connection_pool=pool)
sum_url_list = []
SEARCH_COUNT = 0
SEARCH_INDEX_COUNT = 0

def search(keyword):
    """this funcation is search keyword for hzaobiao.cn"""
    global SEARCH_COUNT
    currentpage = 1
    params = {
        "field": "title",
        "searchtype": "zb",
        "isLogin": "true",
        "queryword": keyword
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        'Cookie': 'CNZZDATA5373302=cnzz_eid%3D1872521335-1634281217-%26ntime%3D1634604674; Cookies_token=5de91865-b6f1-40a2-b9fa-4c0b635f949c; reg_referer=aHR0cHM6Ly9zLnpoYW9iaWFvLmNuL3M=; Cookies_SearchHistory_new="5aSn5rCU55uR5rWLIyPlup/msJTnm5HmtYsjIw=="; JSESSIONID=F07B6B618B6CCFF4EB70473116D6ECAD; __gads=ID=eb9b8f72f8fe4b87-229d59e49acc007f:T=1634289269:RT=1634289269:S=ALNI_MZ0yLzNy9RnExWwq4wYfdcuMF6Cnw; UM_distinctid=17c833986bfe7a-011a2d88fff46e-49193201-280000-17c833986c0f43; __jsluid_s=a3d5262a856b627fac2499475fed7ac5'
    }
    csv_headers = ["关键词", "公司名", "法人名", "行业", "电话", "邮箱", "地址", "注册时间", "营业期限", "注册资本", "人员规模", "统一社会信用代码",
                   "组织机构代码", "注册号",
                   "经营状态",
                   "公司类型", "登记机关", "业务范围"]
    for i in range(1,11):
        try:
            response = requests.get(url=SEARCH_URL, headers=headers, params=params, proxies=proxies)
            print("OK")
            break
        except:
            pass
        print("{}第{}次".format(keyword,i))
    html = tree(response.text)
    totalPage = html.xpath("//input[@id='totalPage']/@value")[0]
    for s in range(1,int(totalPage)+1):
        url = 'https://s.zhaobiao.cn/s?searchtype=zb&queryword={}&currentpage={}&field=title'.format(keyword, s)
        print(url)
        sum_url_list.append(url)
        client.sadd("zhaobiao_search_url", url)
        SEARCH_COUNT += 1
        print(SEARCH_COUNT)
        with open("searchurl.txt", "a") as w:
            w.write(str(url+'\n'))
def tree(html):
    return etree.HTML(html)






if __name__ == '__main__':
    keywords = ['大气监测', '废气监测', '水质监测', '气体检测', 'VOCs监测', '烟尘监测', '水质检测', '暖通', '制冷展', '热泵', '两联供', '太阳能', '空调',
                '供热', '智能家居',
                '智能控制', '智能物联', '新风系统', '通风设备', '空气净化器', '管业', '管道', '电线', '电缆', '不锈钢', '塑胶', '塑料', '铜业', '线缆', '建筑工程',
                '施工安装', '机电安装/设备', '建筑设计院'
        , '装饰装潢', '水务水司', '给排水工程', '消防工程', '自来水', '工装', '家装', '建材'
                ]
    #获得请求队列
    with open("searchurl.txt", "w") as w:
        w.close()
    for keyword in keywords:
        search(keyword)



# 大气监测、废气监测、水质监测、气体检测、VOCs监测、烟尘监测
# 、水质检测
# 暖通、制冷展、热泵、两联供、太阳能、空调、供热、智能家居、智能控制、智能系统集成、智能控制、智能物联
# AVT：新风系统、通风设备、空气净化器
# 管业、管件、管道、电线、电缆、不锈钢、塑胶、塑料、铜业、线缆
# 观众关键词：
# 建筑工程、施工安装、机电安装 / 设备、建筑设计院、装饰装潢、水务水司、给排水工程、消防工程、自来水、工装、家装、建材
