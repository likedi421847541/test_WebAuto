# -*- coding:utf-8 -*-
# 主要对目前常用的 Chrome，Firefox ,IE 三大浏览器引擎的二次封装
import configparser   #configparser 读取配置文件
import os.path
from  selenium import webdriver
from framework.logger import Logger
logger = Logger()

class BrowserEngine():
    dir = os.path.dirname(os.path.realpath(__file__))
    dir = os.path.dirname(os.path.realpath(dir))
    print(dir)
    chrome_driver_path = dir + r'\tools\chromedriver.exe'
    print(chrome_driver_path)
    ie_driver_path = dir +r'\tools\IEDriverServer.exe'

    # def __init__(self,driver):
    #     self.driver = driver
    # 从配置文件中读取浏览器类型
    def open_browser(self):
        config = configparser.ConfigParser()
        #file_path1 = os.path.dirname(os.path.abspath('.'))+r'\config\config.ini'
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.dirname(os.path.realpath(file_path))
        file_path = os.path.join(file_path,'config\config.ini')
        #print(file_path)
        config.read(file_path,encoding='utf-8')  # 读取config配置文件

        browser = config.get("browserType",'browserName')  # 获取浏览器类型，名字
        logger.info('您已经选择{}浏览器'.format(browser))  # 日志打印你选择的浏览器类型
        url = config.get('testServer','URL')  # 获取测试的 URL 地址
        logger.info('您即将测试的网站是{}'.format(url))

        # 判断你选择的浏览器
        if browser == 'Firefox':
            self.driver = webdriver.Firefox()
            logger.info('开始火狐浏览器')
        elif browser == 'Chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('lang=EN')  # 设置浏览器默认语言为英文
            logger.info('打开谷歌浏览器')
            self.driver = webdriver.Chrome(self.chrome_driver_path,options= chrome_options) # 初始化一个实例
        elif browser == 'IE':
            self.driver = webdriver.Ie(self.ie_driver_path)
            logger.info('开始 IE 浏览器')
        self.driver.get(url)   # 访问 url
        logger.info('打开网站: {}'.format(url))
        #self.driver.maximize_window() # 窗口放大
        #driver.implicitly_wait(10)
        # print(driver)
        return self.driver
    def quit_browser(self):
        logger.info('现在，关闭浏览器')
        self.driver.quit()

