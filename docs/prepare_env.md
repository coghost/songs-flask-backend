---
title: Enviroment
---



# Songs Backend of Flask

##  参考链接

- [Mysql设计](https://www.cnblogs.com/mjbrian/p/6841226.html)
- [Nginx支持](https://www.v2ex.com/t/333075)

## 1. 数据流

使用 `https` 方式, 将请求转发到 flask 后端: `nginx` -> `flask`



## 2. 环境配置

- [ubuntu docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#supported-storage-drivers)

### 2.1 安装

```sh
apt-get update

apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

apt-key fingerprint 0EBFCD88

add-apt-repository \
   "deb [arch=armhf] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
apt-get update

apt-get install docker-ce
```



## nginx 配置

```sh
upstream sfb_svr {
    server 127.0.0.1:5000;
}

server {
    listen 443;
    server_name localhost;

    ssl on;
    ssl_certificate /<path>/crt/server.crt;
    ssl_certificate_key /<path>/crt/server.key;

    access_log /<path>/.sfb/nginx_logs/access_log.log;
    error_log /<path>/.sfb/nginx_logs/error_log.log;

    location / {
        proxy_next_upstream error timeout http_502;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        #proxy_set_header   Host                   $http_host;
        #only $host works ok ,$http_host failed.
        proxy_set_header    Host    $host:$proxy_port;
        proxy_set_header   Connection "From LFP";
        proxy_http_version 1.1;
        proxy_pass  http://sfb_svr/;
    }
}
```



## mysql

```sh

docker run \
  --name=mysql_sfb \
  -tid \
  -e 'DB_NAME=sio' \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -p 3306:3306 \
  -v /<HOME_DIR>/Documents/Luoo/mysql:/var/lib/mysql \
  mysql:latest
```
