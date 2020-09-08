# -*- coding:utf-8 -*-
import unittest
import time
from selenium import webdriver
from framework.browser_engine import BrowserEngine
from pageobjects.login import LoginPage
class Test(unittest.TestCase):
    browser = BrowserEngine()
    @classmethod
    def setUpClass(cls):
        driver = cls.browser.open_browser()
        cls.login = LoginPage(driver)
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit_browser()
    def tearDown(self):
        self.browser.driver.delete_all_cookies()
        self.browser.driver.refresh()
    def test_login_normal(self):  # 测试正常登陆
        self.login.input_email('421847541@qq.com')
        self.login.input_pwd('12345678q')
        self.login.click_keepLogin_pwd()
        self.login.click_submit()
        #time.sleep(3)
        # 断言
        home = self.login.get_home()
        self.assertEqual('Home',home)
    def test_login_no_email(self):  # 测试没有邮箱登录
        self.login.input_pwd('12345678q')
        self.login.click_submit()
        error_message = self.login.get_emptyEmail_message()
        self.assertEqual('email is required!',error_message)
    def test_login_no_pwd(self): # 测试没有密码登录
        self.login.input_email('421847541@qq.com')
        self.login.click_submit()
        error_message = self.login.get_emptyPwd_message()
        self.assertEqual('password is required',error_message)
    def test_login_errorType_email(self): # 测试错误格式的邮箱
        self.login.input_email('421')
        self.login.input_pwd('12345678q')
        self.login.click_submit()
        error_message = self.login.get_errorType_email()
        self.assertEqual('Invalid email address.',error_message)

    def test_login_error_pwd(self): #测试账号或密码有误
        self.login.input_email('421847541@qq.com')
        self.login.input_pwd('1234')
        self.login.click_submit()
        time.sleep(2)
        error_message = self.login.get_error_pwd()
        self.assertEqual('The username or password is incorrect.',error_message)


if __name__ == '__main__':
    unittest.main()


