# V2EX

这是一个仿写[V2EX](https://www.v2ex.com/)的网站，使用python的flask框架编写.

****
|Author|simonzhoup|
|---|---
|E-mail|simonzhoup@gmail.com

## 特点
完全仿写[V2EX](https://www.v2ex.com/), 虽然不太熟悉前段语言, 但力求一致, 算是一个很好的学习机会.

后端使用 `Flask` 框架编写

有用到 `MySQL` `JavaScript` `CSS` `Bootstrap` `AJAX`


## 截图

### 主页
![](/Screenshots/index.png)
### 节点页
![](/Screenshots/node.png)
### 帖子&回复
![](/Screenshots/post.png)
### 编辑帖子
![](/Screenshots/new.png)
### 注册&登录
![](/Screenshots/register.png)
![](/Screenshots/login.png)


## 如何使用
* 创建数据库
```python
#项目使用Flask-Migrate扩展, 用来管理数据库
#创建迁移仓库
$ python V2DE.py db init

#自动创建迁移脚本
$ python V2DE.py db migrate -m "initial migration"

* 更新数据库
$ python V2DE.py db upgrade
```

* 填充数据
```python
#进入shell环境
$ python V2DE.py shell

#导入数据填充脚本
>>> import populate as p

#填充主题
>>> p.populate_tag()
'Done'
#填充节点
>>> p.populate_node()
'Done'
#填充虚拟用户
>>> p.populate_user()
'Done'
#填充帖子
>>> p.populate_post()
'Done'
#帖子关联用户
>>> p.user_post()
'Done'
```
> 其实这里的步骤不需要这么复杂，一个命令就能完成。


## 启动程序
```python
$ python V2DE.py runserver
```


## 访问
浏览器打开 http://127.0.0.1:5000

