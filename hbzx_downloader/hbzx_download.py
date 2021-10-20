import threading
import time

import redis
import requests

from proxy import proxies

PATH = "/Users/dengjiaxin/Desktop/herui/zhaobiao/files/"
pool = redis.ConnectionPool(host='192.168.100.235', port=6379, decode_responses=True)


def download(number):
    client = redis.Redis(connection_pool=pool)
    while True:
        print("im:{}".format(number))
        # 取数据
        # url = client.spop("hbzx:requests")
        url = client.spop("hbzx:requests")
        if url is None:
            print("url为空开始等待")
            time.sleep(10)
            continue
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
        }
        try:
            response = requests.get(url=url, headers=headers, proxies=proxies, timeout=15)
            if response.status_code != 200:
                raise Exception("非200")
            else:
                with open(PATH + url.replace("/", "*"), "w") as w:
                    w.write(response.text)
        except Exception as e:
            with open("err.log", "a") as f:
                f.write("{}出现错误已经添加到队列---info:{}---date:{}\n".format(url, str(e),
                                                                     str(time.asctime(time.localtime(time.time())))))
            client.sadd("hbzx:request_failed", url)


if __name__ == '__main__':
    # 生成锁
    # download(1)
    lock = threading.RLock()
    # 创建多线程下载
    threads_list = []
    for th in range(10):
        threads_list.append(threading.Thread(target=download, args=(th,)))
    for th in threads_list:
        th.start()
        th.join()
