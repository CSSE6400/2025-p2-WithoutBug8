## 这是Practice-2的项目笔记

#### 项目结构

```shell
.
├── instance/         							# 存放SQLite数据库文件
├── tests/            							# 存放单元测试的代码
		├── base.py								# 提供独立的数据库模式，防止在测试过程中修改数据库
		├── test_todo.py						# 提供的一些测试案例
		└── test_health.py						# 小demo用于验证是否可以进行单元测试
├── todo/							
│   ├── models 									# 存放数据模型
			 ├── _init_.py    					# 初始化 Flask-SQLAlchemy 数据库实例,由__init__.py文件调用
			 └── todo.py						# 这是ORM模型，定义Todo模型
│   ├── views
			├── routes.py 	  					# 负责增删改查，并将数据写入到数据库中
│   ├── __init__.py								# 主文件，负责启动整个程序
├── .gitignore
├── endpoints.http								# 这个文件主要用于测试API
├── poetry.lock									# 由 Poetry 生成的依赖管理文件
├── pyproject.toml								# 由 Poetry 生成的依赖管理文件
├── README_ZH.md
└── README.md
```



#### 运行流程

1. 启动后端Flask服务，监听端口:6400,等待API请求；这一步主要在--init.py--文件里
2. 处理API请求，route中定义了增删改查操作，Flask 根据 @api.route 处理请求
3. endpoint.http 用于测试请求，根据不同的路径响应不同的请求GET、POST、PUT、DELETE
4. 单元测试文件，用于确保API的逻辑是否正确

#### 解决的问题
1. ✅查询completed问题;如果请求参数中有completed的话需要把已完成/未完成的任务暂时给用户，而不是把全部数据展示给用户
2. ✅查询windows问题；window窗口参数应该是查询从当前开始，window天之后的任务，需要把这些展示给用户
3. ✅恶意添加未知字段的问题：本来规定的数据库的默认字段，但是不怀好意者永远想添加默认的字段，所以严防默认字段插入
4. ✅修改主键问题：默认状态下主键最好不要修改
5. ✅修改未知字段问题：修改数据库中的数据时，不能修改未知(新建)的字段，这是不合法的

