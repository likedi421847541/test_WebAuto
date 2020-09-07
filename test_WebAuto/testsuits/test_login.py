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
    def test_login_normal(self):
        self.login.input_email('421847541@qq.com')
        self.login.input_pwd('12345678q')
        self.login.click_keepLogin_pwd()
        self.login.click_submit()
    def test_login_no_email(self):
        self.login.input_pwd('12345678q')
        self.login.click_submit()
        error_message = self.login.get_emptyEmail_message()
        self.assertEqual('email is required!',error_message)



if __name__ == '__main__':
    unittest.main()


