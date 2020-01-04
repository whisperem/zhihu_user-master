# -*- coding:utf-8 -*-
__author__ = 'LXG'
__date__ = '2020/1/4 10:54'

import requests
import pymongo
import time


# 第一页种子
def get_first_page():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36'
    }
    # url = 'https://www.zhihu.com/api/v4/members/zhouyuan/followees?include=data%5B*%5D.answer_count' \
    #       '%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(' \
    #       'type%3Dbest_answerer)%5D.topics&offset=0&limit=20'

    url = 'https://www.zhihu.com/api/v4/questions/35953016/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=1&offset=0&platform=desktop&sort_by=default'
    url_follow_num = 'https://www.zhihu.com/api/v4/questions/35953016/followers?include=data%5B*%5D.gender%2Canswer_count%2Carticles_count%2Cfollower_count%2Cis_following%2Cis_followed&limit=10&offset=0'
    # url = 'https://www.zhihu.com/api/v4/answers/446545012/rewarders?include=data%5B*%5D.answer_count%2Carticles_count%2Cfollower_count%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed&offset=0&limit=10'

    response = requests.get(url, headers=header)
    return response.json()

#获得关注数页面
def get_follow_num_page():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36'
    }
    url_follow_num = 'https://www.zhihu.com/api/v4/questions/35953016/followers?include=data%5B*%5D.gender%2Canswer_count%2Carticles_count%2Cfollower_count%2Cis_following%2Cis_followed&limit=10&offset=0'
    response = requests.get(url_follow_num, headers=header)
    return response.json()


def get_page(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36 '
    }
    response = requests.get(url, headers=header)
    return response.json()


def get_page_num(url_follow_num):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36 '
    }
    response = requests.get(url_follow_num, headers=header)
    return response.json()


def parse_follow_num(html_follow_num):
    global question_follow_num
    items_follow_nums = html_follow_num['paging']
    question_follow_num = items_follow_nums['totals']


# 解析函数
def parse(html):
    items = html['data']

    for item in items:
        search_terms = '面试'
        question_url = item['question']['url']
        title = item['question']['title']
        name = item['author']['name']
        id = item['id']
        # follower_count = item['author']['follower_count']
        comment_count = item['comment_count']
        url_token = item['author']['url_token']
        url = 'https://www.zhihu.com/api/v4/members/' + str(url_token) + '/followees?include=data%5B*%5D.answer_count' \
                                                                         '%2Carticles_count%2Cgender%2Cfollower_count' \
                                                                         '%2Cis_followed%2Cis_following%2Cbadge%5B%3F(' \
                                                                         'type%3Dbest_answerer)%5D.topics&offset=0' \
                                                                         '&limit=20 '
        info = {
            'search_terms': search_terms,
            'question_follow_num': question_follow_num,
            'search_rank': items.index(item),
            'question_url': question_url,
            'question_title': title,
            'question_top_answer_username': name,
            # 'follower_count': follower_count,
            'question_top_answer_id': id,
        }
        print('search_terms:', search_terms)
        print('search_rank:', items.index(item))
        print('question_url:', question_url)
        print('question_title:', title)
        print('question_follow_num', question_follow_num)
        print('question_top_answer_username:', name)
        # print('follower_count:', follower_count)
        print('question_top_answer_id:', id)
        print('-' * 20)
        url_list.append(url)
        # 存入数据库
        save_to_mongo(info)


# 连接到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'zhihu_user_network'
MONGO_COLLECTION = 'users_info'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]


def save_to_mongo(info):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(info):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


# url列表
url_list = []

if __name__ == '__main__':
    html_follow_num = get_follow_num_page()
    parse_follow_num(html_follow_num)
    html = get_first_page()
    parse(html)
    for url in url_list:
        if url in range(1):
            try:
                html_next = get_page(url)
                parse(html_next)
                time.sleep(2)
            except OSError:
                pass
            continue
        else:
            break
