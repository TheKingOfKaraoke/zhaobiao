# coding=utf-8
import io
import sys
import time

from lxml import etree
import requests
import csv

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


class Main:

    def __init__(self):
        self.url = "https://s.zhaobiao.cn/s"
        # self.key_words = ['净水器', '净水机', '饮水机', '饮水器', '开水器', '售水机', '净饮水', '富氢水', '茶吧机 ', '热水', '地暖']
        # self.key_words = [  '地暖']
        self.key_words = ['大气监测','废气监测','水质监测','气体检测','VOCs监测','烟尘监测','气体检测','水质检测']
        self.params = {
            "queryword": "",
            "field": "title",
            "searchtype": "zb",
            "channels": "succeed",
            'currentpage': 1,
            'totalPage': 100,
            'maxPages': 100,
            'relTotalPages': 6157,
            'attachment': 1,
            'isLogin':'true'
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            'Cookie': 'CNZZDATA5373302=cnzz_eid%3D1872521335-1634281217-%26ntime%3D1634604674; Cookies_token=5de91865-b6f1-40a2-b9fa-4c0b635f949c; reg_referer=aHR0cHM6Ly9zLnpoYW9iaWFvLmNuL3M=; Cookies_SearchHistory_new="5aSn5rCU55uR5rWLIyPlup/msJTnm5HmtYsjIw=="; JSESSIONID=F07B6B618B6CCFF4EB70473116D6ECAD; __gads=ID=eb9b8f72f8fe4b87-229d59e49acc007f:T=1634289269:RT=1634289269:S=ALNI_MZ0yLzNy9RnExWwq4wYfdcuMF6Cnw; UM_distinctid=17c833986bfe7a-011a2d88fff46e-49193201-280000-17c833986c0f43; __jsluid_s=a3d5262a856b627fac2499475fed7ac5'
        }
        self.csv_headers = ["关键词", "公司名", "法人名", "行业", "电话", "邮箱", "地址", "注册时间", "营业期限", "注册资本", "人员规模", "统一社会信用代码",
                            "组织机构代码", "注册号",
                            "经营状态",
                            "公司类型", "登记机关", "业务范围"]
        self.now_key_word = ""

    def start(self):
        """Start"""
        page = 1
        for key_word in self.key_words:
            self.now_key_word = key_word
            self.params["queryword"] = key_word
            while 1:
                self.params["currentpage"] = page
                print("第{}页".format(page))
                response = self.search_index(page)
                if response is False:
                    page = 1
                    break
                page += 1


    #


    def search_index(self, page):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        response.encoding = response.apparent_encoding
        with open("search.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        html = etree.HTML(response.text)
        if not html.xpath("/html/body/table/tbody/tr[2]/td[2]/a/@href"):
            return False
        res = html.xpath("//tbody[2]/tr")
        for i in range(1, len(res) + 1):
            print("第{}页---第{}条".format(page, i))
            page_url = html.xpath("//tbody[2]/tr[{}]/td[2]/a/@href".format(i))
            self.page_analysis(page_url[0])

    def page_analysis(self, url=None):
        """内容页分解"""
        response = requests.get(url=url, headers=self.headers)
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text)
        company_area = html.xpath("/html/body/div[5]/div[3]/div/div[6]/div/ul/li")
        if not company_area:
            return
        else:
            for count, i in enumerate(company_area):
                company_info_page = html.xpath(
                    "/html/body/div[5]/div[3]/div/div[6]/div/ul/li[{}]/a/@href".format(count + 1))
                self.company_info(company_info_page[0])

    def company_info(self, url):
        response = requests.get(url=url, headers=self.headers)
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text)
        if not html:
            return
        with open("info.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        # 公司名
        company_name = html.xpath("//table[@class='comp_info']/tr[1]/td[2]/text()")
        # 法人名
        name = html.xpath("//table[@class='comp_info']/tr[2]/td[2]/text()")
        # 行业
        industry = html.xpath("//table[@class='comp_info']/tr[2]/td[4]/text()")
        # 电话
        mobile_phone = html.xpath("//table[@class='comp_info']/tr[3]/td[2]/label/text()")
        # 邮箱
        email = html.xpath("//table[@class='comp_info']/tr[4]/td[2]/label/text()")
        # 地址
        address = html.xpath("//table[@class='comp_info']/tr[5]/td[2]/text()")
        # 注册时间
        register_time = html.xpath("//table[@class='comp_info']/tr[6]/td[2]/text()")
        # 营业期限
        operating_period = html.xpath("//table[@class='comp_info']/tr[6]/td[4]/text()")
        # 注册资本
        registered_capital = html.xpath("//table[@class='comp_info']/tr[7]/td[2]/text()")
        # 人员规模
        scale = html.xpath("//table[@class='comp_info']/tr[7]/td[4]/text()")
        # 统一社会信用代码
        credit_code = html.xpath("//table[@class='comp_info']/tr[8]/td[2]/text()")
        # 组织机构代码
        organization_code = html.xpath("//table[@class='comp_info']/tr[8]/td[4]/text()")
        # 注册号
        register_code = html.xpath("//table[@class='comp_info']/tr[9]/td[2]/text()")
        # 经营状态
        operating_status = html.xpath("//table[@class='comp_info']/tr[9]/td[4]/text()")
        # 公司类型
        company_type = html.xpath("//table[@class='comp_info']/tr[10]/td[2]/text()")
        # 登记机关
        registration_authority = html.xpath("//table[@class='comp_info']/tr[10]/td[4]/text()")
        # 业务范围
        business_scope = html.xpath("//table[@class='comp_info']/tr[11]/td[2]/text()")
        # print(company_name)
        # print(name)
        # print(industry)
        # print(mobile_phone)
        # print(email)
        # print(address)
        # print(register_time)
        # print(operating_period)
        # print(registered_capital)
        # print(scale)
        # print(credit_code)
        # print(organization_code)
        # print(register_code)
        # print(operating_status)
        # print(company_type)
        # print(registration_authority)
        # print(business_scope)
        row = [
            {"关键词": self.now_key_word, "公司名": company_name[0] if company_name else "", "法人名": name[0] if name else "",
             "行业": industry[0] if industry else "", "电话": mobile_phone[0] if mobile_phone else "",
             "邮箱": email[0] if email else "",
             "地址": address[0] if address else "",
             "注册时间": register_time[0] if register_time else "",
             "营业期限": operating_period[0] if operating_period else "",
             "注册资本": registered_capital[0] if registered_capital else "", "人员规模": scale[0] if scale else "",
             "统一社会信用代码": credit_code[0] if credit_code else "",
             "组织机构代码": organization_code[0] if organization_code else "",
             "注册号": register_code[0] if register_code else "",
             "经营状态": operating_status[0] if operating_status else "",
             "公司类型": company_type[0] if company_type else "",
             "登记机关": registration_authority[0] if registration_authority else "",
             "业务范围": business_scope[0] if business_scope else ""}]
        try:
            print(row)
        except Exception as e:
            print(e)
        # with open("test.csv", "a", newline="",encoding="utf-8-sig") as f:
        try:
            with open("zhaobiao.csv", "a", newline="") as f:
                csvf = csv.DictWriter(f, self.csv_headers)
                csvf.writerows(row)
        except Exception as e:
            with open("err.log", 'a') as f:
                f.write(str(e))
                f.write(url)


print("start")
main = Main()
main.start()
