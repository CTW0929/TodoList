<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>登录</h2>
        </div>
      </template>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" style="width: 100%;">登录</el-button>
        </el-form-item>
        <el-form-item style="text-align: center;">
          <span>还没有账号？</span>
          <el-button type="text" @click="$router.push('/register')">立即注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
const loginFormRef = ref(null)

const loginForm = ref({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

import { ElMessage } from 'element-plus'

const handleLogin = async () => {
  if (loginFormRef.value) {
    await loginFormRef.value.validate(async (valid) => {
      if (valid) {
        try {
          await store.dispatch('login', {
            username: loginForm.value.username,
            password: loginForm.value.password
          })
          ElMessage.success('登录成功')
          router.push('/tasks')
        } catch (error) {
          ElMessage.error('登录失败：' + (error.response?.data?.message || '请检查用户名和密码'))
        }
      }
    })
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.login-header {
  text-align: center;
  padding: 20px 0;
}

.login-header h2 {
  margin: 0;
  color: #409EFF;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  height: 40px;
  font-size: 16px;
}
</style>