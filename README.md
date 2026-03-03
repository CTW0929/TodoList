# Flask Todo List 项目

## 项目结构

```
TodoList/
├── app.py            # 主应用文件
├── config.py         # 配置文件
├── init_db.py        # 数据库初始化脚本
├── app/              # 应用目录
│   ├── __init__.py   # 包初始化文件
│   ├── routes.py     # API路由
│   └── models.py     # 数据库模型
└── README.md         # 项目说明
```

## 环境要求

- Python 3.6+
- Flask
- Flask-SQLAlchemy
- pyodbc
- SQL Server 数据库

## 安装依赖

```bash
pip install Flask Flask-SQLAlchemy pyodbc
```

## 配置数据库连接

编辑 `config.py` 文件，修改数据库连接字符串：

```python
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server'
```

## 初始化数据库

```bash
python init_db.py
```

## 运行应用

```bash
python app.py
```

应用将在 `http://127.0.0.1:5000` 运行。

## API 端点

- `GET /api/todos` - 获取所有待办事项
- `POST /api/todos` - 创建新的待办事项
- `GET /api/todos/<id>` - 获取单个待办事项
- `PUT /api/todos/<id>` - 更新待办事项
- `DELETE /api/todos/<id>` - 删除待办事项
