
# sinaweibo_manager

新浪微博营销，管理后台


python环境：python3

# 环境

## supervisor进程管理
- 安装

    sudo apt-get install supervisor

## mysql数据库
- 安装mysql服务：

    sudo apt-get install mysql-server
- 安装mysql客户端(python程序调用client访问server)：
    
    sudo apt-get install mysql-client
    
- 安装mysql客户端相关库：

    sudo apt-get install libmysqlclient-dev

## redis
- 安装命令：

    sudo apt-get install redis

- 通过supervisor启动redis。在supervisor/conf.d/目录下新建一个.conf文件，用来管理redis，其内容如下

    
    [program:redis_server]

    command     = redis-server
    autostart=true
    autorestart=true
    startsecs   = 3
    startretries=3
    user        = root
    
    redirect_stderr         = true
    stdout_logfile_maxbytes = 50MB
    stdout_logfile_backups  = 50
    stdout_logfile          = /hanf/logs/supervisor_redis_server.log
    
    stopasgroup=true
    killasgroup=true


- 说明：

    因为redis安装后并不是默认启动的，这里用supervisor进程管理工具来启动redis


## rabbitmq
- 安装命令：

    sudo apt-get install rabbitmq-server
    
- 说明：
    
    订单需要别的应用程序来完成，所以需要一个消息队列往另外的程序中传递信息，所以需要安装一个rabbitmq的消息队列的服务：
    
- 配置：

    1、上阿里云开启15672端口，以便通过浏览器访问
    
    2、ip:15672访问web管理，新建一个用户和其对应的虚拟主机
    
    3、当不需要使用浏览器来操作rabbitmq的话，可以上阿里云关闭15672端口


## 检测并更新微博账号登录状态
- 脚本：

    scripts/update_weiboaccount_loginstatus.py

- 说明：

    将该脚本做成crontab计划任务，每天检测一遍



## 修改gitlab默认端口

- gitlab安装成功后，默认端口是80，修改其端口（修改完端口后，要在nginx中配置一个端口映射）

    1、打开/etc/gitlab/gitlab.rb
    
    2、修改内容如下：
    
        nginx['listen_port'] = 9091
        
        unicorn['port'] = 9092
        
    3、保存配置，重启gitlab
    
        sudo gitlab-ctl reconfigure
        
        sudo gitlab-ctl restart
        
        sudo gitlab-ctl status
        
        
## 配置二级域名与端口映射
- 安装nginx    

    1、sudo apt update
    
    2、sudo apt install nginx
    
- 修改配置

    1、/etc/nginx/conf.d 目录下新建一个文件vhost.conf
    
    2、vhost.conf内容如下：
    
        server {
            listen 80;
            server_name gitlab.humphry150.com;
            location / { 
                proxy_set_header  Host  $http_host;
                proxy_pass      http://0.0.0.0:9091;
            }   
        }
        server {
            listen 80; 
            server_name testadmin.humphry150.com;
            location / { 
                proxy_set_header  Host  $http_host;
                proxy_pass      http://0.0.0.0:9001;
            }   
        }
        server {
            listen 80; 
            server_name admin.humphry150.com;
            location / { 
                proxy_set_header  Host  $http_host;
                proxy_pass      http://0.0.0.0:9002;
            }   
        }

    3、重新启动nginx，命令为：nginx -s reload
