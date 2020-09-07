# -*- coding:utf-8 -*-
import unittest
import os
import time
from framework import HTMLTestRunner
cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)
report_path = cur_path + '/test_report/'#设置报告文件的地址
if not os.path.exists(report_path):os.mkdir(report_path)
# 获取当前时间
now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
# 设置报告名称格式
HtmlFile = os.path.join(report_path,now+'result.html')
fp = open(HtmlFile,'wb')
# 用例路径
case_path = os.path.join(os.getcwd(),'testsuits')
print(case_path)

# 构建 suite
suite = unittest.TestLoader().discover(case_path,'test_*.py',top_level_dir=None)

if __name__ == '__main__':
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'Web 自动化测试报告')
    runner.run(suite)
    fp.close()