# a = "https://www.hbzhan.com/st630444/product_20590300.html"
# import re
# company_url = re.findall(r'https://www.hbzhan.com/.*/', a)#[0] if re.findall(r'https://www.hbzhan.com/.*/', a) else a
# print(company_url)
# import redis
# pool = redis.ConnectionPool(host='192.168.100.235', port=6379, decode_responses=True)
# client = redis.Redis(connection_pool=pool)
# # print(client.scard("zhaobiao_search_url"))
# def a():
#     # while 1:
#
#         print(client.spop("zhaobiao_search_url"))
# def b():
#     with open("searchurl.txt", "r") as r:
#         for url in r:
#             client.sadd("zhaobiao_search_url", url)
#
# def c():
#     cc = [
#         "https://www.hbzhan.com/st542102/product_19609636.html",
#         "https://www.hbzhan.com/st604533/product_21687744.html",
#         "https://www.hbzhan.com/st612338/product_21687445.html"
#     ]
#     for i in cc:
#         client.sadd("test:requests", i)
# #
# # a()
# # b()
# c()
import datetime
import time

url = '111'
try:
    raise Exception("hehe")
except Exception as e :
    with open("err.log", "a") as f:
        f.write("{}出现错误已经添加到队列---info:{}---date:{}\n".format(url, str(e), str(time.asctime( time.localtime(time.time()) ))))