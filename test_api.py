import requests
import json

# 测试登录
def test_login():
    url = 'http://127.0.0.1:5000/api/auth/login'
    data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = requests.post(url, json=data)
    print('Login response:', response.status_code, response.json())
    return response.cookies

# 测试获取任务
def test_get_todos(cookies):
    url = 'http://127.0.0.1:5000/api/todos'
    response = requests.get(url, cookies=cookies)
    print('Get todos response:', response.status_code, response.json())

# 测试创建任务
def test_create_todo(cookies):
    url = 'http://127.0.0.1:5000/api/todos'
    data = {
        'title': '测试任务',
        'description': '这是一个测试任务',
        'status': 'pending',
        'priority': 1
    }
    response = requests.post(url, json=data, cookies=cookies)
    print('Create todo response:', response.status_code, response.json())
    return response.json().get('id')

# 测试更新任务
def test_update_todo(cookies, todo_id):
    url = f'http://127.0.0.1:5000/api/todos/{todo_id}'
    data = {
        'status': 'in_progress'
    }
    response = requests.put(url, json=data, cookies=cookies)
    print('Update todo response:', response.status_code, response.json())

# 测试删除任务
def test_delete_todo(cookies, todo_id):
    url = f'http://127.0.0.1:5000/api/todos/{todo_id}'
    response = requests.delete(url, cookies=cookies)
    print('Delete todo response:', response.status_code, response.json())

# 测试获取统计数据
def test_get_stats():
    url = 'http://127.0.0.1:5000/api/stats/completion'
    response = requests.get(url)
    print('Get stats response:', response.status_code, response.json())

if __name__ == '__main__':
    print('Testing Flask API...')
    cookies = test_login()
    test_get_todos(cookies)
    todo_id = test_create_todo(cookies)
    if todo_id:
        test_update_todo(cookies, todo_id)
        test_get_todos(cookies)
        test_delete_todo(cookies, todo_id)
        test_get_todos(cookies)
    test_get_stats()
    print('API testing completed!')
