import cv2
import os
import numpy as np
from paddleocr import PaddleOCR
'''------------------------------------------'''
import re
import requests
import random
import json
from hashlib import md5
import time
# 使用前阅读 Readme 中的 Translate paddleOCR's content
appid = '20...'
appkey = 'iL...'

from_lang = 'zh'
to_lang = 'en'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

def contains_chinese(text):
    # 使用正则表达式检查文本中是否包含中文字符
    return re.search('[\u4e00-\u9fff]', text) is not None

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def translate(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    if 'trans_result' in result:
        return result['trans_result'][0]['dst']
    else:
        print(f"Error: {result}")
        return query  # 返回原始文本以防出错

image_path = "../data"
output_path = '../output/'
all_imgs = os.listdir(image_path)

ocr = PaddleOCR(use_angle_cls=True, lang='ch')
print(all_imgs)

for img in all_imgs:
    # 读取图片并进行 OCR 识别
    this = os.path.join(image_path, img)
    image = cv2.imread(this)
    result = ocr.ocr(this, cls=True)

    # 获取原图尺寸
    original_height, original_width = image.shape[:2]

    # 设置新图像尺寸，增加一定的边距
    margin = 100
    new_height = original_height + 2 * margin
    new_width = 2 * original_width + 2 * margin
    new_image = np.ones((new_height, new_width, 3), dtype=np.uint8) * 255  # 创建白色背景的新图像

    # 绘制识别到的文本
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            box = line[0]
            text = line[1][0]
            
            # 确保text是字符串
            if not isinstance(text, str):
                text = str(text)
            
            # 计算文本框的中心点
            x_min = min(box[0][0], box[1][0], box[2][0], box[3][0])
            y_min = min(box[0][1], box[1][1], box[2][1], box[3][1])
            x_max = max(box[0][0], box[1][0], box[2][0], box[3][0])
            y_max = max(box[0][1], box[1][1], box[2][1], box[3][1])
            
            # 计算新的文本位置，增加额外的间距
            text_position = (int(x_min)* 2 + margin, int(y_min) + margin)
            # text_position = (int(x_min) + margin, int(y_min) + margin)
            
            # 检查文本是否包含中文字符
            if contains_chinese(text):
                time.sleep(1)
                text = translate(text)
            
            # 绘制识别到的文本
            cv2.putText(new_image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # 保存结果图像
    respath = os.path.join(output_path, img)
    cv2.imwrite(respath, new_image)
    print('save: ', respath)
    # break
