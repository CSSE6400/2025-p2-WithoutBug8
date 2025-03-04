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
						 ├── _init_.py    		# 初始化 Flask-SQLAlchemy 数据库实例,由__init__.py文件调用
						 └── todo.py			# 这是ORM模型，定义Todo模型
│   ├── views
						├── routes.py 	  		# 负责增删改查，并将数据写入到数据库中
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

#### 具体函数

