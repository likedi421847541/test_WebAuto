# -*- coding:utf-8 -*-
import time
import  os.path
from framework.logger import Logger
from selenium.webdriver.support.ui import WebDriverWait
logger = Logger()
class Base():
    '''
    对 selenium 原生的查找原生进行二次封装
    40s 内循环查找页面上有没有元素
    这样的封装的好处
    1、可以有效提高查找元素的效率，避免元素没加载完抛异常
    2、相对于 sleep 和 implicitly time 更节省时间
    3、大大减少代码重复，使用例书写更加简洁
    '''

    def __init__(self,driver):
        self.driver = driver
    def findEle(self,locator):
        '''
        定位方法参数化
        :param locator: locator 参数是定位方式，如('id','kw'),把两个参数合并成一个元组
        '''

        element = WebDriverWait(self.driver,40,0.5).until(lambda x:x.find_element(*locator))
        logger.info('已经定位到元素！')
        return element   #显示等待，在40s 内每0.5s 刷新一次，直到找到对应元素，如果找不到抛异常
    def click(self,locator):
        # 封装点击方法
        ele = self.findEle(locator)
        try:
            ele.click()
            logger.info('元素已被点击！')
        except :
            logger.error('元素点击失败！{}'.format(ele))
            self.get_windows_img()
    def sendKeys(self,locator,text,is_clear_first = False):
        '''

        :param locator:
        :param text: 需要穿入的文本
        :param is_clear_first:  根据该参数是否进行清空，默认为false，即不清除
        :return:
        '''
        ele = self.findEle(locator)
        if is_clear_first:
            ele.clear()
        try:
            ele.send_keys(text)
            logger.info('已经将{}输入文本框中'.format(text))
        except NameError as e:
            logger.error('写入文本框失败,已截图')
            self.get_windows_img()
    def clear(self,locator):
        ele = self.findEle(locator)
        try:
            ele.clear()
            logger.info('在输入文本前，先清空文本框')
        except NameError as e:
            logger.error('清空文本框失败 %s'%e)
            self.get_windows_img()

    def get_text(self,locator): #二次封装获取文本
        ele1 = self.findEle(locator)
        ele2 = ele1.text
        logger.info('{}元素的文本是{}'.format(ele1,ele2))
        return ele2
    def get_windows_img(self): #保存照片
        cur_path = os.path.dirname(os.path.realpath(__file__))
        root_path = os.path.dirname(cur_path)
        img_path = os.path.join(root_path,'ScreenShots')
        print(img_path)
        if not os.path.exists(img_path):os.mkdir(img_path)
        rq = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        screen_name  = os.path.join(img_path ,rq+ '.png')
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info('已经将截图保存在：/screenShots 文件夹')
        except NameError as e:
            logger.error('截图失败!{}'.format(e))
            self.get_windows_img()
    def error_message(self,locator):
        ele = self.findEle(locator)
        ele = ele.text
        return ele
