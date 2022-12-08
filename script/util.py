#!/usr/bin/env python
# encoding: utf-8
import hashlib


def read_file(file):
    with open(file, 'r', encoding='utf-8') as fp:
        return fp.read()


def parse_request(request):
    # ps:使用字典格式获取请求头内容需要判断内容是否为空
    client_ip = request.remote_addr
    # full_url = request.url
    # req_method = request.method
    # req_form = list(request.form)
    # header_host = request.host
    # header_ua = request.user_agent
    # print(f"[*] URL:[{full_url}] SIP:[{client_ip}] SM:[{req_method}] HOST:[{header_host}] FORM:{req_form} UA:[{header_ua}]")


def get_file_md5(file):
    # 打印文本MD5
    md5_hash = hashlib.md5()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        md5 = (md5_hash.hexdigest()).upper()
        return md5


# 判断列表内的字符串是否某个字符串内 # 如果列表为空,就返回default值
def list_in_str(list_=None, str_=None, default=True):
    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag
