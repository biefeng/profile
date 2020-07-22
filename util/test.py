import requests

url = "http://chrome.google.com/webstore/ajax/item?hl=zh-CN&gl=PH&pv=20200420&mce=atf%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Chap%2Cnma%2Cdpb%2Car2%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Chsf%2Cmac%2Cepb%2Cfcf%2Crma%2Cigb%2Cpot%2Cevt%2Cbem%2Crae%2Cshr%2Cesl&requestedCounts=featured%3A7%3A10%3Afalse%2Cmcol%23top_picks_web-development%3A11%3A1%3Atrue&category=ext%2F11-web-development&_reqid=640825&rt=j"

proxies = {'http': 'socks5://127.0.0.1:1080',
           'https': 'socks5://127.0.0.1:1080'
           }

payload = "login=biefeng6%40gmail.com&f.req=%5B%5B%5B%22featured%22%2C7%2C10%2Cfalse%5D%2C%5B%22mcol%23top_picks_web-development%22%2C11%2C1%2Ctrue%5D%5D%2C%22ext%2F11-web-development%22%5D&t=AHUv8HGU0VSHaV2QDIGeZHkYIv362ngCXQ%3A1595388022735&"
headers = {
    'authority': 'chrome.google.com',
    'x-same-domain': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://chrome.google.com',
    'x-client-data': 'CI62yQEIpbbJAQjEtskBCKmdygEI/7zKAQjnyMoBCLTLygE=',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://chrome.google.com/',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'HSID=AXJ-3nljB9GXLEu6W; SSID=AeBSiWKGcAZ8adS51; APISID=ZeTbkaSeQFhQ-_ag/AloYOr7XCpCE5nLU-; SAPISID=-7I1uSrR_xJanry2/ATxMaK0_xiB60pHUV; __Secure-HSID=AXJ-3nljB9GXLEu6W; __Secure-SSID=AeBSiWKGcAZ8adS51; __Secure-APISID=ZeTbkaSeQFhQ-_ag/AloYOr7XCpCE5nLU-; __Secure-3PAPISID=-7I1uSrR_xJanry2/ATxMaK0_xiB60pHUV; __utmc=73091649; S=billing-ui-v3=WwnapRklvZ7NW5iQAxTZ4Y0uMfR0F5xJ:billing-ui-v3-efe=WwnapRklvZ7NW5iQAxTZ4Y0uMfR0F5xJ; _ga=GA1.3.1825346260.1591807403; ANID=AHWqTUnowf0cwa_ohB-1w1227HeKihToFIyGf4zRaSsFbOobZG0XtHxHA6-6RI78; SID=zAfxZcVBbGPr8aW9V_x06GMLIXACHg7bZJ3mxKNbPxw1hoQq4Xbj8VHGYqw5onBUeQcSGg.; __Secure-3PSID=zAfxZcVBbGPr8aW9V_x06GMLIXACHg7bZJ3mxKNbPxw1hoQq_9-GN71mhPowQXpidpUSXw.; SEARCH_SAMESITE=CgQIoJAB; NID=204=DAw1tYMUHj2IzEQgxT9b5hUV4iQO-OW4fLqdSRt8M3UxkaGnUP0p7jb-Ofzd2i8h1lDK2qNNkfZNFYsBb1SwMjQJkCv_jo6J7BMFDKplRwm6qLc2W8M2W_kNGNFISWkP8fddDa-1SbFKbNx-8BlgY4PZOMPT8zsel1JG2n_6SI7l2eU-u4CQ0DY9o3N9RYRyRrMZ9Wp9MpuQEmJchlSj0qgyZJy7r00QdOAMozpJ; 1P_JAR=2020-7-22-3; __utma=73091649.1825346260.1591807403.1595384110.1595387122.31; __utmz=73091649.1595387122.31.20.utmcsr=chrome-ntp-icon|utmccn=(not%20set)|utmcmd=(not%20set); __utmt=1; SIDCC=AJi4QfE84645i-N1GuPyiUonYtQL838HTwFgMhtUg26Wl51e5_Z3-_QkRkHZPPoZd1VuKsu484s; __utmb=73091649.41.7.1595388034379; SIDCC=AJi4QfE-DBomdrnYG1hbmbth27OExEdE00Vk4m4oAKXwI9dbOnMNbIUKjv57aaruPKt0ebZXs3M'
}

response = requests.request("POST", url, headers=headers, data=payload,proxies=proxies)

print(response.text.encode('utf8'))
