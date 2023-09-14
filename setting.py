#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件
GB_VERSION = "0.2 20230914"  # 无需关注
GB_FILE_HASH = None  # 无需关注

# 输入原始报文路径
GB_HTTP_FILE = "http.txt"
# 对外请求代理
GB_PROXIES = {
    # "http": "http://127.0.0.1:8080",
    # "https": "http://127.0.0.1:8080",
    # "http": "http://user:pass@10.10.1.10:3128/",
    # "https": "https://192.168.88.1:8080",
    # "http": "socks5://192.168.88.1:1080",
}

# 对外请求代超时时间 # URL重定向会严重影响程序的运行时间
GB_TIMEOUT = 5

# payload提取文件名
GB_CLIENT_FILE = "forward"
# payload提取参数名
GB_CLIENT_PARAM = "sql"
# 报文中替换pyload的符号标记
GB_MARK_SYMBOL = "***"
# 是否是HTTPS协议
GB_PROTOCOL = "HTTP"  # HTTPS|HTTP|AUTO

# 记录由于代理服务器导致的协议判断不正确响应关键字
GB_ERROR_PAGE_KEY = ["burp suite"]
# burpsuite中可通过 [勾选抑制错误消息] 修复该问题
