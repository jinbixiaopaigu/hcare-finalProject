启动项目方法：
1.启动redis
2.启动后端：根目录下执行python owl_admin/app.py
3.启动前端：owl-ui目录下执行npm run dev

如果一切正常就应当能输入验证码直接登录了。另外代码生成属于该版若依未完成功能，建议在菜单管理中和若依官网一起改成停用

本项目：
- 前端基于 [RuoYi-Vue3](https://gitcode.com/yangzongzhuan/RuoYi-Vue3)
- 后端基于 [Ruoyi-Vue-Flask](https://gitee.com/shaw-lee/ruoyi-vue-flask)

目前项目目标：
- [ ]  1.清除首页的联系信息和捐赠支持
- [ ]  2.新建普通用户的菜单和功能
- [ ]  3.配合硬件数据结构修改数据库
- [ ]  4.修复因接口缺失/不匹配的搜索bug(如各种页面点击搜索后的500错误，点击表头后无法排序等)
- [ ]  5.修改logo