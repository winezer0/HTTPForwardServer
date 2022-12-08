#!/usr/bin/env python
# encoding: utf-8

import sys
sys.dont_write_bytecode = True  # 设置不生成pyc文件


def handle_response(response):
    resp_headers = response.headers
    resp_content = response.content
    resp_status = str(response.status_code)
    return resp_headers, resp_content, resp_status
