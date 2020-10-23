# 一个为了学校内统计信息而写的网页

第一个Django项目，质量极差

## Features

- [x] 按班级分组学生
- [x] 支持多班级联合统计
- [x] 支持结果分组化(result group)
- [x] 多用户管理不同班级
- [x] 超级管理员更改用户密码+查看所有统计
- [x] 网页学生端缓存学生名
- [x] 学生端说明内容支持已读反馈
- [ ] Live2d和自定义的提示
- [ ] redis缓存支持

## Disadvantage

- 虽然Django是MVC模式的,但是这个几乎看不出来架构
- 页面几乎没有模板,页面几乎纯重复内容,没有模板
- 强用JS\ajax?······

## 入门

- 主URL转发器 `tongji/url.py`

- 数据库配置文件 `tongji/settings.py`

## Licenses

本项目采用LICSNSE文件内的License,覆盖文件顶部的License