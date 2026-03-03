<template>
  <div class="gantt-container">
    <el-card class="gantt-card">
      <template #header>
        <div class="gantt-header">
          <h2>甘特图</h2>
        </div>
      </template>
      <div ref="ganttContainer" class="gantt-chart"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useStore } from 'vuex'
import Gantt from 'frappe-gantt'
import 'frappe-gantt/dist/frappe-gantt.css'

const store = useStore()
const ganttContainer = ref(null)
let ganttInstance = null

const tasks = computed(() => store.getters.getTasks)

const prepareGanttData = () => {
  return tasks.value.map(task => {
    return {
      id: task.id,
      name: task.title,
      start: task.startDate,
      end: task.endDate,
      progress: task.status === 'completed' ? 100 : task.status === 'in_progress' ? 50 : 0,
      dependencies: ''
    }
  })
}

const initGantt = () => {
  if (ganttContainer.value) {
    ganttInstance = new Gantt(ganttContainer.value, prepareGanttData(), {
      header_height: 50,
      column_width: 30,
      step: 24,
      view_modes: ['Day', 'Week', 'Month'],
      bar_height: 20,
      bar_corner_radius: 3,
      arrow_curve: 5,
      padding: 18,
      view_mode: 'Week',
      date_format: 'YYYY-MM-DD',
      custom_popup_html: function(task) {
        return `
          <div class="gantt-popup">
            <h3>${task.name}</h3>
            <p>开始日期: ${task.start}</p>
            <p>结束日期: ${task.end}</p>
            <p>进度: ${task.progress}%</p>
          </div>
        `
      }
    })
  }
}

const updateGantt = () => {
  if (ganttInstance) {
    ganttInstance.refresh(prepareGanttData())
  }
}

watch(() => tasks.value, () => {
  updateGantt()
}, { deep: true })

onMounted(() => {
  store.dispatch('fetchTasks')
  setTimeout(() => {
    initGantt()
  }, 100)
})
</script>

<style scoped>
.gantt-container {
  width: 100%;
}

.gantt-card {
  margin-bottom: 20px;
}

.gantt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.gantt-header h2 {
  margin: 0;
  color: #409EFF;
}

.gantt-chart {
  height: 500px;
  margin-top: 20px;
}

:deep(.gantt-popup) {
  padding: 10px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

:deep(.gantt-popup h3) {
  margin: 0 0 10px 0;
  color: #409EFF;
}

:deep(.gantt-popup p) {
  margin: 5px 0;
  font-size: 14px;
}
</style>