

# HTTPRelayServer  



### 0X00 严正声明:

```
本工具仅用于合法范围内进行企业防御测试,请勿用于违法活动, 否则所有产生后果由使用者自身负责！！！

本团队任何技术及文件仅用于学习研究，请勿用于任何违法活动，感谢大家的支持！！！
```


### 0X01 框架用途

```
1、通过中转发服务器实现【请求、响应、格式】数据修改，常用于实现中转SQL注入
2、复活古老的GET型号工具，转变请求方式
3、其他思路还有中转Webshell流量免杀、中转加密爆破等功能
4、相关实践资料较多，但是没有完善的框架项目，基于项目驱动对其进行实现
5、非持久项目|视需求维护和开放
```



### 0X02 框架特点

```
1、支持自动解析HTTP报文，参考sqlmap的-r参数
2、支持自定义修改 请求处理、载荷处理、响应处理、配置参数
```



### 0X02 更新记录

```
20221208 初步实现中转注入框架
    中转 普通GET报文 测试通过
    中转 普通POST报文 测试通过
    中转 普通PUT传参 测试通过
    中转 文件上传包 测试通过
    中转 JSON传参报文 测试通过
    中转 XML传参报文  测试通过
    中转 POST型SQL注入 测试通过
    详情查看【中转测试记录.docx】
建议测试时，开启Burpsuite查看流量信息，防止发生未知错误
```



### 0X03 TODO

```
可选:优化全局变量结构
```



### 0X04 使用方法

```
1、在【http.txt】内、粘贴【burp格式的】HTTP请求报文
2、在【http.txt】内在需要替换位置输入【***】，参考sqlmap的【*】标志
3、在【setting.py】中指定目标URL的协议，【AUTO】表示自动识别
4、启动【python3 httpRelayServer.py】

注意：协议自动识别可能存在错误，请注意查看提示信息:
未检测成功：
[*] PROTOCOL CHECK RESULT:{'https': -1, 'http': -1}
[+] 当前自动获取的请求协议为:None 

已检测成功：
[*] PROTOCOL CHECK RESULT:{'https': -1, 'http': 302}
[+] 当前自动获取的请求协议为:http


5、访问本地【http://127.0.0.1:8888/forward?sql=1】 
正常响应应该为【http.txt】重放的效果
可通过配置【setting.py】的【GB_PROXIES】进行流量查看。

6、在【setting.py】可配置相关参数名、请求代理等。
```



### 0X05 相关案例

```
SQL 注入进阶：FLASK 加工中转 SQLMAP 流量
https://mp.weixin.qq.com/s/L8WyJcreQ09z76XjSRDSLQ

通过 selenium 和 flask 中转后利用 sqlmap 进行注入
https://mp.weixin.qq.com/s/mtn_5lx1S-d0Ahbm5zqjIQ

利用WebSocket接口中转注入渗透实战
https://mp.weixin.qq.com/s/gOE71HRTB-jtSybkbLH1Vg

第34篇：go语言编写"中转注入"让古老的注入工具复活
https://mp.weixin.qq.com/s/2PBgJzKRt4DaL2uAQX50GA
```



### 0X06 NEED STAR And ISSUE

```
1、右上角点击Star支持更新.
2、ISSUE或NOVASEC提更新需求
```

![NOVASEC](doc/NOVASEC.jpg)