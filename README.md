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

2. 安装依赖文件

3. 按需配置  
请在配置文件 `config.yml` 填入服务端（展示端）地址和密钥，并按需设置其他功能开关。

4. 转到程序目录，运行主程序 `app.py`

```
cd ./status_sosu_client
python3 ./app.py
```

5. 使用 Cron 等添加定时任务，定期运行本程序  
本程序不保持常驻运行，即采即发即走。

## 配置

在根目录中有一个配置文件 `config.yml`。

配置功能见文件中的注释。