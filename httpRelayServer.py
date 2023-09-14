#!/usr/bin/env python
# encoding: utf-8
import sys

from flask import Flask, make_response, request

from script.check_protocol import check_protocol
from script.handle_requests import handle_request
from script.handle_response import handle_response
from script.parse_http_pkg import parse_http_pkg_simple
from script.util import read_file, parse_request, get_file_md5
import setting

# 判断是否需要重新加载变量
setting.GB_FILE_HASH = get_file_md5(setting.GB_HTTP_FILE)

# 初始化HTTP报文 # 存放在此处不支持热加载
http_pkg = read_file(setting.GB_HTTP_FILE)
http_host, http_method, http_path, http_headers, http_body, http_content_type = parse_http_pkg_simple(http_pkg)
# 动态判断判断请求协议
if "auto" in setting.GB_PROTOCOL.lower():
    setting.GB_PROTOCOL = check_protocol(http_host, http_path)
    print(f"[+] 当前自动获取的请求协议为:{setting.GB_PROTOCOL}")

sys.dont_write_bytecode = True  # 设置不生成pyc文件

# 启动FLASK服务器
app = Flask(__name__)


@app.route(f'/{setting.GB_CLIENT_FILE}', methods=['GET', 'POST'])
def forward():
    # 收到请求
    parse_request(request)
    # http://127.0.0.1:8888/forward?sql=1%20and%201=1

    # 接受参数
    payload = request.values.get(setting.GB_CLIENT_PARAM)
    print(f"[*] 请求信息:[{setting.GB_CLIENT_FILE}]---[{setting.GB_CLIENT_PARAM}]---[{payload}]")

    # 热加载HTTP请求包
    new_file_md5 = get_file_md5(setting.GB_HTTP_FILE)
    if new_file_md5 != setting.GB_FILE_HASH:
        print("请求包文件已经改变,需要重新读取配置文件,注意本次不会改变请求协议...")
        global http_pkg, http_host, http_method, http_path, http_headers, http_body, http_content_type
        http_pkg = read_file(setting.GB_HTTP_FILE)
        http_host, http_method, http_path, http_headers, http_body, http_content_type = parse_http_pkg_simple(http_pkg)
        setting.GB_FILE_HASH = new_file_md5

    # 代理请求
    response = handle_request(http_host, http_method, http_path, http_headers, http_body, http_content_type, payload)
    # 处理响应
    resp_headers, resp_content, resp_status = handle_response(response)
    # 返回响应
    resp = make_response(resp_content)
    resp.status = resp_status
    resp.http_headers = resp_headers
    return resp


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8888, debug=True)
    app.run(host='127.0.0.1', port=8888, debug=False, threaded=True)
