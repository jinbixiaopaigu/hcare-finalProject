启动项目方法：
1.启动redis
2.启动虚拟环境：根目录下执行.\venv38\Scripts\activate
3.启动后端：根目录下执行python owl_admin/app.py
4.启动前端：owl-ui目录下执行npm run dev

如果一切正常就应当能输入验证码直接登录了。另外代码生成属于该版若依未完成功能，建议在菜单管理中和若依官网一起改成停用

本项目：
- 前端基于 [RuoYi-Vue3](https://gitcode.com/yangzongzhuan/RuoYi-Vue3)
- 后端基于 [Ruoyi-Vue-Flask](https://gitee.com/shaw-lee/ruoyi-vue-flask)

目前项目目标：
- [x]  1.清除首页的联系信息和捐赠支持
- [ ]  2.新建普通用户的菜单和功能
- [ ]  3.配合硬件数据结构修改数据库
- [ ]  4.修复因接口缺失/不匹配的搜索bug(如各种页面点击搜索后的500错误，点击表头后无法排序等)
- [ ]  5.修改logo
- [ ]  6.从华为research sdk中获取项目信息


华为research sdk初始化脚本使用方法：根目录新建config.ini
格式为：
[credentials]
access_key = <your_access_key>
secret_key = <your_secret_key>
然后根目录执行python bridge_client_init.py


docker首次启动方法:根目录执行docker-compose up --build

项目数据必须要要在乐龄智伴中的统计页面下拉后才能同步到华为research库中