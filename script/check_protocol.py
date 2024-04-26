#!/usr/bin/env python
# encoding: utf-8
import requests
import setting
from script.util import list_in_str

requests.packages.urllib3.disable_warnings()


def check_url(url, method):
    status_code = -1
    # text_length = -1
    try:
        response = requests.request(method, url, proxies=setting.GB_PROXIES, timeout=setting.GB_TIMEOUT, verify=False,
                                    allow_redirects=False)
        status_code = response.status_code
        text_length = len(response.text)
        print(f"[*] {url} text_length:{text_length}")
        # print(f"{url} text_length:{response.text}")
        # 排除由于代理服务器导致的访问BUG
        if list_in_str(setting.GB_ERROR_PAGE_KEY, response.text.lower(), False):
            print("[!] 当前由于代理服务器问题导致响应状态码错误...Fixed...")
            status_code = -1
    except Exception as error:
        pass
        # print(f"[*] CHECK URL PROTOCOL OCCUR ERROR: {error}")
    finally:
        return status_code


def check_protocol(host, path):
    result = {}
    for proto in ["https", "http"]:
        url = f"{proto}://{host}{path}"
        result[proto] = check_url(url, 'GET')

    print(f"[*] PROTOCOL CHECK RESULT:{result}")

    # 处理协议值为None的情况
    result = {key: value if value is not None else -1 for key, value in result.items()}

    if result["https"] <= 0 and result["http"] <= 0:
        return None

    if result["https"] <= 0 and result["http"] > 0:
        return "http"

    if result["https"] > 0 and result["http"] <= 0:
        return "https"

    if result["https"] > 0 and result["http"] > 0:
        if str(result["https"]).startswith("30"):
            return "http"
        else:
            return "https"


if __name__ == "__main__":
    host = 'petstore.swagger.io'
    path = '/'
    print(check_protocol(host, path))
