# API文档

## 1. 认证相关API

### 1.1 注册用户
- **端点**: `POST /api/auth/register`
- **功能**: 注册新用户
- **请求体**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **响应**:
  - 成功: `201 Created`
    ```json
    {"message": "User registered successfully"}
    ```
  - 失败: `400 Bad Request`
    ```json
    {"message": "Username already exists"}
    ```
    或
    ```json
    {"message": "Email already exists"}
    ```

### 1.2 用户登录
- **端点**: `POST /api/auth/login`
- **功能**: 用户登录
- **请求体**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "message": "Login successful",
      "user": {
        "id": 1,
        "username": "string",
        "email": "string",
        "role": "string",
        "created_at": "string"
      }
    }
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Invalid username or password"}
    ```

### 1.3 用户登出
- **端点**: `POST /api/auth/logout`
- **功能**: 用户登出
- **响应**:
  - 成功: `200 OK`
    ```json
    {"message": "Logout successful"}
    ```

### 1.4 获取当前用户信息
- **端点**: `GET /api/auth/me`
- **功能**: 获取当前登录用户信息
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "id": 1,
      "username": "string",
      "email": "string",
      "role": "string",
      "created_at": "string"
    }
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```

## 2. 任务管理API

### 2.1 获取所有任务
- **端点**: `GET /api/todos`
- **功能**: 获取所有待办事项
- **响应**:
  - 成功: `200 OK`
    ```json
    [
      {
        "id": 1,
        "title": "string",
        "description": "string",
        "assignee_id": 1,
        "assignee": "string",
        "start_time": "string",
        "end_time": "string",
        "priority": 0,
        "status": "pending",
        "completed": false,
        "created_at": "string"
      }
    ]
    ```

### 2.2 创建新任务
- **端点**: `POST /api/todos`
- **功能**: 创建新的待办事项
- **请求体**:
  ```json
  {
    "title": "string",
    "description": "string",
    "assignee_id": 1,
    "start_time": "string",
    "end_time": "string",
    "priority": 0,
    "status": "pending"
  }
  ```
- **响应**:
  - 成功: `201 Created`
    ```json
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "assignee_id": 1,
      "assignee": "string",
      "start_time": "string",
      "end_time": "string",
      "priority": 0,
      "status": "pending",
      "completed": false,
      "created_at": "string"
    }
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```

### 2.3 获取单个任务
- **端点**: `GET /api/todos/<id>`
- **功能**: 获取单个待办事项
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "assignee_id": 1,
      "assignee": "string",
      "start_time": "string",
      "end_time": "string",
      "priority": 0,
      "status": "pending",
      "completed": false,
      "created_at": "string"
    }
    ```
  - 失败: `404 Not Found`
    ```json
    {"message": "Todo not found"}
    ```

### 2.4 更新任务
- **端点**: `PUT /api/todos/<id>`
- **功能**: 更新待办事项
- **请求体**:
  ```json
  {
    "title": "string",
    "description": "string",
    "assignee_id": 1,
    "start_time": "string",
    "end_time": "string",
    "priority": 0,
    "status": "pending",
    "completed": false
  }
  ```
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "assignee_id": 1,
      "assignee": "string",
      "start_time": "string",
      "end_time": "string",
      "priority": 0,
      "status": "pending",
      "completed": false,
      "created_at": "string"
    }
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```
  - 失败: `404 Not Found`
    ```json
    {"message": "Todo not found"}
    ```

### 2.5 删除任务
- **端点**: `DELETE /api/todos/<id>`
- **功能**: 删除待办事项
- **响应**:
  - 成功: `200 OK`
    ```json
    {"message": "Todo deleted"}
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```
  - 失败: `404 Not Found`
    ```json
    {"message": "Todo not found"}
    ```

### 2.6 更新任务状态
- **端点**: `PATCH /api/todos/<id>/status`
- **功能**: 更新任务状态
- **请求体**:
  ```json
  {
    "status": "string"
  }
  ```
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "assignee_id": 1,
      "assignee": "string",
      "start_time": "string",
      "end_time": "string",
      "priority": 0,
      "status": "string",
      "completed": false,
      "created_at": "string"
    }
    ```
  - 失败: `400 Bad Request`
    ```json
    {"message": "Status is required"}
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```
  - 失败: `404 Not Found`
    ```json
    {"message": "Todo not found"}
    ```

## 3. 任务依赖关系API

### 3.1 创建任务依赖关系
- **端点**: `POST /api/task-dependencies`
- **功能**: 创建任务依赖关系
- **请求体**:
  ```json
  {
    "task_id": 1,
    "dependency_id": 2
  }
  ```
- **响应**:
  - 成功: `201 Created`
    ```json
    {
      "id": 1,
      "task_id": 1,
      "dependency_id": 2,
      "created_at": "string"
    }
    ```
  - 失败: `400 Bad Request`
    ```json
    {"message": "Task ID and Dependency ID are required"}
    ```
    或
    ```json
    {"message": "Dependency already exists"}
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```
  - 失败: `404 Not Found`
    ```json
    {"message": "Task not found"}
    ```
    或
    ```json
    {"message": "Dependency task not found"}
    ```

### 3.2 删除任务依赖关系
- **端点**: `DELETE /api/task-dependencies/<id>`
- **功能**: 删除任务依赖关系
- **响应**:
  - 成功: `200 OK`
    ```json
    {"message": "Dependency deleted"}
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```
  - 失败: `404 Not Found`
    ```json
    {"message": "Dependency not found"}
    ```

### 3.3 获取任务依赖关系
- **端点**: `GET /api/todos/<id>/dependencies`
- **功能**: 获取任务的依赖项和依赖于该任务的其他任务
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "dependencies": [
        {
          "id": 1,
          "dependency_id": 2,
          "dependency_title": "string",
          "created_at": "string"
        }
      ],
      "dependents": [
        {
          "id": 2,
          "task_id": 3,
          "dependent_title": "string",
          "created_at": "string"
        }
      ]
    }
    ```

## 4. 数据统计API

### 4.1 甘特图数据
- **端点**: `GET /api/gantt-data`
- **功能**: 获取甘特图数据
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "tasks": [
        {
          "id": 1,
          "text": "string",
          "start_date": "string",
          "end_date": "string",
          "progress": 0,
          "assignee": "string",
          "status": "string"
        }
      ],
      "links": [
        {
          "id": 1,
          "source": 2,
          "target": 1,
          "type": "0"
        }
      ]
    }
    ```

### 4.2 任务时间线
- **端点**: `GET /api/timeline`
- **参数**:
  - `start_date`: 开始日期 (可选)
  - `end_date`: 结束日期 (可选)
- **功能**: 获取指定时间范围内的任务
- **响应**:
  - 成功: `200 OK`
    ```json
    [
      {
        "id": 1,
        "title": "string",
        "description": "string",
        "assignee_id": 1,
        "assignee": "string",
        "start_time": "string",
        "end_time": "string",
        "priority": 0,
        "status": "string",
        "completed": false,
        "created_at": "string"
      }
    ]
    ```

### 4.3 任务完成情况统计
- **端点**: `GET /api/stats/completion`
- **功能**: 获取任务完成情况统计
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "total_tasks": 10,
      "completed_tasks": 5,
      "pending_tasks": 5,
      "completion_rate": 50,
      "status_stats": [
        {"status": "pending", "count": 3},
        {"status": "in_progress", "count": 2},
        {"status": "completed", "count": 5}
      ],
      "user_stats": [
        {
          "username": "user1",
          "total_tasks": 5,
          "completed_tasks": 3,
          "completion_rate": 60
        }
      ]
    }
    ```

### 4.4 延期预警
- **端点**: `GET /api/stats/overdue`
- **功能**: 获取已过期和即将过期的任务
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "overdue_tasks": [
        {
          "id": 1,
          "title": "string",
          "assignee": "string",
          "end_time": "string",
          "overdue_days": 2
        }
      ],
      "soon_overdue_tasks": [
        {
          "id": 2,
          "title": "string",
          "assignee": "string",
          "end_time": "string",
          "hours_until_deadline": 12
        }
      ],
      "total_overdue": 1,
      "total_soon_overdue": 1
    }
    ```

### 4.5 报表数据
- **端点**: `GET /api/stats/report`
- **参数**:
  - `start_date`: 开始日期 (可选)
  - `end_date`: 结束日期 (可选)
- **功能**: 获取报表数据
- **响应**:
  - 成功: `200 OK`
    ```json
    {
      "total_tasks": 10,
      "completed_tasks": 5,
      "completion_rate": 50,
      "status_distribution": {
        "pending": 3,
        "in_progress": 2,
        "completed": 5
      },
      "user_distribution": {
        "user1": {
          "total": 5,
          "completed": 3
        }
      },
      "priority_distribution": {
        "0": 5,
        "1": 3,
        "2": 2
      },
      "time_range": {
        "start_date": "string",
        "end_date": "string"
      }
    }
    ```

## 5. 管理员API

### 5.1 获取所有用户
- **端点**: `GET /api/admin/users`
- **功能**: 获取所有用户信息 (需要管理员权限)
- **响应**:
  - 成功: `200 OK`
    ```json
    [
      {
        "id": 1,
        "username": "string",
        "email": "string",
        "role": "string",
        "created_at": "string"
      }
    ]
    ```
  - 失败: `401 Unauthorized`
    ```json
    {"message": "Unauthorized"}
    ```
  - 失败: `403 Forbidden`
    ```json
    {"message": "Insufficient permissions"}
    ```