import requests

url = "https://www.hbzhan.com/st542102/product_19609636.html"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
}
response = requests.get(url=url, headers=headers)
with open("test.html", "w") as w:
    w.write(response.text)