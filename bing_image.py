# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
from urllib.parse import urljoin

import requests


def get_bing_image():
    url = 'https://cn.bing.com'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36'
    }

    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding

    ret = re.search("var _model =(\{.*?\});", res.text)
    if not ret:
        return

    data = json.loads(ret.group(1))
    image_content = data['MediaContents'][0]['ImageContent']
    ssd = data['MediaContents'][0]['Ssd']
    # video_content = data['MediaContents'][0]['VideoContent']
    # audio_content = data['MediaContents'][0]['AudioContent']

    return {
        'title': image_content['Title'],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'copyright': image_content['Copyright'],
        'description': image_content['Description'],
        'headline': image_content['Headline'],
        'quickFact': image_content['QuickFact']['MainText'],
        'imageUrl': urljoin(url, image_content['Image']['Url']),
        'ssd': ssd,
    }


if __name__ == '__main__':
    res = get_bing_image()
    print(json.dumps(res, ensure_ascii=False, indent=2))
