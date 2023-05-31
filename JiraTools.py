import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

ChromedriverPath = r'D:\Tools\chromedriver_win32\chromedriver.exe'
JiraLoginJsp = 'https://jira-pro.uuzu.com/secure/Dashboard.jspa'

def add_options():
    print("—————————— options ——————————")
    # 创建谷歌浏览器驱动参数对象
    chrome_options = webdriver.ChromeOptions()
    # 不加载图片
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # 使用无界面浏览器模式！！
    chrome_options.add_argument('--headless')
    # 使用隐身模式（无痕模式）
    chrome_options.add_argument('--incognito')
    # 禁用GPU加速
    chrome_options.add_argument('--disable-gpu')
    return chrome_options

def init_driver():
    # 方式一
    s = Service(executable_path=ChromedriverPath)
    _driver = webdriver.Chrome(service=s)

    # 方式二：通过设置参数，不打开浏览器
    # _driver = webdriver.Chrome(service=s,options=add_options())
    return _driver


def login_jira(_driver):
    _driver.get(JiraLoginJsp)
    _input = driver.find_element(By.XPATH, '//*[@id="login-form-username"]')
    _input.send_keys('zhwu')

    _input = driver.find_element(By.XPATH, '//*[@id="login-form-password"]')
    _input.send_keys('Wz147258')

    time.sleep(1)
    # _input.send_keys(Keys.ENTER)
    _driver.find_element(By.ID, 'login').click()

    #cookie缓存本地
    cookies = driver.get_cookies()  # 获取cookies
    f1 = open('cookie.txt', 'w')  # cookies存入文件JSON字符串
    f1.write(json.dumps(cookies))

def check_jira_Id(jiraId,_driver):
    version = ""
    time.sleep(1)
    # 模拟jira单号查询
    findIndex = 0
    search_input = _driver.find_element(By.ID, 'quickSearchInput')
    search_input.clear()

    # 输入jira单号
    search_input.send_keys(jiraId)
    time.sleep(0.5)

    # jira单号查询结果
    result = _driver.find_element(By.CSS_SELECTOR,'#quicksearch > div.quicksearch-dropdown > div:nth-child(1) > ul > li')
    resultStr = result.text.replace("\n", "")
    time.sleep(0.5)
    #搜索结果检查单号合法性
    findIndex = resultStr.find("SLPK")
    print(resultStr, findIndex)

    # 获取该单号的所属版本
    time.sleep(1)
    if findIndex > 0:
        # 模拟进入查询到的单号详情
        driver.find_element(By.CSS_SELECTOR,'#quicksearch > div.quicksearch-dropdown > div:nth-child(1) > ul > li:nth-child(2) > a > span.quick-search-item-title').click()
        time.sleep(1)
        version = driver.find_element(By.CSS_SELECTOR, '#fixVersions-field > a')
        print('jiraId:{0}合法,所属迭代版本:{1}'.format(jiraId,version.text))

    else:
        print('jiraId:{0}不在需求池,非法提交!'.format(jiraId))
        return


if __name__ == "__main__":
    print("—————————— start ——————————")
    driver = init_driver()
    login_jira(driver)
    check_jira_Id("SLPK-192221", driver)
    check_jira_Id("SLPK-19222",driver)
    time.sleep(3)
    print("—————————— end ——————————")