# GNE网页信息提取接口

[原gne项目地址](https://github.com/kingname/GeneralNewsExtractor/projects/1)

## 环境配置

**python3.7+**

安装依赖：

```
pip install -r requirements.txt
```



## 启动服务

启动：

```
python parse.py [port]
```

- port:	服务端口号，默认8000

后台启动（Linux）：

```
nohup python parse.py [port] > /dev/null 2>&1 &
```



## 接口文档

- 在线文档（需要先启动服务）：
  - redoc（推荐）：http://IP:端口/redoc		（例如：http://127.0.0.1:8000/redoc）
  - swagger：http://IP:端口/docs

