from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
from pprint import pprint

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
time.sleep(5)
driver.set_window_size(500, 500)
time.sleep(5)
driver.set_window_size(1920, 1080)
time.sleep(5)
driver.set_window_size(1920, 2000)
driver.get("https://fwango.io/sccs/")
