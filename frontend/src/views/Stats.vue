<template>
  <div class="stats-container">
    <el-card class="stats-card">
      <template #header>
        <div class="stats-header">
          <h2>数据统计</h2>
        </div>
      </template>
      <div class="stats-grid">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">总任务数</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ stats.completed }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ stats.inProgress }}</div>
            <div class="stat-label">进行中</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ stats.pending }}</div>
            <div class="stat-label">待办</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ stats.completionRate }}%</div>
            <div class="stat-label">完成率</div>
          </div>
        </el-card>
      </div>
      <div class="charts-container">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <h3>任务状态分布</h3>
            </div>
          </template>
          <canvas ref="statusChart" width="400" height="300"></canvas>
        </el-card>
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <h3>任务优先级分布</h3>
            </div>
          </template>
          <canvas ref="priorityChart" width="400" height="300"></canvas>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import Chart from 'chart.js/auto'

const store = useStore()
const statusChart = ref(null)
const priorityChart = ref(null)
let statusChartInstance = null
let priorityChartInstance = null

const stats = computed(() => store.getters.taskStats)
const tasks = computed(() => store.getters.getTasks)

const initCharts = () => {
  initStatusChart()
  initPriorityChart()
}

const initStatusChart = () => {
  if (statusChart.value) {
    const ctx = statusChart.value.getContext('2d')
    statusChartInstance = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['待办', '进行中', '已完成'],
        datasets: [{
          data: [stats.value.pending, stats.value.inProgress, stats.value.completed],
          backgroundColor: ['#909399', '#E6A23C', '#67C23A'],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }
}

const initPriorityChart = () => {
  if (priorityChart.value) {
    const ctx = priorityChart.value.getContext('2d')
    
    // 计算优先级分布
    const priorityCounts = {
      high: 0,
      medium: 0,
      low: 0
    }
    
    tasks.value.forEach(task => {
      priorityCounts[task.priority]++
    })
    
    priorityChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['高', '中', '低'],
        datasets: [{
          label: '任务数量',
          data: [priorityCounts.high, priorityCounts.medium, priorityCounts.low],
          backgroundColor: ['#F56C6C', '#E6A23C', '#67C23A'],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0
            }
          }
        }
      }
    })
  }
}

const updateCharts = () => {
  if (statusChartInstance) {
    statusChartInstance.data.datasets[0].data = [stats.value.pending, stats.value.inProgress, stats.value.completed]
    statusChartInstance.update()
  }
  
  if (priorityChartInstance) {
    const priorityCounts = {
      high: 0,
      medium: 0,
      low: 0
    }
    
    tasks.value.forEach(task => {
      priorityCounts[task.priority]++
    })
    
    priorityChartInstance.data.datasets[0].data = [priorityCounts.high, priorityCounts.medium, priorityCounts.low]
    priorityChartInstance.update()
  }
}

onMounted(() => {
  store.dispatch('fetchTasks')
  setTimeout(() => {
    initCharts()
  }, 100)
})
</script>

<style scoped>
.stats-container {
  width: 100%;
}

.stats-card {
  margin-bottom: 20px;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-header h2 {
  margin: 0;
  color: #409EFF;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
}

.stat-item {
  padding: 20px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 16px;
  color: #606266;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-header h3 {
  margin: 0;
  color: #606266;
}
</style>