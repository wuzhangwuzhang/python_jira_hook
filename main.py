# from selenium import webdriver
#
# driver = webdriver.Chrome()
# driver.get("https://jira-pro.uuzu.com/")
# driver.implicitly_wait(5)

# _*_coding:utf-8_*_
import time
from selenium.webdriver.common.keys import Keys  # 模仿键盘,操作下拉框的
from selenium import webdriver  # selenium驱动
from selenium.webdriver.support.wait import WebDriverWait  # 导入等待类
from selenium.webdriver.support import expected_conditions as EC  # 等待条件
from selenium.webdriver.common.by import By  # 节点定位


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

def test_open():
    print("—————————— open ——————————")
    # 方式一：默认打开浏览器驱动
    driver = webdriver.Chrome()
    # 方式二：通过设置参数，不打开浏览器
    # driver = webdriver.Chrome(options=add_options())
    driver.get('https://www.jd.com/')
    driver.implicitly_wait(5)
    # 找到id=key的标签
    _input = driver.find_element(By.ID, 'key')
    # 输入内容，查询商品信息
    _input.send_keys('iphone14')
    time.sleep(1)
    _input.clear()
    time.sleep(1)
    _input.send_keys('华为mate50pro')
    time.sleep(1)
    _input.send_keys(Keys.ENTER)
    # 触发点击事件的两种方式：1.调用键盘回车键；2.触发按钮的click事件
    # driver.find_element(By.CLASS_NAME, 'button.cw-icon').click()
    # 等待商品列表加载
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.ID, "J_goodsList")))
    # 滚动到页面底部
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    # 滚动到页面顶部
    driver.execute_script('window.scrollTo(0,0)')
    time.sleep(1)
    # 打印看看商品信息
    list = driver.find_elements(By.CLASS_NAME, "gl-item")
    for item in list:
        print(item.text)
    driver.close()
    pass


if __name__ == "__main__":
    test_open()
    print("—————————— end ——————————")