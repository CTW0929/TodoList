import requests
import json

# 测试基地址
BASE_URL = 'http://127.0.0.1:5000/api'

# 测试步骤
print("=== 测试任务 CRUD 接口 ===")

# 1. 注册用户
print("\n1. 注册用户")
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print(f"注册响应: {response.status_code} - {response.json()}")

# 2. 登录
print("\n2. 登录")
login_data = {
    "username": "testuser",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"登录响应: {response.status_code} - {response.json()}")
token = response.cookies.get('session')
cookies = {'session': token}

# 3. 创建任务
print("\n3. 创建任务")
task_data = {
    "title": "测试任务",
    "description": "这是一个测试任务",
    "assignee_id": 1,
    "start_time": "2026-03-03T00:00:00",
    "end_time": "2026-03-10T00:00:00",
    "priority": 1,
    "status": "pending"
}
response = requests.post(f"{BASE_URL}/todos", json=task_data, cookies=cookies)
print(f"创建任务响应: {response.status_code} - {response.json()}")
task_id = response.json().get('id')

# 4. 获取所有任务
print("\n4. 获取所有任务")
response = requests.get(f"{BASE_URL}/todos", cookies=cookies)
print(f"获取任务响应: {response.status_code}")
print(f"任务列表: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

# 5. 获取单个任务
print("\n5. 获取单个任务")
response = requests.get(f"{BASE_URL}/todos/{task_id}", cookies=cookies)
print(f"获取单个任务响应: {response.status_code} - {response.json()}")

# 6. 更新任务
print("\n6. 更新任务")
update_data = {
    "title": "更新后的测试任务",
    "description": "这是更新后的测试任务",
    "priority": 2,
    "status": "in_progress"
}
response = requests.put(f"{BASE_URL}/todos/{task_id}", json=update_data, cookies=cookies)
print(f"更新任务响应: {response.status_code} - {response.json()}")

# 7. 更新任务状态
print("\n7. 更新任务状态")
status_data = {
    "status": "completed"
}
response = requests.patch(f"{BASE_URL}/todos/{task_id}/status", json=status_data, cookies=cookies)
print(f"更新任务状态响应: {response.status_code} - {response.json()}")

# 8. 删除任务
print("\n8. 删除任务")
response = requests.delete(f"{BASE_URL}/todos/{task_id}", cookies=cookies)
print(f"删除任务响应: {response.status_code} - {response.json()}")

# 9. 再次获取所有任务，确认任务已删除
print("\n9. 再次获取所有任务")
response = requests.get(f"{BASE_URL}/todos", cookies=cookies)
print(f"获取任务响应: {response.status_code}")
print(f"任务列表: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

print("\n=== 测试完成 ===")
