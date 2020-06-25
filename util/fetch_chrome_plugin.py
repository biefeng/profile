# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/14 10:48
# file_name : fetch_chrome_plugin.py

import csv
import datetime
import io
import json
import os

import pymysql
import requests

from app.baidu_obs import bos_client, GENIOUS_BUCKET, md5_file, md5_obj
from util.MysqlUtil import Import

login_info = {
    "login": "biefeng6@gmail.com",
    "t": "AHUv8HGOzaKV-HYwj4U1lNAXr3McNfUGbw:1592218704450"
}

categories = ['collection/editors_picks_extensions', 'recommended_extensions']

today = datetime.date.today()
date_prefix = "{0}-{1}-{2}".format(today.year, today.month, today.day)
chrome_data_dir = "D:\\Download\\chromePlugin\\{0}\\".format(date_prefix)
if not os.path.exists(chrome_data_dir):
    os.mkdir(chrome_data_dir)


def fetch_plugin_info_into_file():
    url = "https://chrome.google.com/webstore/ajax/item?hl=zh-CN&gl=JP&pv=20200420&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Chap%2Cnma%2Cdpb%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Cmac%2Cepb%2Cfcf%2Crma%2Cpot%2Cevt&count=200&token=225@758604&category=extensions&sortBy=0&container=CHROME&features=5&_reqid=1340884&rt=j"

    payload = "login=biefeng6%40gmail.com&t=AHUv8HFZ99MAXKSyy3hinr6GzvdR3dYq4A%3A1592658971409&"
    headers = {
        'authority': 'chrome.google.com',
        'x-same-domain': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://chrome.google.com',
        'x-client-data': 'CI62yQEIpbbJAQjEtskBCKmdygEYm77KARiAv8oB',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://chrome.google.com/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'ANID=AHWqTUmhsPFfP5pos-5AqVvBZugFEgrv7YNCQp5C7Jzw9TYscKQTzUmn2EPpQC0D; SID=xwfxZdPhUjPqWljFqcHP5kZ4Mxka2cSG5cfcJajlt9UKj0gOKyvptdgSiIjGKy3o76ZP6g.; __Secure-3PSID=xwfxZdPhUjPqWljFqcHP5kZ4Mxka2cSG5cfcJajlt9UKj0gO1XuRH06_D4sLDu8Ls62hyw.; HSID=AXJ-3nljB9GXLEu6W; SSID=AeBSiWKGcAZ8adS51; APISID=ZeTbkaSeQFhQ-_ag/AloYOr7XCpCE5nLU-; SAPISID=-7I1uSrR_xJanry2/ATxMaK0_xiB60pHUV; __Secure-HSID=AXJ-3nljB9GXLEu6W; __Secure-SSID=AeBSiWKGcAZ8adS51; __Secure-APISID=ZeTbkaSeQFhQ-_ag/AloYOr7XCpCE5nLU-; __Secure-3PAPISID=-7I1uSrR_xJanry2/ATxMaK0_xiB60pHUV; __utmc=73091649; SEARCH_SAMESITE=CgQI_Y8B; NID=204=i3480g6BOpvnAr942iOxxPRa8w93pxosNFKvLLfCtEsE6EdmMWlNWG1U-ocyd9iOuAf6Wgn-gwzjZj024iGsLbSUjcTQoezRZEx1l7zJglhMskDhFbTY4QV49ms7wDZvEgDppe2wWEICfrvNTkuZ6xBg8mYPLNHMb30YYYFHgFxefzDUeatwmGfjuXfOpHvr6eYK59f7RhrUJ60xN22HCVnLYAIPqBOoUIjXFuzz; 1P_JAR=2020-06-20-06; __utma=73091649.1825346260.1591807403.1592651305.1592658668.11; __utmz=73091649.1592658668.11.7.utmcsr=chrome-ntp-icon|utmccn=(not%20set)|utmcmd=(not%20set); __utmt=1; __utmb=73091649.67.9.1592659036572; SIDCC=AJi4QfF9WhaR3xi0LU4PJzqZ2T-jPnjNXm6rI08p0LblPiPZEtxqX6we2F-pdfmGOzMbMjdeHYQ; SIDCC=AJi4QfGf1nXmdLP-kkfxOUaJt5pLk-SYlXSQ_NliPkKwSgr8aJ2ZSA_v713lojDAmUawvcNV92Y'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data_str = response.text.encode("utf-8").replace(b"\n", b"")[4:].decode("utf-8").replace("null", "\"null\"")
    # print(dataStr)
    data = (json.loads(data_str))

    with open(chrome_data_dir + 'chrome_plugin.csv', mode="w", encoding='utf-8') as sql_file:
        writer = csv.DictWriter(sql_file, fieldnames=['plugin_id', 'name', 'short_desc', 'description', 'cover_image'], delimiter=r" ")
        writer.writeheader()
        for i in data[0][1][1]:
            print(i[0] + ": " + i[1] + " " + i[6])
            detail_url = "https://chrome.google.com/webstore/ajax/detail?hl=zh-CN&gl=SG&pv=20200420&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Chap%2Cnma%2Cdpb%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Cmac%2Cepb%2Cfcf%2Crma&id={0}&container=CHROME&_reqid=177793&rt=j".format(
                i[0])
            # print(detail_url)
            detail_res = requests.post(detail_url, data=payload)
            detail = json.loads(detail_res.text[4:])
            # print(detail[0][1][1][1])
            plugin_data = {
                'plugin_id': i[0],
                'name': i[1],
                'cover_image': i[len(i) - 10],
                'short_desc': i[6],
                'description': detail[0][1][1][1]
            }
            # sql = "insert into chrome_plugin (name,short_desc,description) values ('{0}','{1}','{2}');".format(i[1], i[6], detail[0][1][1][1])
            # print("update chrome_plugin set cover_image='{0}' where plugin_id='{1}';".format(plugin_data['cover_image'], plugin_data['plugin_id']))
            # print(plugin_data)
            # 先校验是否已上传过，即在文件服务器重复，如果重复，代表已经下载过该插件并插入到数据库
            fn = i[1] + ".crx"
            if not (file_exists(fn)):
                writer.writerow(plugin_data)
            else:
                print("{0} was duplicated".format(fn))
                continue
            download_crx(i[0], i[1])

            # break


def insert_plugin_info_into_mysql():
    connect = pymysql.connect(host="106.13.83.252", user='root', db='blog_mini', passwd='Biefeng123!')
    cursor = connect.cursor()

    with open(chrome_data_dir + 'chrome_plugin.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=' ')
        for row in reader:
            plugin_data = [
                row['name'],
                row['short_desc'],
                datetime.datetime.now(),
                datetime.datetime.now(),
                row['description']
            ]
            sql = "insert into chrome_plugin (name,short_desc,create_time,update_time,description) values (%s,%s,%s,%s,%s)"
            cursor.execute(sql, plugin_data)

    connect.commit()


def download_crx(id, name):
    fn = name + ".crx"
    crx_name = chrome_data_dir + id + ".crx"
    if os.path.exists(crx_name):
        print("{0} was downloaded ".format(fn))
        return
    url = "https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x64&os_arch=x86_64&nacl_a" \
          "rch=x86-64&prod=chromecrx&prodchannel=&prodversion=83.0.4103.97&lang=zh-CN&acceptformat=crx3&x=id%3D{0}%26installsource%3Dondemand%26uc".format(
        id)
    s = requests.session()

    s.keep_alive = False
    payload = {}
    headers = {
        # 'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'X-Client-Data': 'CI62yQEIpbbJAQjEtskBCKmdygEYm77KAQ==',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'ANID=AHWqTUmhsPFfP5pos-5AqVvBZugFEgrv7YNCQp5C7Jzw9TYscKQTzUmn2EPpQC0D; SID=xwfxZdPhUjPqWljFqcHP5kZ4Mxka2cSG5cfcJajlt9UKj0gOKyvptdgSiIjGKy3o76ZP6g.; __Secure-3PSID=xwfxZdPhUjPqWljFqcHP5kZ4Mxka2cSG5cfcJajlt9UKj0gO1XuRH06_D4sLDu8Ls62hyw.; HSID=AXJ-3nljB9GXLEu6W; SSID=AeBSiWKGcAZ8adS51; APISID=ZeTbkaSeQFhQ-_ag/AloYOr7XCpCE5nLU-; SAPISID=-7I1uSrR_xJanry2/ATxMaK0_xiB60pHUV; __Secure-HSID=AXJ-3nljB9GXLEu6W; __Secure-SSID=AeBSiWKGcAZ8adS51; __Secure-APISID=ZeTbkaSeQFhQ-_ag/AloYOr7XCpCE5nLU-; __Secure-3PAPISID=-7I1uSrR_xJanry2/ATxMaK0_xiB60pHUV; SEARCH_SAMESITE=CgQI-I8B; NID=204=aO8ahavbzR4kfQLxTqCCBheqrJi6alg1CvwjC0qxSP0gY7yrAggb6R_fSuHTSRj7RxxopR2720qQhTjH3eiceWR_Q51Okhp3WD7tDgY_oLFWgxUSlu_ujM310s3TfBJeehnBuSX0qed2P5h914tBdG-W65lgwb_Vl33IJz42y5RlL25TGO4ViIyz-JnLmkoRAu-rAbJ9zl3Oj3TEIfdl-sv20M1LvGqcy4Jmp4GG; 1P_JAR=2020-6-15-7; SIDCC=AJi4QfFwFtK3YK1W4ZA2-MHUimwWsLBePsEJ4ytg_m2LxCXG7RfjFuIm3iinCGJeFUes-ixHI3M; SIDCC=AJi4QfGiX-IvK-ndyoj6oc-acrm030PE1PwQn_zdRu_8TYB5RKXSul_uR17kefmO3ShO8TJID3E'
    }
    # print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    content = response.content

    with open(crx_name, mode='wb') as crx_file:
        crx_file.write(content)
        crx_file.flush()
    # upload_crx_to_baidu_obs(name + ".crx", content)


def upload_crx_to_baidu_obs():
    with open(chrome_data_dir + "chrome_plugin.csv", mode='r', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=r" ")

        rows = []
        index = 1
        for row in reader:
            upload_name = row['name'] + ".crx"
            upload_name = upload_name.replace("/", "")
            fn = chrome_data_dir + row['plugin_id'] + ".crx"
            key = "chrome/crx/{0}/{1}".format(date_prefix, upload_name)
            # print(index)
            index += 1
            url = bos_client.generate_pre_signed_url(bucket_name=GENIOUS_BUCKET, key=key, expiration_in_seconds=-1)
            row['crx_url'] = url.decode("utf-8")
            rows.append(row)
            if file_exists(upload_name):
                print("{0} exists".format(upload_name))
                continue
            with open(fn, mode='rb') as file_data:
                if os.path.getsize(fn) > 25 * 1024 * 1024:
                    fs = os.path.getsize(fn) / (1024 * 1024)
                    print("multipart upload {0},it's size is {1}M".format(upload_name, str(fs)))
                    multipart_upload(fn, key)
                else:
                    print("common upload {0}".format(upload_name))
                    bos_client.put_object(GENIOUS_BUCKET, key, file_data, os.path.getsize(fn), md5_file(fn))

                # print(url)
                # break
        with open(chrome_data_dir + "chrome_plugin_url.csv", mode="w", encoding="utf-8") as url_file:
            writer = csv.DictWriter(url_file, fieldnames=['plugin_id', 'name', 'short_desc', 'description', 'cover_image', "crx_url"], delimiter=r" ")
            writer.writeheader()
            writer.writerows(rows)


def multipart_upload(fn, key):
    upload_id = bos_client.initiate_multipart_upload(GENIOUS_BUCKET, key).upload_id
    left_size = os.path.getsize(fn)
    # left_size用于设置分块开始位置
    # 设置分块的开始偏移位置
    offset = 0

    part_number = 1
    part_list = []
    index = 0
    while left_size > 0:
        # 设置每块为5MB
        part_size = 5 * 1024 * 1024
        if left_size < part_size:
            part_size = left_size

        response = bos_client.upload_part_from_file(
            GENIOUS_BUCKET, key, upload_id, part_number, part_size, fn, offset)
        index += 1
        print(index)
        left_size -= part_size
        offset += part_size
        part_list.append({
            "partNumber": part_number,
            "eTag": response.metadata.etag
        })

        part_number += 1
    location = bos_client.complete_multipart_upload(GENIOUS_BUCKET, key, upload_id, part_list)
    print(location.location)
    return location



def replace_image_url():
    im = Import("baiduyun", "blog_mini", "root", "Biefeng123!")
    select = im.select("select plugin_id ,cover_image from chrome_plugin")
    sql = "update chrome_plugin set  cover_image='{0}' where plugin_id='{1}'"
    with open(chrome_data_dir + "chrome_plugin_url.csv", mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=" ")
        index = 1
        # print(len(select))
        for row in reader:
            print(index)
            index += 1

            try:
                if row['cover_image'] is None or row['cover_image'] == 'null':
                    continue
                img_res = requests.get(row['cover_image'])
                content = img_res.content
                fn = date_prefix + "/" + row['plugin_id'] + "_main.png"
                key = "chrome/image/" + fn
                if not file_exists(row['plugin_id'] + "_main.png"):
                    bos_client.put_object(GENIOUS_BUCKET, key, io.BytesIO(content), len(content), md5_obj(content))
                url = bos_client.generate_pre_signed_url(bucket_name=GENIOUS_BUCKET, key=key, expiration_in_seconds=-1)
                sql_format = sql.format(url.decode("utf-8"), row['plugin_id'])

                im.update(sql_format)
            except Exception as e:
                print(row['plugin_id'] + " replace failed")

def list_uploaded_objects():
    response = bos_client.list_objects(GENIOUS_BUCKET)
    keys = []
    for object in response.contents:
        keys.append(object.key)
    return keys


def file_exists(fn):
    """
    :arg 文件名是否存在
    :return 如果文件存在，返回文件url,否则返回None
    """
    keys = list_uploaded_objects()
    for key in keys:
        slash_index = key.rfind("/")
        if slash_index > 0:
            file_name = key[slash_index + 1:]
            if file_name == fn:
                url = bos_client.generate_pre_signed_url(bucket_name=GENIOUS_BUCKET, key=key, expiration_in_seconds=-1)
                return url.decode("utf-8")
            return None


if __name__ == '__main__':
    fetch_plugin_info_into_file()
    im = Import("baiduyun", "blog_mini", "root", "Biefeng123!")
    upload_crx_to_baidu_obs()
    im.import_csv(chrome_data_dir + "chrome_plugin_url.csv", "chrome_plugin")
    replace_image_url()

    # multipart_upload("D:\\Download\\chromePlugin\\2020-6-20\\emffkefkbkpkgpdeeooapgaicgmcbolj.crx", "chrome/crx/{0}/{1}.crx".format(date_prefix, "Wikiwand: Wikipedia Modernized"))
    # list_uploaded_objects()
    # print(file_exists("新的兰博基尼卡和壁纸收集.crx"))
