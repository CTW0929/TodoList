<template>
  <div id="app">
    <el-container>
      <el-header v-if="isAuthenticated">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="tasks">任务管理</el-menu-item>
          <el-menu-item index="gantt">甘特图</el-menu-item>
          <el-menu-item index="stats">数据统计</el-menu-item>
          <el-menu-item index="logout" style="float: right;">退出登录</el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const isAuthenticated = computed(() => store.state.isAuthenticated)
const activeIndex = computed(() => {
  const path = router.currentRoute.value.path
  if (path === '/tasks') return 'tasks'
  if (path === '/gantt') return 'gantt'
  if (path === '/stats') return 'stats'
  return 'tasks'
})

const handleSelect = (key) => {
  if (key === 'logout') {
    store.commit('logout')
    router.push('/login')
  } else {
    router.push(`/${key}`)
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-header {
  background-color: #409EFF;
  color: white;
  padding: 0;
  height: 60px;
}

.el-menu-demo {
  background-color: transparent;
  border-bottom: none;
}

.el-menu-item {
  color: white;
  height: 60px;
  line-height: 60px;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.el-menu-item.is-active {
  color: white;
  background-color: rgba(255, 255, 255, 0.2);
}

.el-main {
  padding: 20px;
  overflow-y: auto;
}
</style>