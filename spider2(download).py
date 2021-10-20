import threading
COUNT = 0
import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)

def download(number, lock):
    """下载！"""
    global COUNT
    client = redis.Redis(connection_pool=pool)
    # print(client.spop("zhaobiao_search_url"))
    while 1:
        print("im:{}".format(number))
        url = client.spop("zhaobiao_search_url")
        print(url)
        if url is None:
            break





if __name__ == '__main__':
    # download(1,1)
    lock = threading.RLock()
    threads = []
    for th in range(10):
        threads.append(threading.Thread(target=download, args=(th, lock)))
    for th in threads:
        th.start()