# -*- coding:utf-8 -*-
import requests
import time
import json
import pymysql
import os
import logging
from PIL import Image as ImagePIL, ImageFont, ImageDraw

conn = pymysql.connect(host="127.0.0.1",
                       user="root",
                       password="password",
                       database="bing",
                       charset="utf8")
cursor = conn.cursor()
FORMAT = "%(levelname)s %(lineno)d %(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO, filename='log.log')

logging.info('当前时间：%s 程序已经执行' %
             (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ))


def addslashes(s):
    d = {'"': '\\"', "'": "\\'", "\0": "\\\0", "\\": "\\\\"}
    return ''.join(d.get(c, c) for c in s)


url = "https://cn.bing.com/HPImageArchive.aspx"
http = "https://cn.bing.com"
data = {
    'format': 'js',
    'idx': 0,
    'n': 1,
    'nc': int((time.time() * 1000)),
    'pid': 'hp'
}

headers = {
    'cookie':
    "MUID=354A50E6331566ED28CF5EE5371565E7; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=652A02AB36A24C75907C72A928513C5F&dmnchg=1; MUIDB=354A50E6331566ED28CF5EE5371565E7; SRCHUSR=DOB=20191029&T=1572412007000; _EDGE_CD=u=zh-hans; _EDGE_S=mkt=zh-cn&ui=zh-hans&SID=19DC6D3A521F6F2F0B68633F53316E9B; SNRHOP=I=&TS=; ipv6=hit=1572428982179&t=4; SRCHHPGUSR=CW=1550&CH=729&DPR=1.2395833730697632&UTC=480&WTS=63708022181; _SS=SID=19DC6D3A521F6F2F0B68633F53316E9B&HV=1572425972&bIm=_FG",
    'user-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
}

response = requests.get(url, headers=headers, params=data)

res_json = json.loads(response.text)
res_json = res_json['images']

r = requests.get(http + str(res_json[0]['url']), headers=headers)
img = str(res_json[0]['enddate']) + '.jpg'
path_url = '/data/flask_bing/App/static/images/'
if r.status_code == 200:
    with open(path_url + img, 'wb') as f:
        f.write(r.content)
    im = ImagePIL.open(path_url + img)
    im.save(path_url + img, dpi=(200.0, 200.0))
res_json = res_json[0]
sql = " insert into bingImg(copyright,copyrightlink,startdate,fullstartdate, "
sql += " enddate,hsh,url,imgUrl,http,bot,drk,title,top,wp,hs,addTime,imgName) "
sql += " values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%d,'%s',%d,'%s','%s',SYSDATE(),'%s') " % \
       (str(res_json['copyright']), str(res_json['copyrightlink']), str(res_json['startdate']),
        str(res_json['fullstartdate']), str(res_json['enddate']), str(res_json['hsh']), str(res_json['url']),
        addslashes(path_url + img), http, int(res_json['bot']), int(res_json['drk']),
        str(res_json['title']), int(res_json['top']), str(res_json['wp']), str(res_json['hs']), img)
cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()
