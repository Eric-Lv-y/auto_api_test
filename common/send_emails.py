#coding:utf-8

import  time
import smtplib

from email import  encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.mime.multipart import  MIMEMultipart
from common import  commons as common
import os

def _foemat_addr(s):
    name,addr = parseaddr(s)
    return  formataddr((Header(name,'utf-8').encode(),addr))

def send_mail():
    from_addr = "**@qq.com"
    recive_addr = ['**@qq.com']
    smtp_server = "smtp.qq.com"
    License_Key = "**"
    locatime = time.strftime('%Y-%m-%d %H:%M:%S')
    logs = common.Commom().get_logs()
    info =  '''
            这是今日的测试报告！！！
            邮件需要下载后打开！！！
    '''
    content = f'''
        Dear All:
                {info}
                邮件发送时间：{locatime}
'''
    msg = MIMEMultipart()
    body = MIMEText(content.encode(),'plain','utf-8')
    msg.attach(body)
    file_path = os.path.abspath(common.Commom().mkdir_path(os.path.abspath(common.report_html))[0])
    # print('这是file_path'+file_path)
    all_file = os.listdir(file_path)
    for file in all_file:
        file_code = file_path + '/' + file
        attachment = MIMEBase('application','octet-stream')
        attachment.set_payload(open(file_code,'rb').read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition','attachment',filename = file)
        msg.attach(attachment)
    msg['From'] = _foemat_addr('发件人名称 <%s>' % from_addr)
    msg['To'] = _foemat_addr('收件人名称 <%s>'% recive_addr)
    msg['Subject'] = Header('邮件标题','utf-8').encode()
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server,465)
    server.login(from_addr,License_Key)
    server.sendmail(from_addr,recive_addr, msg= msg.as_string())
    logs.debug('收件人是：'+recive_addr[0]+'发件人是：'+from_addr+' ，邮件发送成功!!!')
    server.quit()
# if __name__ == '__main__':
#     send_mail()