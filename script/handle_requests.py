#!/usr/bin/env python
# encoding: utf-8
import sys
import urllib

import requests

import setting
from script.handle_payload import handle_payload

sys.dont_write_bytecode = True  # 设置不生成pyc文件
requests.packages.urllib3.disable_warnings()


def handle_request(host, method, path, headers, body, content_type, payload):
    # print(f"host: {host}")
    # print(f"method: {method}")
    # print(f"path: {path}")
    # print(f"headers: {headers}")
    # print(f"body: {body}")
    # print(f"content_type: {content_type}")
    # print(f"payload: {payload}")

    # 判断path中是否存在请求头 例如 POST http://xxxx/Admin/Default.aspx
    if host in path:
        query = "?" + path.split("?", 1)[1] if "?" in path else ""
        path = urllib.parse.urlsplit(path).path + query
        print(f"new path:{path}")

    # 组合URL
    url = f"{setting.GB_PROTOCOL.lower()}://{host}{path}"
    print(f"url:{url}")

    # 处理payload
    payload = handle_payload(payload)

    # 判断注入标记是否在URL中
    if setting.GB_MARK_SYMBOL in url:
        payload = urllib.parse.quote(payload)  # 当注入点在URL中时 对payload进行URL编码
        url = url.replace(setting.GB_MARK_SYMBOL, payload)

    # 判断注入标记是否在Body中
    if body and setting.GB_MARK_SYMBOL in body:
        # 对json内的数据应该做双引号转义处理
        if 'application/json' in content_type:
            payload = payload.replace(r'"', r'\"')

        # 当注入点在body中时 对payload中的空格进行编码,转为+号
        payload = payload.replace(" ", "+")
        body = body.replace(setting.GB_MARK_SYMBOL, payload)
        # 修复Body中的换行符
        if "\r\n" not in body and "\n" in body:
            body = body.replace("\n", "\r\n")
            print("Fixed Body CLRF...")


        # 根据内容类型 对body参数进行处理 复杂,尝试不处理Body格式
        # if 'application/json' in content_type:
        #     body = json.dumps(body)
        # if 'boundary' in content_type:
        # 处理文件上传 https://blog.csdn.net/Chihwei_Hsu/article/details/81943008
        # 对于普通格式 application/x-www-form=urlencoded 不知道怎么替换处理 data={'key1':'value1','key2':'value2'}
        # https://blog.csdn.net/Gym987/article/details/104479154

    response = requests.request(method,
                                url,
                                data=body,
                                headers=headers,
                                proxies=setting.GB_PROXIES,
                                timeout=setting.GB_TIMEOUT,
                                verify=False)
    return response
