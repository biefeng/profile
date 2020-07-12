#!usr/bin/env python
# -*- coding: utf-8 -*-
# fileName: test.py.py
# time: 2020/07/08 21:58

__author__ = '33504'

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

options = webdriver.ChromeOptions();
options = webdriver.ChromeOptions();
options.add_argument("--auto-open-devtools-for-tabs");

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
browser = webdriver.Chrome(options=options, desired_capabilities=caps)
url = 'https:www.baidu.com'
browser.get(url)
time.sleep(2)
for entry in browser.get_log('performance'):
	print(entry)

