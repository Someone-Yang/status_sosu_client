# 探针被测端索斯！

[status_sosu](https://github.com/Someone-Yang/status_sosu) 被测端程序。

## 安装

环境：

- 一台能运行 Python 的设备（例如云服务器）
- 不支持虚拟主机

1. 克隆本仓库

```
git clone https://github.com/Someone-Yang/status_sosu_client
```

2. 按需配置

3. 转到程序目录，运行主程序 `app.py`

```
cd ./status_sosu_client
python ./app.py
```

4. 使用 Cron 等添加定时任务，定期运行本程序  
本程序不保持常驻运行，即采即发即走。

## 配置

在根目录中有一个配置文件 `config.yml`，类似下文。

```
host:
  # 展示端主机地址
  address: "http://localhost:5000"
  # 密钥，需和展示端设置一致
  secret: "faputa"
client:
  # 被测本机名称，需和展示端设置一致
  clientname: "demo"
  # 是否打印状态信息
  printstatus: True
  # 是否上传状态信息
  upload: True
  # 是否写入日志
  log: True
```