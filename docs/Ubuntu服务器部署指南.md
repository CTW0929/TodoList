# Ubuntu 服务器部署 TodoList 应用详细流程

## 1. 服务器准备

### 1.1 更新系统
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 安装必要的系统依赖
```bash
sudo apt install -y python3 python3-pip python3-venv git nginx ufw curl
```

### 1.3 配置防火墙
```bash
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 2. 应用部署

### 2.1 创建应用目录
```bash
sudo mkdir -p /var/www/todolist
sudo chown -R $USER:$USER /var/www/todolist
cd /var/www/todolist
```

### 2.2 克隆代码
```bash
git clone <repository-url> .
```

### 2.3 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.4 安装依赖
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.5 配置环境变量
编辑 `.env` 文件：
```bash
nano .env
```

添加以下内容：
```
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### 2.6 初始化数据库
```bash
# 确保在项目根目录下执行
cd /var/www/todolist

# 激活虚拟环境
source venv/bin/activate

# 运行数据库初始化
python init_db.py
```

## 3. 配置 Gunicorn

### 3.1 创建 Gunicorn 配置文件
```bash
cat > gunicorn.conf.py << EOF
bind = '127.0.0.1:8000'
workers = 3
timeout = 120
EOF
```

## 4. 配置 Nginx 反向代理

### 4.1 创建 Nginx 配置文件
```bash
sudo cat > /etc/nginx/sites-available/todolist << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
```

### 4.2 启用站点
```bash
sudo ln -s /etc/nginx/sites-available/todolist /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 5. 配置 Systemd 服务

### 5.1 创建服务文件
```bash
sudo cat > /etc/systemd/system/todolist.service << EOF
[Unit]
Description=TodoList Flask Application
After=network.target

[Service]
User=$USER
WorkingDirectory=/var/www/todolist
Environment="PATH=/var/www/todolist/venv/bin"
ExecStart=/var/www/todolist/venv/bin/gunicorn -c gunicorn.conf.py app:app

[Install]
WantedBy=multi-user.target
EOF
```

### 5.2 启动并启用服务
```bash
sudo systemctl daemon-reload
sudo systemctl start todolist
sudo systemctl enable todolist
```

### 5.3 检查服务状态
```bash
sudo systemctl status todolist
```

## 6. 前端部署（可选）

### 6.1 安装 Node.js
```bash
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install -y nodejs
```

### 6.2 构建前端
```bash
cd /var/www/todolist/frontend
npm install
npm run build
```

### 6.3 配置 Nginx 以服务前端静态文件
修改 Nginx 配置：
```bash
sudo nano /etc/nginx/sites-available/todolist
```

添加静态文件服务配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 服务前端静态文件
    location / {
        root /var/www/todolist/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 服务后端 API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

重启 Nginx：
```bash
sudo nginx -t
sudo systemctl restart nginx
```

## 7. 验证部署

### 7.1 检查应用是否运行
```bash
curl http://localhost:8000/api/todos
```

### 7.2 通过域名访问
- 后端 API：`http://your-domain.com/api/todos`
- 前端应用：`http://your-domain.com`

### 7.3 测试 API 功能
- 注册用户：`POST /api/auth/register`
- 登录：`POST /api/auth/login`
- 创建任务：`POST /api/todos`
- 获取任务：`GET /api/todos`

## 8. 维护与监控

### 8.1 查看应用日志
```bash
sudo journalctl -u todolist
```

### 8.2 重启应用
```bash
sudo systemctl restart todolist
```

### 8.3 更新应用
```bash
cd /var/www/todolist
git pull
source venv/bin/activate
pip install -r requirements.txt

# 如果前端有更新
cd frontend
npm install
npm run build

# 重启服务
sudo systemctl restart todolist
sudo systemctl restart nginx
```

## 9. 故障排除

### 9.1 常见错误及解决方法

#### 502 Bad Gateway 错误
- 检查 Gunicorn 服务是否运行：`sudo systemctl status todolist`
- 检查 Gunicorn 日志：`sudo journalctl -u todolist`

#### 404 Not Found 错误
- 检查 Nginx 配置是否正确
- 检查前端文件是否正确构建

#### 数据库连接错误
- 检查数据库文件权限
- 确保数据库初始化成功

### 9.2 查看详细日志
```bash
# 应用日志
tail -f logs/app.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/error.log

# Gunicorn 日志
sudo journalctl -u todolist -f
```

## 10. 注意事项

1. **数据库备份**：定期备份 `todo.db` 文件
2. **安全更新**：定期更新系统和依赖包
3. **HTTPS 配置**：建议使用 Let's Encrypt 配置 HTTPS
4. **日志监控**：设置日志监控，及时发现问题
5. **性能优化**：根据实际使用情况调整 Gunicorn 工作进程数

此部署流程适用于生产环境，确保了应用的稳定性和安全性。