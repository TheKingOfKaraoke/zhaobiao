"""the script file be able read url file write to redis """
import os
import re
import threading
import time

import redis

FILE_PATH = "/Users/dengjiaxin/Desktop/herui/files/环保在线/hbzx_all_url/"

pool = redis.ConnectionPool(host='192.168.100.235', port=6379, decode_responses=True)
# client1 = redis.Redis(connection_pool=pool)
sum_list = []
COUNT=0
def redis_read(number, lock):
    global COUNT
    client1 = redis.Redis(connection_pool=pool)
    while sum_list:
        lock.acquire()
        COUNT += 1
        print(COUNT)
        data = sum_list.pop()
        lock.release()
        print("i'm{}--{}".format(number, data))
        client1.sadd("hbzx:dupefilter",data)


if __name__ == '__main__':
    start = time.time()
    for root, dirs, files in os.walk(FILE_PATH):
        # files type is list
        print(files)
        for filename in files:
            if filename.endswith(".txt"):
                with open(FILE_PATH + filename, "r") as f:
                    for i in f:
                        if i.startswith("https"):
                            info = re.findall(r'https://www.hbzhan.com/.*/', i)[0]
                            sum_list.append(info)
                            sum_list.append(i.replace("\n",""))

# https://www.hbzhan.com/st630444/product_20590300.html
    sum_list = list(set(sum_list))
    print(len(sum_list))
    # 线程池
    lock = threading.RLock()
    threads = []
    for th in range(300):
        threads.append(threading.Thread(target=redis_read, args=(th, lock)))
    for i in threads:
        i.start()


    end = time.time()
    print("总耗时:{}秒".format(end-start))

        # read_file("")