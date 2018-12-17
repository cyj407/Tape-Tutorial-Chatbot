import re
import requests
import jieba
import jieba.analyse

from seg import seg_word

def getHotKey():
    url_list = ['https://www.youtube.com/results?search_query=%E8%B2%BC%E7%B4%AE',
                'https://www.youtube.com/results?search_query=%E8%82%8C%E5%85%A7%E6%95%88',
                'https://www.youtube.com/results?search_query=%E8%82%8C%E8%B2%BC',
                'https://www.youtube.com/results?search_query=%E9%81%8B%E5%8B%95%E8%B2%BC%E7%B4%AE',
                'https://www.youtube.com/results?search_query=%E8%82%8C%E8%B2%BC&sp=CAM%253D']

    result = []
    for i in url_list:
        html = requests.get(i, timeout=30)
        m = re.compile('<span aria-label="(.*?) 上傳者')
        result = result + m.findall(html.text)

    tags = []
    sum_of_tags = {}
    for idx in result:
        tmp = jieba.analyse.extract_tags(idx, topK=5)
        tags = tags + tmp
        for j in tmp:
            if(tags.count(j) != 0):
                sum_of_tags[j] = tags.count(j) + 1
            else:
                sum_of_tags[j] = 1

    sorted_tags = sorted(sum_of_tags.items(), key=lambda kv: kv[1], reverse=True) 

    hotKey = []
    cnt = 0
    for (key, freq) in sorted_tags:
        if(cnt >= 3):
            break
        if(key == '腳踝' or key == '膝蓋' or key == '手腕' \
            or key == 'Shoulder' or key == '足底' or key == 'Knee'\
            or key == '肩膀' or key == '小腿' or key == '網球肘' or key == '手指'\
            or key == '肩部'):
                cnt = cnt + 1
                hotKey.append(key)

    return hotKey