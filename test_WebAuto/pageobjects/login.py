# -*- coding:utf-8 -*-
'''
登录页面中，主要是元素定位和页面操作写成函数，供测试类调用
'''
from selenium import webdriver
from framework.base import Base
class LoginPage(Base): # 继承 Base 类，可直接调用Base 中的方法
    email_locator = ('id','userEmail')
    pwd_locator = ('id','userPassword')
    submit_locator = ('id','btnLogin')
    keepLogin_locator = ('xpath',"//span[@translate='keepMe']")  # 保持登录定位
    empty_email_locator = ('id','emailEmpty')
    def input_email(self,email):  #输入邮箱
        self.sendKeys(self.email_locator,email)
    def input_pwd(self,pwd):  #输入密码
        self.sendKeys(self.pwd_locator,pwd)
    def click_submit(self):  #点击登录
        self.click(self.submit_locator)
    def click_keepLogin_pwd(self):  #点击保持登录
        self.click(self.keepLogin_locator)
    # 以下都是为了断言
    def get_emptyEmail_message(self):
        error_message = self.get_text(self.empty_email_locator)
        return error_message
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://web.learning-genie.com/#/login')
    lg = LoginPage(driver)
    #lg.keepLogin_pwd()
    driver.quit()