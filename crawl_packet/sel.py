import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()

driver.implicitly_wait(10)

# 打开网页
driver.get("https://www.bilibili.com/")

ele_list = driver.find_elements(By.XPATH, '//div[@class="channel-items__left"]/a[@class="channel-link"]')

for element in ele_list:
    url_ele = element.get_attribute('href')

    element.click()

    driver.refresh()

    ele_part = driver.find_elements(By.XPATH, '//div[@class="home-recommand-feed-body"]/div')





driver.quit()
