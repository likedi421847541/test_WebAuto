# -*- coding:utf-8 -*-
import os,sys
import smtplib
import time
import configparser   #configparser 读取配置文件
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reportPath = os.path.dirname(os.path.realpath(__file__))
reportPath = os.path.dirname(reportPath)+r'\test_report'

print(reportPath)

class SendMail():
    def get_report(self):  # 为了在测试报告的路径下找到最新的测试报告
        dirs = os.listdir(reportPath)
        dirs.sort(key=lambda fn:os.path.getatime(os.path.join(reportPath,fn)))
        newreportname = os.path.join(reportPath,dirs[-1])  # 获取最新的报告的地址
        return newreportname  # 返回的是测试报告的名字
    def send(self):

        # 读取邮件配置，如发送者，接受者等
        config = configparser.ConfigParser()
        config_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.dirname(config_path)+r'\config\config.ini'
        print(config_path)
        config.read(config_path, encoding='utf-8')  # 读取 config 内容
        smtp_server = config.get('email', 'smtp_server')
        sender = config.get('email', 'sender')
        psw = config.get('email', 'psw')
        receiver = config.get('email', 'receiver')
        port = config.get('email', 'port')

        newreport = self.get_report()  #获取最新的报告
        with open(newreport, 'rb') as f:
            mailbody = f.read()  # 读取测试报告的内容

        #定义邮件内容
        msg = MIMEMultipart()
        body = MIMEText(mailbody, _subtype='html', _charset='utf-8')  # 将测试报告的内容放在 邮件的正文中
        msg['Subject'] = 'Web 自动化测试报告'  # 邮件标题
        msg['from'] = sender
        msg['to'] = receiver
        msg.attach(body)  # 将 body 附加在msg 里

        # html 附件  下面是将测试报告放在附件中发送
        att = MIMEText(open(newreport,'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="TestReport.html"'  # 这里的filename可以任意写，写什么名字，附件的名字就是什么
        msg.attach(att)

        # 设置邮件发送方
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_server)  # 连服务器
            smtp.login(sender, psw)
        except:
            smtp = smtplib.SMTP_SSL(smtp_server, port)
            smtp.login(sender, psw)  # 登录
        smtp.sendmail(from_addr= sender,to_addrs=receiver,msg = msg.as_string())  # 发送邮件
        smtp.quit()
        print('sendmail success')


if __name__ == '__main__':
    sendMail = SendMail()
    sendMail.send()