#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动gunicorn服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
