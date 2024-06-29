# <center>HIT 2024春季学期 软件工程课程实践项目</center>
## <center>E萌宠（eCutePet）宠物综合服务平台 · 说明文档</center>

__目录：__ 概述、部署

__开发人员：__ 林枭熠、苗梓萌、王梓健
#### 开发时间：2024/06/07~2024/06/29

---

## 一、概述

&emsp;&emsp;本项目是哈尔滨工业大学 2024 春季学期软件工程课程实践项目的成果，主体为 `Django` 后端 + `VUE` 前端实现的 *Web* 项目，主要数据库为 `MySQL` ，同时采用了 `Redis` 数据库作为缓存数据库，并以 `cerely` 实现异步任务。

&emsp;&emsp;E萌宠（eCutePet）是一个面向 <font color=DodgerBlue>宠物饲养</font> 的综合性服务平台，包含 **社区**、**商城**、**宠物预约就诊** 三大板块，服务于 **宠物主** 和 **宠物医生** 两类主体用户，具体功能可自行体验或参考验收PPT，开发流程详见实验报告，二者在此不做赘述。

---

## 二、部署

### 1. 后端部署

&emsp;&emsp;后端部署到本地需执行以下流程：

+ 新建并激活虚拟环境，在本目录下打开终端，输入指令：

    ```terminal OR cmd
    pip install -r requirements.txt
    ```
+ 配置 `MySQL` ，*root* 密码设置为 <font color=gold>eCutePet</font>，或更改 `./backend/EdjangoProject/settings.py` 中 **DATABASES** 的 'USER' 和 'PASSWORD' ，使之符合本地 mysql 设置

+ 新建连接到项目，在连接下新建 mysql 数据库，名为 `e_database`

+ 配置 `Redis` 并启动 redis 服务

+ 启动 `celery` 服务

+ 启动消费者进程，在 `./backend` 目录下新建终端，输入指令：

    ```terminal OR cmd
    celery -A E_djangoProject worker -l info
    ```
        
+ 启动生产者进程，在 `./backend` 目录下新建终端，输入指令：

    + 对于 Linux 系统

        ```terminal
        celery -A E_djangoProject worker -l info -P eventlet
        ```

    + 对于 Windows 系统

        ```cmd
        celery -A E_djangoProject worker -l info -P eventlet
        ```

+ 进行数据库迁移，在 `./backend` 目录的终端下输入指令：

    ```termianl OR cmd
    python manage.py makemigrations
    python manage.py migrate
    ```

+ 创建管理员（超级用户），在 `./backend` 目录的终端下输入指令：

    ```termianl OR cmd
    python manage.py createsuperuser
    ```

+ 启动 `Django` 服务器，在`./backend` 目录的终端下输入指令：

    ```terminal OR cmd
    python manage.py runserver
    ```

&emsp;&emsp;本项目后端已部署到云服务器，公网 IP 为 http://182.92.171.51:8000/ ，并且前端接口调用时采用的是云服务器上配置好的后端的 API 接口，如有本地开发和测试的需要，可在本地完成后端部署后将 `./appfront/src/api/api.js` 中的所有 *182.92.171.51* 都替换为 *127.0.0.1* 。

&emsp;&emsp;http://182.92.171.51:8000/api/docs 为后端 API 接口文档，可供参考。

---

### 2. 数据初始化

&emsp;&emsp;详见 `./DataInit` 下的 markdown 说明文档。

---

### 3. 前端部署

&emsp;&emsp;本地完成 `NodeJs` 部署后，在 `./appfront` 目录下打开终端，输入如下指令即可在 http://localhost:8080 打开前端页面：

```terminal OR cmd
npm run dev
```


