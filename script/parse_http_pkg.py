import json
import xml.etree.ElementTree as ET
from email import parser as mimeparse
from email import policy
from urllib import parse as urlencodeparse

import xmltodict  # type: ignore

# Python解析HTTP请求报文 https://blog.csdn.net/zy010101/article/details/127207055

ENTER = "\n"
CLRF = "\r\n"


def http_parse_simple(http_pkg):
    """
    http报文初步解析函数
    参数：http报文字符串
    返回：http起始行，headers, body
    """
    if ENTER in http_pkg:  # 处理非CLRF分割的http报文
        res = http_pkg_split_simple(ENTER, http_pkg)
    elif CLRF in http_pkg:
        res = http_pkg_split_simple(CLRF, http_pkg)
    else:
        raise Exception("http报文格式错误")
    return res


def http_pkg_split_simple(sep, http_pkg):
    """
    http报文分割函数
    参数：http报文字符串，分割字符
    返回：http起始行，headers, body
    """
    tmp = http_pkg.split(sep=sep, maxsplit=1)
    start_line = tmp[0]
    others = tmp[1]  # 去除http报文起始行之后，剩余的内容应完全遵从MIME数据格式
    # 指定policy为HTTP，使得遵循 RFC 2822以及当前的各种 MIME RFC（RFC 5322, RFC 2047)
    p = mimeparse.Parser(policy=policy.HTTP)
    msg = p.parsestr(text=others, headersonly=False)  # 解析header和body

    headers = {}
    for k, v in msg.items():
        headers[k] = str(v)

    tmp_ = others.split(f"{sep}{sep}", 1)
    if len(tmp_) >= 2:
        body = tmp_[-1]
    else:
        body = None
    return start_line, headers, body


def parse_http_pkg_simple(http_pkg):
    try:
        start_line, headers, body = http_parse_simple(http_pkg=http_pkg)
        # 解析起始行
        method, path, http_version = start_line.split(" ")
        # 解析http body
        content_type = headers.get("Content-Type", "")
        # body = body_parse(body, content_type)
        host = headers.get("Host", "")
    except:
        print("解析失败")
    finally:
        return host, method, path, headers, body, content_type


def http_parse(http_pkg):
    """
    http报文初步解析函数
    参数：http报文字符串
    返回：http起始行，headers, body
    """
    if ENTER in http_pkg:  # 处理非CLRF分割的http报文
        res = http_pkg_split(ENTER, http_pkg)
    elif CLRF in http_pkg:
        res = http_pkg_split(CLRF, http_pkg)
    else:
        raise Exception("http报文格式错误")
    return res


def http_pkg_split(sep, http_pkg):
    """
    http报文分割函数
    参数：http报文字符串，分割字符
    返回：http起始行，headers, body
    """
    tmp = http_pkg.split(sep=sep, maxsplit=1)
    start_line = tmp[0]
    others = tmp[1]  # 去除http报文起始行之后，剩余的内容应完全遵从MIME数据格式
    # 指定policy为HTTP，使得遵循 RFC 2822以及当前的各种 MIME RFC（RFC 5322, RFC 2047)
    p = mimeparse.Parser(policy=policy.HTTP)
    msg = p.parsestr(text=others, headersonly=False)  # 解析header和body

    headers = {}
    for k, v in msg.items():
        headers[k] = str(v)
    body = msg.get_payload()
    return start_line, headers, body


def body_parse(body, content_type=""):
    """
    http body解析函数
    参数：http body
    返回：解析后的结果表示为dict形式
    """
    if isinstance(body, str):  # xml,json,urlencode经过email模块解析之后都是str
        data = get_parse(body, content_type)
    elif isinstance(body, list):  # multipart/form-data解析之后是列表
        data = multipart_parse(body, content_type)
    else:
        data = None
    return data


def get_parse(body, content_type=""):
    """
    获取xml, json, urlencode解析后的结果
    参数：body是http body, content_type应该取自http headers，默认为空字符串
    返回：解析后的结果可能是dict或者list
    """
    # 下面的代码借助了content_type来帮助判断，能加快解析速度。
    if "json" in content_type:
        res, data = is_json(body)
        if res:
            return data
        else:
            return None
    elif "xml" in content_type:
        res, data = is_xml(body)
        if res:
            return data
        else:
            return None
    elif "urlencode" in content_type:
        res, data = is_urlencode(body)
        if res:
            return data
        else:
            return None
    else:  # 无法从http headers中获取content_type或者content_type的类型不是以上几种
        res, data = is_json(body)
        if res:
            return data
        res, data = is_xml(body)
        if res:
            return data
        res, data = is_urlencode(body)
        if res:
            return data
        return None


def is_json(data):
    """
    判断数据是否是JSON
    参数：数据data
    返回：一个bool值，如果是True，表示是JSON；如果是False，表示不是JSON。第二个值是JSON的情况下，返回JSON解析的结构，否则返回None
    """
    try:
        res = json.loads(data)
    except json.JSONDecodeError:
        return False, None
    else:
        return True, res


def is_xml(data):
    """
    判断数据是否是xml，如果是并将其转为字典
    参数：数据data
    返回：一个bool值，如果是True，表示是xml；如果是False，表示不是xml
    """
    try:
        ET.fromstring(data)
    except ET.ParseError:
        return False, None
    else:
        # 是xml，并将其转为dict
        res = xmltodict.parse(data)
        return True, res


def is_urlencode(data):
    """
    判断数据是否是urlencode
    参数：数据data
    返回：一个bool值和一个字典，如果是True，表示是urlencode，并返回解析后的字典；如果是False，表示不是urlencode，并返回None
    """
    try:
        # 保留没有值的键，如果解析错误，引发ValueError异常
        res = urlencodeparse.parse_qs(qs=data, keep_blank_values=True, strict_parsing=True)
    except ValueError:
        return False, None
    else:
        return True, res


def multipart_parse(body, content_type=""):
    """
    解析multipart/form-data格式的数据
    参数：body是http body, content_type应该取自http headers，默认为空字符串
    返回：multipart/form-data格式的数据的解析结果
    """
    if "multipart/form-data" in content_type:
        res = []
        for b in body:
            for k, v in b.items():
                if k == "Content-Disposition":
                    info = urlencodeparse.parse_qs(qs=v)
                    break
            info["Content-Type"] = b.get_content_type()
            info["content"] = b.get_content()  # type: ignore
            res.append(info)
        return res
    else:
        return None


def parse_http_pkg(http_pkg):
    try:
        start_line, headers, body = http_parse(http_pkg=http_pkg)
        # 解析起始行
        method, path, http_version = start_line.split(" ")
        # 解析http body
        content_type = headers.get("Content-Type", "")
        # body = body_parse(body, content_type)
        host = headers.get("Host", "")
    except:
        print("解析失败")
    finally:
        return host, method, path, headers, body, content_type


if __name__ == "__main__":
    http_pkg = """POST /v2/pet/1/uploadImage HTTP/2
Host: petstore.swagger.io
Content-Length: 998
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="99"
Accept: application/json
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarygZCWUWVOUSClxVIr
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36
Sec-Ch-Ua-Platform: "Linux"
Origin: https://petstore.swagger.io
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://petstore.swagger.io/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9

------WebKitFormBoundarygZCWUWVOUSClxVIr
Content-Disposition: form-data; name="additionalMetadata"

2
------WebKitFormBoundarygZCWUWVOUSClxVIr
Content-Disposition: form-data; name="file"; filename="test.png"
Content-Type: image/png

\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01)\x00\x00\x00\xdb\x08\x02\x00\x00\x00\xbe\xd6\xf0s\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95+\x0e\x1b\x00\x00\x02yIDATx\x9c\xed\xd31\x01\x00 \x0c\xc00\xc0\xcb\xfc[\xc4\x05=H\x14\xf4\xe9\x9e\x99\x05<w\xea\x00\xf8\x94\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0q\x01\xdb\xc4\x02%u\xd0\xc3\x18\x00\x00\x00\x00IEND\xaeB`\x82
------WebKitFormBoundarygZCWUWVOUSClxVIr--
"""
    host, method, path, headers, body, content_type = parse_http_pkg_simple(http_pkg)
    print(method)  # POST
    print(path)  # /v2/pet/1/uploadImage
    print(body)
    # [{' name': ['"additionalMetadata"'], 'Content-Type': 'text/plain', 'content': '2'}, {' name': ['"file"'], ' filename': ['"test.png"'], 'Content-Type': 'image/png', 'content': b'\x89PNG\r\n\x1a
