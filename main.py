# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime

import requests

import bing_image
from fileUtils import writeToReadme


def main():
    data = bing_image.get_bing_image()
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')

    image_folder = './images'
    image_path = date.strftime("%Y/%m/%d")

    new_folder = os.path.join(image_folder, image_path)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    # &rf=LaDigue_UHD.jpg&pid=hp&w=3840&h=2160&rs=1&c=4
    # 将图片保存到对应的日期文件夹下
    image_url = data.get('imageUrl')
    image_name = re.search(r'OHR\.(.*)\.webp', image_url).group(1) + '_' + date.strftime("%Y-%m-%d")
    image_path_webp = os.path.join(new_folder, image_name + '.webp')
    image_path_jpg = os.path.join(new_folder, image_name + '.jpg')
    with open(image_path_webp, 'wb') as webp, open(image_path_jpg, 'wb') as jpg:
        webp.write(requests.get(image_url).content)
        jpg.write(requests.get(image_url.replace('webp', 'jpg')).content)

    filename = os.path.join(new_folder, date.strftime("%Y-%m-%d") + '.json')

    with open(filename, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

    writeToReadme()
