from flask import jsonify, request, session
from app import app, db, bcrypt, cache
from app.models import User, Todo, TaskDependency, Role
from datetime import datetime, timedelta

# 生成密码哈希
def generate_password_hash(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# 验证密码
def check_password_hash(password_hash, password):
    return bcrypt.check_password_hash(password_hash, password)

# 注册路由
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    # 检查邮箱是否已存在
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    # 生成密码哈希
    password_hash = generate_password_hash(data['password'])
    
    # 创建用户
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        role_id=1  # 默认角色为普通用户
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# 登录路由
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 查找用户
    user = User.query.filter_by(username=data['username']).first()
    
    # 验证用户和密码
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # 创建会话
    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role.name
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.name,
            'created_at': user.created_at.isoformat()
        }
    })

# 登出路由
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'})

# 获取当前用户信息
@app.route('/api/auth/me', methods=['GET'])
def get_me():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role.name,
        'created_at': user.created_at.isoformat()
    })

# 权限检查装饰器
def require_role(role_name):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'message': 'Unauthorized'}), 401
            
            if session['role'] != role_name:
                return jsonify({'message': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 需要管理员权限的路由示例
@app.route('/api/admin/users', methods=['GET'])
@require_role('admin')
def get_all_users():
    users = User.query.all()
    
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role.name,
        'created_at': user.created_at.isoformat()
    } for user in users])

# Todo路由
@app.route('/api/todos', methods=['GET'])
@cache.cached(timeout=300, key_prefix='todos')
def get_todos():
    todos = Todo.query.all()
    
    return jsonify([{
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'assignee_id': todo.assignee_id,
        'assignee': todo.assignee.username if todo.assignee else None,
        'start_time': todo.start_time.isoformat() if todo.start_time else None,
        'end_time': todo.end_time.isoformat() if todo.end_time else None,
        'priority': todo.priority,
        'status': todo.status,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    } for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # 创建todo
    new_todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        assignee_id=data.get('assignee_id'),
        start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
        end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
        priority=data.get('priority', 0),
        status=data.get('status', 'pending')
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    # 清除缓存
    cache.delete('todos')
    
    return jsonify({
        'id': new_todo.id,
        'title': new_todo.title,
        'description': new_todo.description,
        'assignee_id': new_todo.assignee_id,
        'assignee': new_todo.assignee.username if new_todo.assignee else None,
        'start_time': new_todo.start_time.isoformat() if new_todo.start_time else None,
        'end_time': new_todo.end_time.isoformat() if new_todo.end_time else None,
        'priority': new_todo.priority,
        'status': new_todo.status,
        'completed': new_todo.completed,
        'created_at': new_todo.created_at.isoformat()
    }), 201

@app.route('/api/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'assignee_id': todo.assignee_id,
        'assignee': todo.assignee.username if todo.assignee else None,
        'start_time': todo.start_time.isoformat() if todo.start_time else None,
        'end_time': todo.end_time.isoformat() if todo.end_time else None,
        'priority': todo.priority,
        'status': todo.status,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    })

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    todo = Todo.query.get(id)
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    # 更新todo
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.assignee_id = data.get('assignee_id', todo.assignee_id)
    todo.start_time = datetime.fromisoformat(data['start_time']) if data.get('start_time') else todo.start_time
    todo.end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else todo.end_time
    todo.priority = data.get('priority', todo.priority)
    todo.status = data.get('status', todo.status)
    todo.completed = data.get('completed', todo.completed)
    
    db.session.commit()
    
    # 清除缓存
    cache.delete('todos')
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'assignee_id': todo.assignee_id,
        'assignee': todo.assignee.username if todo.assignee else None,
        'start_time': todo.start_time.isoformat() if todo.start_time else None,
        'end_time': todo.end_time.isoformat() if todo.end_time else None,
        'priority': todo.priority,
        'status': todo.status,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    })

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    todo = Todo.query.get(id)
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    db.session.delete(todo)
    db.session.commit()
    
    # 清除缓存
    cache.delete('todos')
    
    return jsonify({'message': 'Todo deleted'})

# 更新任务状态的路由
@app.route('/api/todos/<int:id>/status', methods=['PATCH'])
def update_todo_status(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    if 'status' not in data:
        return jsonify({'message': 'Status is required'}), 400
    
    todo = Todo.query.get(id)
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    # 更新状态
    todo.status = data['status']
    
    # 自动更新completed状态
    if data['status'] == 'completed':
        todo.completed = True
    elif data['status'] != 'completed':
        todo.completed = False
    
    db.session.commit()
    
    # 清除缓存
    cache.delete('todos')
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'assignee_id': todo.assignee_id,
        'assignee': todo.assignee.username if todo.assignee else None,
        'start_time': todo.start_time.isoformat() if todo.start_time else None,
        'end_time': todo.end_time.isoformat() if todo.end_time else None,
        'priority': todo.priority,
        'status': todo.status,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    })

# 任务依赖关系路由
@app.route('/api/task-dependencies', methods=['POST'])
def create_task_dependency():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    if 'task_id' not in data or 'dependency_id' not in data:
        return jsonify({'message': 'Task ID and Dependency ID are required'}), 400
    
    # 检查任务是否存在
    task = Todo.query.get(data['task_id'])
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    # 检查依赖任务是否存在
    dependency_task = Todo.query.get(data['dependency_id'])
    if not dependency_task:
        return jsonify({'message': 'Dependency task not found'}), 404
    
    # 检查依赖关系是否已存在
    existing_dependency = TaskDependency.query.filter_by(
        task_id=data['task_id'],
        dependency_id=data['dependency_id']
    ).first()
    if existing_dependency:
        return jsonify({'message': 'Dependency already exists'}), 400
    
    # 创建依赖关系
    new_dependency = TaskDependency(
        task_id=data['task_id'],
        dependency_id=data['dependency_id']
    )
    
    db.session.add(new_dependency)
    db.session.commit()
    
    return jsonify({
        'id': new_dependency.id,
        'task_id': new_dependency.task_id,
        'dependency_id': new_dependency.dependency_id,
        'created_at': new_dependency.created_at.isoformat()
    }), 201

@app.route('/api/task-dependencies/<int:id>', methods=['DELETE'])
def delete_task_dependency(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    dependency = TaskDependency.query.get(id)
    
    if not dependency:
        return jsonify({'message': 'Dependency not found'}), 404
    
    db.session.delete(dependency)
    db.session.commit()
    
    return jsonify({'message': 'Dependency deleted'})

@app.route('/api/todos/<int:id>/dependencies', methods=['GET'])
def get_task_dependencies(id):
    # 获取任务的依赖项
    dependencies = TaskDependency.query.filter_by(task_id=id).all()
    
    # 获取依赖于该任务的其他任务
    dependents = TaskDependency.query.filter_by(dependency_id=id).all()
    
    return jsonify({
        'dependencies': [{
            'id': dep.id,
            'dependency_id': dep.dependency_id,
            'dependency_title': Todo.query.get(dep.dependency_id).title if Todo.query.get(dep.dependency_id) else None,
            'created_at': dep.created_at.isoformat()
        } for dep in dependencies],
        'dependents': [{
            'id': dep.id,
            'task_id': dep.task_id,
            'dependent_title': Todo.query.get(dep.task_id).title if Todo.query.get(dep.task_id) else None,
            'created_at': dep.created_at.isoformat()
        } for dep in dependents]
    })

# 甘特图数据接口
@app.route('/api/gantt-data', methods=['GET'])
def get_gantt_data():
    # 获取所有任务
    todos = Todo.query.all()
    
    # 获取所有依赖关系
    dependencies = TaskDependency.query.all()
    
    # 构建甘特图数据
    gantt_data = []
    for todo in todos:
        gantt_data.append({
            'id': todo.id,
            'text': todo.title,
            'start_date': todo.start_time.isoformat() if todo.start_time else None,
            'end_date': todo.end_time.isoformat() if todo.end_time else None,
            'progress': 1 if todo.completed else 0,
            'assignee': todo.assignee.username if todo.assignee else None,
            'status': todo.status
        })
    
    # 构建依赖关系数据
    links = []
    for dep in dependencies:
        links.append({
            'id': dep.id,
            'source': dep.dependency_id,
            'target': dep.task_id,
            'type': '0'
        })
    
    return jsonify({
        'tasks': gantt_data,
        'links': links
    })

# 任务时间线查询
@app.route('/api/timeline', methods=['GET'])
def get_timeline():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 构建查询
    query = Todo.query
    
    if start_date:
        query = query.filter((Todo.start_time >= start_date) | (Todo.end_time >= start_date))
    
    if end_date:
        query = query.filter((Todo.start_time <= end_date) | (Todo.end_time <= end_date))
    
    # 按开始时间排序
    todos = query.order_by(Todo.start_time.asc()).all()
    
    return jsonify([{
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'assignee_id': todo.assignee_id,
        'assignee': todo.assignee.username if todo.assignee else None,
        'start_time': todo.start_time.isoformat() if todo.start_time else None,
        'end_time': todo.end_time.isoformat() if todo.end_time else None,
        'priority': todo.priority,
        'status': todo.status,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat()
    } for todo in todos])

# 任务完成情况统计
@app.route('/api/stats/completion', methods=['GET'])
def get_completion_stats():
    # 总任务数
    total_tasks = Todo.query.count()
    
    # 已完成任务数
    completed_tasks = Todo.query.filter_by(completed=True).count()
    
    # 未完成任务数
    pending_tasks = Todo.query.filter_by(completed=False).count()
    
    # 按状态统计
    from sqlalchemy import func
    status_stats = db.session.query(Todo.status, func.count(Todo.id)).group_by(Todo.status).all()
    
    # 按用户统计
    user_stats = db.session.query(
        User.username,
        func.count(Todo.id).label('total'),
        func.sum(func.case([(Todo.completed == True, 1)], else_=0)).label('completed')
    ).outerjoin(Todo, User.id == Todo.assignee_id).group_by(User.id).all()
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': round(completed_tasks / total_tasks * 100, 2) if total_tasks > 0 else 0,
        'status_stats': [{'status': stat[0], 'count': stat[1]} for stat in status_stats],
        'user_stats': [{
            'username': stat.username,
            'total_tasks': stat.total or 0,
            'completed_tasks': stat.completed or 0,
            'completion_rate': round((stat.completed or 0) / (stat.total or 1) * 100, 2)
        } for stat in user_stats]
    })

# 延期预警功能
@app.route('/api/stats/overdue', methods=['GET'])
def get_overdue_tasks():
    # 获取当前时间
    now = datetime.now()
    
    # 已过期任务
    overdue_tasks = Todo.query.filter(
        Todo.end_time < now,
        Todo.completed == False
    ).all()
    
    # 即将过期任务（24小时内）
    soon_deadline = now + timedelta(hours=24)
    soon_overdue_tasks = Todo.query.filter(
        Todo.end_time >= now,
        Todo.end_time <= soon_deadline,
        Todo.completed == False
    ).all()
    
    return jsonify({
        'overdue_tasks': [{
            'id': task.id,
            'title': task.title,
            'assignee': task.assignee.username if task.assignee else None,
            'end_time': task.end_time.isoformat() if task.end_time else None,
            'overdue_days': (now - task.end_time).days if task.end_time else 0
        } for task in overdue_tasks],
        'soon_overdue_tasks': [{
            'id': task.id,
            'title': task.title,
            'assignee': task.assignee.username if task.assignee else None,
            'end_time': task.end_time.isoformat() if task.end_time else None,
            'hours_until_deadline': ((task.end_time - now).total_seconds()) / 3600 if task.end_time else 0
        } for task in soon_overdue_tasks],
        'total_overdue': len(overdue_tasks),
        'total_soon_overdue': len(soon_overdue_tasks)
    })

# 报表数据接口
@app.route('/api/stats/report', methods=['GET'])
def get_report_data():
    # 时间范围参数
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 构建查询
    query = Todo.query
    
    if start_date:
        query = query.filter(Todo.created_at >= start_date)
    
    if end_date:
        query = query.filter(Todo.created_at <= end_date)
    
    # 执行查询
    tasks = query.all()
    
    # 统计数据
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    
    # 按状态统计
    status_count = {}
    for task in tasks:
        status = task.status
        if status not in status_count:
            status_count[status] = 0
        status_count[status] += 1
    
    # 按用户统计
    user_count = {}
    for task in tasks:
        user = task.assignee.username if task.assignee else 'Unassigned'
        if user not in user_count:
            user_count[user] = {'total': 0, 'completed': 0}
        user_count[user]['total'] += 1
        if task.completed:
            user_count[user]['completed'] += 1
    
    # 按优先级统计
    priority_count = {}
    for task in tasks:
        priority = task.priority
        if priority not in priority_count:
            priority_count[priority] = 0
        priority_count[priority] += 1
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': round(completed_tasks / total_tasks * 100, 2) if total_tasks > 0 else 0,
        'status_distribution': status_count,
        'user_distribution': user_count,
        'priority_distribution': priority_count,
        'time_range': {
            'start_date': start_date,
            'end_date': end_date
        }
    })