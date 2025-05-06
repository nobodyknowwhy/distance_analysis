import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()

driver.implicitly_wait(10)

# 打开网页
driver.get("https://www.baidu.com")

element = driver.find_element(By.ID, 'kw')

element.send_keys('python')

driver.find_element(By.XPATH, '//input[@id="su"]').click()

time.sleep(5)

driver.quit()
