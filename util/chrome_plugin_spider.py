# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/23 11:46
# file_name : chrome_plugin_spider.py


import csv
import datetime
import json
import logging
import os

import requests

from app.baidu_obs import BaiduBos, GENIOUS_BUCKET
from util.MysqlUtil import Import

# from app.baidu_obs import file_exists

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

today = datetime.date.today()
date_prefix = "{0}-{1}-{2}".format(today.year, today.month, today.day)
# date_prefix = "{0}-{1}-{2}".format(today.year, today.month, 10)

base_word_dir = "D:\\Download\\chromePlugin\\"

# chrome_data_dir = "D:\\Download\\chromePlugin\\{0}\\".format(date_prefix)

plugin_cover_image_base_dir = base_word_dir + "image\\"

plugin_crx_base_dir = base_word_dir + "crx\\"

download_csv_file = base_word_dir + "chrome_plugin_downloaded_{0}.csv".format(date_prefix)
upload_csv_file = base_word_dir + "chrome_plugin_uploaded_{0}.csv".format(date_prefix)

image_file_suffix = "_main.png"

crx_file_suffix = ".crx"

baidu_bos_crx_key_prefix = "chrome/crx/"

baidu_bos_cover_image_key_prefix = "chrome/image/"

# if not os.path.exists(chrome_data_dir):
#     os.mkdir(chrome_data_dir)

LOGGER = logging.getLogger(__name__)


class ChromePluginSpider():
	def __init__(self, url=None):
		self.url = url
		self._baidu_bos = BaiduBos(GENIOUS_BUCKET)
		self._import = Import("baiduyun", "blog_mini", "root", "Biefeng123!")

	def get_plugins(self):
		"""
		:param igonre_exists: 是否忽略本地已存在的下载文件，如果忽略，将会记录在csv，后期插入数据库
		:return:
		"""
		LOGGER.info("===============download crx and image===============start")
		response = requests.post(self.url, headers=headers, data=payload)
		data_str = response.text.encode("utf-8").replace(b"\n", b"")[4:].decode("utf-8").replace("null", "\"null\"")
		data = (json.loads(data_str))
		self.handle_item_list_response(data)

	def handle_item_list_response(self, data):
		mark = data[0][1][0]
		if mark != 'getitemsresponse':
			return
		headers_exists = False
		if os.path.exists(download_csv_file):
			headers_exists = True
		with open(download_csv_file, mode="a", encoding='utf-8') as sql_file:
			writer = csv.DictWriter(sql_file, fieldnames=['plugin_id', 'name', 'short_desc', 'description', 'cover_image', 'crx_url'], delimiter=r" ")
			if not headers_exists:
				writer.writeheader()
			plugins = data[0][1][1]
			for i in plugins:
				plugin_id = i[0]
				name = i[1]
				short_desc = i[6]
				cover_image = i[len(i) - 10]
				try:
					if cover_image is not None and cover_image != 'null':
						requests.get(cover_image)
				except Exception as e:
					LOGGER.error("****{0}:{1}**** download image failed".format(plugin_id, name))
					continue
				detail_url = "https://chrome.google.com/webstore/ajax/detail?hl=zh-CN&gl=SG&pv=20200420&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Chap%2Cnma%2Cdpb%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Cmac%2Cepb%2Cfcf%2Crma&id={0}&container=CHROME&_reqid=177793&rt=j".format(
					plugin_id)
				detail_res = requests.post(detail_url, data=payload)
				detail = json.loads(detail_res.text[4:])
				# print(detail[0][1][1][1])
				plugin_data = {
					'plugin_id': plugin_id,
					'name': name,
					'cover_image': i[len(i) - 10],
					'short_desc': short_desc,
					'description': detail[0][1][1][1],

				}
				# sql = "insert into chrome_plugin (name,short_desc,description) values ('{0}','{1}','{2}');".format(i[1], i[6], detail[0][1][1][1])
				# print("update chrome_plugin set cover_image='{0}' where plugin_id='{1}';".format(plugin_data['cover_image'], plugin_data['plugin_id']))
				# print(plugin_data)
				# 先校验是否已上传过，即在文件服务器重复，如果重复，代表已经下载过该插件并上传到文件服务器，跳过下载

				result = self.download_plugin(plugin_id, name, cover_image)
				if result[0] and result[1]:
					writer.writerow(plugin_data)
				LOGGER.info("===============download crx files and images===============end")

	def download_plugin(self, plugin_id, name, cover_image):
		try:
			result = [False, False]  # 0位代表crx下载状态 1位代表cover_image下载状态
			fn = name + crx_file_suffix
			crx_file_name = plugin_id + crx_file_suffix
			crx_file_path = plugin_crx_base_dir + crx_file_name
			crx_content = None
			cover_image_content = None
			if not os.path.exists(crx_file_path):
				url = "https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x64&os_arch=x86_64&nacl_a" \
				      "rch=x86-64&prod=chromecrx&prodchannel=&prodversion=83.0.4103.97&lang=zh-CN&acceptformat=crx3&x=id%3D{0}%26installsource%3Dondemand%26uc".format(
					plugin_id)
				s = requests.session()

				s.keep_alive = False
				payload = {}
				headers = {
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
				crx_content = response.content
			else:
				result[0] = True
				LOGGER.warning("{0} has already been downloaded ".format(fn))

			image_file_name = plugin_id + image_file_suffix
			image_file_path = plugin_cover_image_base_dir + image_file_name

			if not os.path.exists(image_file_path):
				img_res = requests.get(cover_image)
				cover_image_content = img_res.content
			else:
				result[1] = True
				LOGGER.warning("{0} has already been downloaded".format(image_file_name))

			if cover_image_content is not None:
				with open(image_file_path, mode='wb') as image_file:
					image_file.write(cover_image_content)
					image_file.flush()
					result[1] = True
			if crx_content is not None:
				with open(crx_file_path, mode='wb') as crx_file:
					crx_file.write(crx_content)
					crx_file.flush()
					result[0] = True
			return result
		except Exception as e:
			LOGGER.error("{0} download failed and the plugin id is {1}.The exception message is {2}".format(name, plugin_id, e.message))
			return [False, False]

	def upload_plugins(self):
		index = 1
		plugin_ids = set()
		headers_exists = False
		if os.path.isfile(upload_csv_file):
			headers_exists = True
		with open(upload_csv_file, encoding='utf-8', mode='a') as uf:
			writer = csv.DictWriter(uf, fieldnames=['plugin_id', 'name', 'short_desc', 'description', 'cover_image', "crx_url"], delimiter=" ")
			if not headers_exists:
				writer.writeheader()
				uf.flush()
			with open(download_csv_file, encoding='utf-8', mode='r') as df:
				reader = csv.DictReader(df, delimiter=' ')

				for row in reader:
					index += 1
					plugin_id = row['plugin_id']
					name = row['name']
					plugin_ids.add(plugin_id)
					crx_local_file_name = plugin_id + crx_file_suffix
					crx_local_file_path = plugin_crx_base_dir + crx_local_file_name
					crx_upload_file_name = name + crx_file_suffix
					cover_image_file_name = plugin_id + image_file_suffix
					cover_image_file_path = plugin_cover_image_base_dir + cover_image_file_name
					try:
						crx_url = self._baidu_bos.upload_file(crx_local_file_path, baidu_bos_crx_key_prefix + crx_upload_file_name, True)
						cover_image_url = self._baidu_bos.upload_file(cover_image_file_path, baidu_bos_cover_image_key_prefix + cover_image_file_name, True)
						row['crx_url'] = crx_url
						row['cover_image'] = cover_image_url
						writer.writerow(row)
						uf.flush()
					except Exception as e:
						LOGGER.error(e)

				# self._import.import_csv_update_exists_record(upload_csv_file, "chrome_plugin", ['plugin_id'])

	def import_into_mysql_ignore_exists(self):
		self._import.import_csv_ignore_exists_record(upload_csv_file, "chrome_plugin", ['plugin_id'])

	def import_into_mysql_update_exists(self):
		self._import.import_csv_update_exists_record(upload_csv_file, "chrome_plugin", ['plugin_id'])


if __name__ == '__main__':
	spider = ChromePluginSpider(
		"https://chrome.google.com/webstore/ajax/item?hl=zh-CN&gl=JP&pv=20200420&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Chap%2Cnma%2Cdpb%2Car2%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Cmac%2Cepb%2Cfcf%2Crma%2Cpot%2Cevt&requestedCounts=infiniteWall%3A96%3A0%3Afalse&token=featured%3A0%4010785749%3A7%3Afalse%2Cmcol%23top_picks_web-development%3A0%4010785750%3A11%3Atrue%2CinfiniteWall%3A0%4010785789%3A188%3Afalse&category=ext%2F11-web-development&_reqid=1012219&rt=j")
	# spider.get_plugins()
	# spider.upload_plugins()
	spider.import_into_mysql_ignore_exists()
