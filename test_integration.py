import requests
import json

# 测试Flask API与前端集成
class IntegrationTest:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000/api'
        self.cookies = {}
    
    def test_login(self):
        """测试登录功能"""
        print("\n=== 测试登录功能 ===")
        url = f'{self.base_url}/auth/login'
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = requests.post(url, json=data)
        print(f'登录响应: {response.status_code}')
        print(f'登录数据: {response.json()}')
        
        if response.status_code == 200:
            self.cookies = response.cookies
            print('登录成功，获取到会话')
            return True
        else:
            print('登录失败')
            return False
    
    def test_get_todos(self):
        """测试获取任务列表"""
        print("\n=== 测试获取任务列表 ===")
        url = f'{self.base_url}/todos'
        response = requests.get(url, cookies=self.cookies)
        print(f'获取任务响应: {response.status_code}')
        print(f'任务数据: {response.json()}')
        return response.status_code == 200
    
    def test_create_todo(self):
        """测试创建任务"""
        print("\n=== 测试创建任务 ===")
        url = f'{self.base_url}/todos'
        data = {
            'title': '集成测试任务',
            'description': '这是一个集成测试任务',
            'status': 'pending',
            'priority': 1,
            'start_time': '2026-03-03',
            'end_time': '2026-03-10'
        }
        response = requests.post(url, json=data, cookies=self.cookies)
        print(f'创建任务响应: {response.status_code}')
        print(f'创建的任务: {response.json()}')
        
        if response.status_code == 201:
            self.todo_id = response.json().get('id')
            print(f'创建任务成功，任务ID: {self.todo_id}')
            return True
        else:
            print('创建任务失败')
            return False
    
    def test_update_todo(self):
        """测试更新任务"""
        print("\n=== 测试更新任务 ===")
        url = f'{self.base_url}/todos/{self.todo_id}'
        data = {
            'status': 'in_progress',
            'priority': 2
        }
        response = requests.put(url, json=data, cookies=self.cookies)
        print(f'更新任务响应: {response.status_code}')
        print(f'更新后的任务: {response.json()}')
        return response.status_code == 200
    
    def test_delete_todo(self):
        """测试删除任务"""
        print("\n=== 测试删除任务 ===")
        url = f'{self.base_url}/todos/{self.todo_id}'
        response = requests.delete(url, cookies=self.cookies)
        print(f'删除任务响应: {response.status_code}')
        print(f'删除结果: {response.json()}')
        return response.status_code == 200
    
    def test_stats(self):
        """测试统计数据接口"""
        print("\n=== 测试统计数据接口 ===")
        url = f'{self.base_url}/stats/completion'
        response = requests.get(url)
        print(f'获取统计数据响应: {response.status_code}')
        print(f'统计数据: {response.json()}')
        return response.status_code == 200
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始集成测试...")
        
        tests = [
            ('登录测试', self.test_login),
            ('获取任务测试', self.test_get_todos),
            ('创建任务测试', self.test_create_todo),
            ('更新任务测试', self.test_update_todo),
            ('删除任务测试', self.test_delete_todo),
            ('统计数据测试', self.test_stats)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    print(f'✅ {test_name} 通过')
                    passed += 1
                else:
                    print(f'❌ {test_name} 失败')
                    failed += 1
            except Exception as e:
                print(f'❌ {test_name} 异常: {str(e)}')
                failed += 1
        
        print(f"\n测试完成: 通过 {passed}, 失败 {failed}")
        return passed == len(tests)

if __name__ == '__main__':
    test = IntegrationTest()
    test.run_all_tests()
