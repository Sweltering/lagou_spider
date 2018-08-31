# 爬取拉钩网职位信息，这些数据是ajax发起异步请求的，在HTML代码中没有这些信息的，现在通过分析接口信息来获取这些职位信息

import requests
from lxml import etree
import time


headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3396.62 Mobile Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl'
                   '=false&fromSearch=true&labelWords=&suginput=',
        'Cookie': '_ga=GA1.2.1315255532.1534724140; user_trace_'
                  'token=20180820081540-2b7f2249-a40e-11e8-aa7e-5254005c3644; '
                  'LGUID=20180820081540-2b7f273b-a40e-11e8-aa7e-5254005c3644; showExpriedIndex=1; '
                  'showExpriedCompanyHome=1; showExpriedMyPublish=1; index_location_city=%E5%8C%97%E4%BA%AC; '
                  'hasDeliver=141; _gid=GA1.2.112981825.1535622218; '
                  'JSESSIONID=ABAAABAAADEAAFI5AE91EAD5BB610D26CCB6EAF55B2D55A; '
                  'LGSID=20180831121455-6a7d950e-acd4-11e8-be5e-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; '
                  'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; '
                  'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1534909049,1535096105,1535622218,1535688897; '
                  'TG-TRACK-CODE=index_search; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; '
                  'SEARCH_ID=7ec2f9a2983646c6ac5a93a21b5cf694; '
                  'LGRID=20180831121742-cdf55a78-acd4-11e8-b30a-5254005c3644; '
                  'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535689064',
        'Origin': 'https://www.lagou.com'
    }


# 爬取职位详情页的url
def request_list_page():
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'

    data = {
        'first': 'false',
        'pn': 1,
        'kd': 'python'
    }

    # 获取前13页的职位信息
    for x in range(1, 14):
        data['pn'] = x
        response = requests.post(url, headers=headers, data=data)
        result = response.json()  # response如果返回的是json数据，json()方法会自动load成字典
        positions = result['content']['positionResult']['result']  # 这个数据最后取到的是一个字典
        for position in positions:
            position_id = position['positionId']  # 职位id
            position_url = 'https://www.lagou.com/jobs/{}.html'.format(position_id)  # 构建职位详情页的url
            parse_position_detail(position_url)
            break
        break


# 爬取详情页的职位信息
def parse_position_detail(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)

    position_name = html.xpath('//h2[@class="title"]/text()')[0]  # 职位名称
    job_request_spans = html.xpath('//div[@class="items"]//span')
    salary = job_request_spans[1].xpath('.//text()')[0]  # 薪水
    city = job_request_spans[3].xpath('.//text()')[0]  # 城市
    work_years = job_request_spans[7].xpath('.//text()')[0]  # 工作年限
    education = job_request_spans[9].xpath('.//text()')[0].strip()  # 学历
    desc = "".join(html.xpath('//div[@class="positiondesc"]//text()')).strip()  # 职位描述
    print(desc)


def main():
    request_list_page()


if __name__ == '__main__':
    main()
