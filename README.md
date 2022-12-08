

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
```

### 0X02 框架特点

```
1、支持自动解析HTTP报文，参考sqlmap的-r参数
2、支持自定义修改请求处理、载荷处理、响应处理
```



### 0X02 更新记录

```
20221208 初步实现中转注入框架
测试 中继 普通GET报文、普通POST报文、普通PUT传参、文件上传包、JSON传参报文、XML传参报文等报文格式 通过
测试 中继 POST型SQL注入 通过
```



### 0X03 TODO

```
可选:优化全局变量结构
```



### 0X04 使用方法

```
1、在【http.txt】内粘贴【burp格式的】HTTP请求报文
2、在【http.txt】内在需要替换位置输入【***】
3、在【setting.py】中指定目标URL的协议，AUTO表示自动识别
4、访问本地【http://127.0.0.1:8888/forward?sql=1】
5、在【setting.py】可配置相关参数名、请求代理等
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

