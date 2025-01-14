<p align="center">
	<img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">RuoYi-Vue-Flask</h1>
<h4 align="center">基于Flask+Vue前后端分离的快速开发框架</h4>
<p align="center">
	<a href="https://gitee.com/shaw-lee/ruoyi-vue-flask/blob/5139e50de7a5d97e0a512019e87a0961768ec9aa/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
</p>

## 平台简介

Ruoyi-Vue-Flask是一套全部开源的快速开发平台，给个人及企业免费使用。

* 前端采用Vue、Element UI。
* 后端采用Flask、SQLAlchemy、Pydantic、Redis & Jwt，与Ruoyi-Vue后端主要接口保持一致。
* 权限认证使用Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 高效率开发，使用代码生成器可以一键生成前后端代码（计划中）。
* 特别鸣谢： [Ruoyi-Vue (V3.8.1)](https://gitee.com/y_project/RuoYi-Vue)

## 内置功能

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  部门管理：配置系统组织机构（公司、部门、小组），树结构展现支持数据权限。
3.  岗位管理：配置系统用户所属担任职务。
4.  菜单管理：配置系统菜单，操作权限，按钮权限标识等。
5.  角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
6.  字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7.  参数管理：对系统动态配置常用参数。
8.  通知公告：系统通知公告信息发布维护。
9.  操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
10. 登录日志：系统登录日志记录查询包含登录异常。
11. 在线用户：当前系统中活跃用户状态监控。
12. 定时任务：在线（添加、修改、删除）任务调度包含执行结果日志。
13. 系统接口：根据业务代码自动生成相关的api接口文档。
14. 服务监控：监视当前系统CPU、内存、磁盘、堆栈等相关信息。
15. 缓存监控：对系统的缓存信息查询，命令统计等。
16. 在线构建器：拖动表单元素生成相应的HTML代码。
17. 连接池监视：（待定，python版本不支持druid连接池）
18. Swagger文档：（计划中）
19. 国际化：（计划中）
20. 代码生成：（计划中）

## 安装部署

### 软件版本

```text
os版本：windows 和 linux
python版本：3.10+
mysql版本：5.7+
redis版本：5.0+
node版本：v20.17.0
```

### mysql数据库
```text
数据名： ry-vue-py

执行sql语句
1. sql/ry_20230706.sql
2. sql/ruoyi2owl.sql
```
### 后端快速启动（开发环境:windows）

```cmd
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
.\.venv\Scripts\activate

# 安装依赖
pip3 install -r ./bin/requirements.txt 
```

```text
# 后端配置
./owl_admin/config/app.yml
  ......
  env: 'dev'
  profile: D:/owl/uploadPath
  ......


./owl_admin/config/app-dev.yml
  ......
  SQLALCHEMY_DATABASE_URI: 'mysql+pymysql://root:123456@127.0.0.1/ry-vue-py'
  ......
  REDIS_URL: "redis://127.0.0.1?db=1"
  ......
```

```cmd
# 启动服务
python owl_admin/app.py
```

### 前端快速启动（开发环境:windows）

```cmd
# 安装依赖
cd owl-ui
npm install

# 启动服务
npm run dev
```

### 浏览器访问
```text
地址: http://localhost:80
用户名/密码: admin/admin123
```

## 演示图

<table>
    <tr>
        <td><img src="https://pic1.imgdb.cn/item/677c9c12d0e0a243d4f0c490.png" alt="用户管理.PNG"/></td>
        <td><img src="https://pic1.imgdb.cn/item/677c9c22d0e0a243d4f0c4ab.png" alt="菜单管理.PNG"/></td>
    </tr>
    <tr>
        <td><img src="https://pic1.imgdb.cn/item/677c9c25d0e0a243d4f0c4af.png" alt="部门管理.PNG"/></td>
        <td><img src="https://pic1.imgdb.cn/item/677c9c27d0e0a243d4f0c4b4.png" alt="岗位管理.PNG"/></td>
    </tr>
    <tr>
        <td><img src="https://pic1.imgdb.cn/item/677c9c29d0e0a243d4f0c4b8.png" alt="字典管理.PNG"/></td>
        <td><img src="https://pic1.imgdb.cn/item/677c9c2bd0e0a243d4f0c4bb.png" alt="操作日志.PNG"/></td>
    </tr>
	<tr>
        <td><img src="https://pic1.imgdb.cn/item/677c9c2ed0e0a243d4f0c4c0.png" alt="登录日志.PNG"/></td>
        <td><img src="https://pic1.imgdb.cn/item/677c9c34d0e0a243d4f0c4c6.png" alt="定时任务.PNG"/></td>
    </tr>	 
    <tr>
        <td><img src="https://pic1.imgdb.cn/item/677c9c36d0e0a243d4f0c4c9.png" alt="缓存监控.PNG"/></td>
        <td><img src="https://pic1.imgdb.cn/item/677c93cad0e0a243d4f0bd1e.png" alt="服务监控.PNG"/></td>
    </tr>
</table>

