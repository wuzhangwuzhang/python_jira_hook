import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

ChromedriverPath = r'D:\Tools\chromedriver_win32\chromedriver.exe'
JiraLoginJsp = 'https://jira-pro.uuzu.com/secure/Dashboard.jspa'
driver = None


# 方式一
s = Service(executable_path=ChromedriverPath)
driver = webdriver.Chrome(service=s)

driver.get(JiraLoginJsp)

_input = driver.find_element(By.XPATH, '//*[@id="login-form-username"]')
_input.send_keys('zhwu')

_input = driver.find_element(By.XPATH, '//*[@id="login-form-password"]')
_input.send_keys('Wz147258')

time.sleep(1)
# _input.send_keys(Keys.ENTER)
driver.find_element(By.ID, 'login').click()
print(driver.get_cookies())

time.sleep(2)
# 我的bug单列表
div_list = driver.find_element(By.CSS_SELECTOR,
                               '#gadget-10002 > div > div > issuetable-web-component > table > tbody')
print(div_list.text.split("\n"))

# 模拟jria单号查询
findIndex = 0

search_input = driver.find_element(By.ID, 'quickSearchInput')
search_input.clear()
search_input.send_keys('SLPK-192221')
time.sleep(1)

# jria单号查询结果
result = driver.find_element(By.CSS_SELECTOR,
                             '#quicksearch > div.quicksearch-dropdown > div:nth-child(1) > ul > li')
findIndex = result.text.find("SLPK")
print(result.text, findIndex)

# 再次查询下
time.sleep(1)
search_input.clear()
search_input.send_keys('SLPK-19222')
time.sleep(1)

# 获取查询结果
result = driver.find_element(By.CSS_SELECTOR,
                             '#quicksearch > div.quicksearch-dropdown > div:nth-child(1) > ul > li')
resultStr = result.text.replace("\n", "")

# 查询结果里是否有SLPK关键字
findIndex = resultStr.find("SLPK")
print(resultStr, findIndex)

# 模拟进入查询到的单号详情
time.sleep(1)
driver.find_element(By.CSS_SELECTOR,
                    '#quicksearch > div.quicksearch-dropdown > div:nth-child(1) > ul > li:nth-child(2) > a > span.quick-search-item-title').click()

# 获取该单号的所属版本
time.sleep(1)
if findIndex > 0:
    version = driver.find_element(By.CSS_SELECTOR, '#fixVersions-field > a')
    print(version.text)
time.sleep(6)
driver.close()
