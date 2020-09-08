# -*- coding:utf-8 -*-
import os,sys
import smtplib
import time
import configparser   #configparser 读取配置文件
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reportPath = os.path.dirname(os.path.abspath(('.')))+r'\test_report'

print(reportPath)

class SendMail():
    msg = MIMEMultipart()
    def get_report(self):  # 为了在测试报告的路径下找到最新的测试报告

        dirs = os.listdir(reportPath)
        dirs.sort(key=lambda fn:os.path.getatime(os.path.join(reportPath,fn)))
        newreportname = os.path.join(reportPath,dirs[-1])
        #print(newreportname)
        return newreportname  # 返回的是测试报告的名字
    def email_config(self):  #读取邮件配置，如发送者，接受者等
        config = configparser.ConfigParser()
        config_path = os.path.dirname(os.path.abspath('.')) + r'\\config\\config.ini'
        # print(config_path)
        config.read(config_path, encoding='utf-8')  # 读取 config 内容
        self.smtp_server = config.get('email', 'smtp_server')
        self.sender = config.get('email', 'sender')
        print(self.sender)
        self.psw = config.get('email', 'psw')
        self.receiver = config.get('email', 'receiver')
        port = config.get('email', 'port')
    def get_report_file(self):
        newreport = self.get_report()
        self.msg = MIMEMultipart()
        self.msg['Subject'] = 'Web 自动化测试报告'  # 邮件标题
        self.msg['date'] = time.strftime('%a,%d %b %Y %H:%M:%S %z')
        #self.msg['from'] = self.sender
        with open(os.path.join(reportPath, newreport), 'rb') as f:
            mailbody = f.read()  # 读取测试报告的内容
        html = MIMEText(mailbody, _subtype='html', _charset='utf-8')  # 将测试报告的内容放在 邮件的正文中
        self.msg.attach(html)  # 将 html 附加在msg 里

        # html 附件  下面是将测试报告放在附件中发送
        att1 = MIMEText(mailbody, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'

        att1["Content-Disposition"] = 'attachment; filename="TestReport.html"'  # 这里的filename可以任意写，写什么名字，附件的名字就是什么
        self.msg.attach(att1)
    def send(self):



        # # recipients = ['xxxx@xxxx.com', 'xxxx@qq.com', 'xxx@xxxxx.com']  # 发送给多个人
        # recipients = ['hgxxx@nnnx.cn']  # 发送给一个人
        # self.take_message()
        # self.msg['from'] = 'hg@xxx.cn'  # 发送邮件的人，这种是公司邮箱转发
        # # self.msg['to'] = recipients  # 收件人和发送人必须这里定义一下，执行才不会报错。
        # toaddrs = recipients
        self.get_report()
        self.get_report_file()
        self.email_config()
        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_server)
        smtp.login(self.sender,self.psw)

        smtp.sendmail(from_addr= self.sender,to_addrs=self.receiver,msg = self.msg.as_string())  # 发送邮件
        smtp.close()
        print('sendmail success')
if __name__ == '__main__':
    # config = configparser.ConfigParser()
    # config_path = os.path.dirname(os.path.abspath('.')) + r'\\config\\config.ini'
    # print(config_path)
    # config.read(config_path, encoding='utf-8')  # 读取 config 内容
    # smtp_server = config.get('email', 'smtp_server')
    # sender = config.get('email', 'sender')
    # print(sender)
    # psw = config.get('email', 'psw')
    # receiver = config.get('email', 'receiver')
    # port = config.get('email', 'port')
    sendMail = SendMail()
    sendMail.send()