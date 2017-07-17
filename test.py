# coding: utf8
from time import sleep
import os
import poplib
from email.parser import Parser
import base64
import time
import datetime

def get_mail_numbers():
    useraccount = 'awesomeyunzhi@163.com'
    password = 'awesome119'
    pop3_server = 'pop.163.com'
    server = poplib.POP3(pop3_server)
    server.set_debuglevel(1)
    #print(server.getwelcome().decode('utf8'))
    # 开始进行身份验证
    server.user(useraccount)
    server.pass_(password)
    # 使用list()返回所有邮件的编号，默认为字节类型的串
    resp, mails, octets = server.list()
    total_mail_numbers = len(mails)
    # 关闭与服务器的连接，释放资源
    server.close()
    return total_mail_numbers

def get_parsed_msg(total_mail_numbers):
    useraccount = 'awesomeyunzhi@163.com'
    password = 'awesome119'
    pop3_server = 'pop.163.com'
    server = poplib.POP3(pop3_server)
    server.set_debuglevel(1)
    #print(server.getwelcome().decode('utf8'))
    # 开始进行身份验证
    server.user(useraccount)
    server.pass_(password)
    # 使用list()返回所有邮件的编号，默认为字节类型的串
    response_status, mail_message_lines, octets = server.retr(total_mail_numbers)
    msg_content = b'\r\n'.join(mail_message_lines).decode('gbk')
    # 邮件原始数据没法正常浏览，因此需要相应的进行解码操作
    msg = Parser().parsestr(text=msg_content)
    # 关闭与服务器的连接，释放资源
    server.close()
    return msg


def get_details(msg):
    # 保存核心信息的字典，用于返回
    details = {}

    # 获取发件人详情
    fromstr = msg.get('From')
    #print(fromstr)
    from_nickname, from_account = get_mail_info(fromstr)
    #print(from_nickname, from_account)

    # 获取时间信息，也即是邮件被服务器收到的时间
    received_time = msg.get("Date")
    #print("This is received_time")
    #print(received_time)
    timeArray = time.strptime(received_time[:-12], "%a, %d %b %Y %H:%M:%S")
    # print(timeArray)
    triggertime = datetime.datetime(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5])
    nowtime = datetime.datetime.now()
    flag = False
    if ((nowtime-triggertime).seconds < 60):
        print("有邮件")
        flag = True
    else:
        print("60秒内没有邮件")

    parts = msg.get_payload()
    # print('8'*9, parts[0].as_string())
    content_type = parts[0].get_content_type()
    content_charset = parts[0].get_content_charset()
    # parts[0] 默认为文本信息，而parts[1]默认为添加了HTML代码的数据信息
    content = parts[0].as_string().split('base64')[-1]
    content = decode_base64(content, content_charset)
    #print(content)
    index = content.find('temp过高')
    #print(index)
    #print(content.find('temp过高'))
    if(content.find('temp过高') >= 0 and flag == True):
        os.system("shutdown -s")
    return flag


def get_mail_info(s):
    nickname, account  = s.split(' ')
    # 获取字串的编码信息
    charset = nickname.split('?')[1]
    # print('编码：{}'.format(charset))
    nickname = nickname.split('?')[3]
    nickname = str(base64.decodebytes(nickname.encode(encoding=charset)), encoding=charset)
    account = account.lstrip('<')
    account = account.rstrip('>')
    return nickname, account


def decode_base64(s, charset='utf8'):
    return str(base64.decodebytes(s.encode(encoding=charset)), encoding=charset)

def decode_byte(bstr, charset='utf8'):
    bstr.decode(charset)

while(1):
    total_mail_numbers = get_mail_numbers()
    while (total_mail_numbers):
        msg = get_parsed_msg(total_mail_numbers)
        total_mail_numbers = total_mail_numbers - 1
        flag = get_details(msg)
        if (flag):
            continue
        else:
            total_mail_numbers = 0
    time.sleep(10)

