# TodoList 系统部署文档

## 1. 环境要求

- Python 3.7+
- Node.js 14+
- pip 20.0+
- npm 6.0+

## 2. 服务器配置

- 推荐配置：2核CPU，4GB内存，50GB磁盘空间
- 操作系统：Ubuntu 20.04 LTS 或 CentOS 7+
- 网络：开放5000端口（或根据配置修改）

## 3. 部署步骤

### 3.1 安装依赖

#### 3.1.1 安装Python依赖

```bash
# 克隆代码仓库
git clone <repository-url> todo-list
cd todo-list

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

#### 3.1.2 安装前端依赖并构建

```bash
# 进入前端目录
cd frontend

# 安装前端依赖
npm install

# 构建前端项目
npm run build

# 回到项目根目录
cd ..
```

### 3.2 配置环境变量

创建 `.env` 文件，设置以下环境变量：

```env
# 环境变量配置
SECRET_KEY=your-production-secret-key-here
# 数据库连接配置（如果使用PostgreSQL或MySQL）
# DATABASE_URL=postgresql://username:password@localhost:5432/todo
# 服务器配置
# SERVER_NAME=your-domain.com
```

### 3.3 初始化数据库

```bash
# 运行初始化脚本
python init_db.py
```

### 3.4 启动应用

#### 3.4.1 使用Gunicorn启动（推荐）

```bash
# 启动Gunicorn服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 3.4.2 使用Flask内置服务器启动（仅用于开发）

```bash
# 启动Flask内置服务器
python app.py
```

## 4. 配置域名和SSL

### 4.1 配置Nginx反向代理

安装Nginx：

```bash
sudo apt update
sudo apt install nginx
```

创建Nginx配置文件：

```bash
sudo nano /etc/nginx/sites-available/todo-list
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/todo-list /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4.2 配置SSL（使用Let's Encrypt）

安装Certbot：

```bash
sudo apt install certbot python3-certbot-nginx
```

获取SSL证书：

```bash
sudo certbot --nginx -d your-domain.com
```

## 5. 监控和日志

### 5.1 日志配置

应用日志会保存在 `logs/app.log` 文件中，同时会输出到控制台。

### 5.2 监控设置

可以使用以下工具进行监控：

- **Prometheus + Grafana**：监控系统性能和应用状态
- **ELK Stack**：收集和分析日志
- **Uptime Robot**：监控网站可用性

## 6. 维护注意事项

### 6.1 定期备份

定期备份数据库和配置文件：

```bash
# 备份数据库
sqlite3 todo.db ".backup backup_$(date +%Y%m%d).db"

# 备份配置文件
cp .env backup_env_$(date +%Y%m%d).env
```

### 6.2 安全更新

定期更新依赖包和系统：

```bash
# 更新Python依赖
pip install --upgrade -r requirements.txt

# 更新系统
apt update && apt upgrade -y
```

### 6.3 性能优化

- 调整Gunicorn进程数：根据服务器CPU核心数调整 `-w` 参数
- 使用缓存：默认使用简单缓存，可根据需要配置Redis等高级缓存
- 数据库优化：对于大型应用，考虑使用PostgreSQL或MySQL

## 7. 故障排查

### 7.1 常见问题

1. **无法访问应用**：检查服务器防火墙是否开放5000端口，或Nginx配置是否正确
2. **数据库连接错误**：检查数据库配置和权限
3. **前端资源无法加载**：确保前端构建文件已正确部署
4. **性能问题**：检查服务器资源使用情况，调整Gunicorn配置

### 7.2 日志分析

查看应用日志：

```bash
tail -f logs/app.log
```

查看Nginx日志：

```bash
tail -f /var/log/nginx/error.log
```

## 8. 部署脚本

项目根目录下的 `deploy.sh` 脚本可用于快速部署：

```bash
#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动gunicorn服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 9. 总结

本部署文档提供了TodoList系统的完整部署流程，包括环境搭建、依赖安装、配置设置、部署步骤和维护注意事项。按照文档中的步骤操作，可以确保系统安全稳定运行。