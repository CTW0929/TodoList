<template>
  <div class="tasks-container">
    <el-card class="tasks-card">
      <template #header>
        <div class="tasks-header">
          <h2>任务管理</h2>
          <el-button type="primary" @click="showAddTaskDialog = true">添加任务</el-button>
        </div>
      </template>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="全部" name="all">
          <el-table :data="tasks" style="width: 100%">
            <el-table-column prop="title" label="任务标题" width="200"></el-table-column>
            <el-table-column prop="description" label="任务描述"></el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="scope">
                <el-tag :type="getPriorityType(scope.row.priority)">{{ getPriorityText(scope.row.priority) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="startDate" label="开始日期" width="120"></el-table-column>
            <el-table-column prop="endDate" label="结束日期" width="120"></el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click="editTask(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteTask(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="待办" name="pending">
          <el-table :data="filteredTasks('pending')" style="width: 100%">
            <el-table-column prop="title" label="任务标题" width="200"></el-table-column>
            <el-table-column prop="description" label="任务描述"></el-table-column>
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="scope">
                <el-tag :type="getPriorityType(scope.row.priority)">{{ getPriorityText(scope.row.priority) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="startDate" label="开始日期" width="120"></el-table-column>
            <el-table-column prop="endDate" label="结束日期" width="120"></el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click="editTask(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteTask(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="进行中" name="in_progress">
          <el-table :data="filteredTasks('in_progress')" style="width: 100%">
            <el-table-column prop="title" label="任务标题" width="200"></el-table-column>
            <el-table-column prop="description" label="任务描述"></el-table-column>
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="scope">
                <el-tag :type="getPriorityType(scope.row.priority)">{{ getPriorityText(scope.row.priority) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="startDate" label="开始日期" width="120"></el-table-column>
            <el-table-column prop="endDate" label="结束日期" width="120"></el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click="editTask(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteTask(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="已完成" name="completed">
          <el-table :data="filteredTasks('completed')" style="width: 100%">
            <el-table-column prop="title" label="任务标题" width="200"></el-table-column>
            <el-table-column prop="description" label="任务描述"></el-table-column>
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="scope">
                <el-tag :type="getPriorityType(scope.row.priority)">{{ getPriorityText(scope.row.priority) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="startDate" label="开始日期" width="120"></el-table-column>
            <el-table-column prop="endDate" label="结束日期" width="120"></el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click="editTask(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteTask(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 添加/编辑任务对话框 -->
    <el-dialog v-model="showAddTaskDialog" :title="isEditing ? '编辑任务' : '添加任务'">
      <el-form :model="taskForm" :rules="rules" ref="taskFormRef" label-width="80px">
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="taskForm.title" placeholder="请输入任务标题"></el-input>
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="taskForm.description" type="textarea" placeholder="请输入任务描述"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="taskForm.status" placeholder="请选择状态">
            <el-option label="待办" value="pending"></el-option>
            <el-option label="进行中" value="in_progress"></el-option>
            <el-option label="已完成" value="completed"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="taskForm.priority" placeholder="请选择优先级">
            <el-option label="高" value="high"></el-option>
            <el-option label="中" value="medium"></el-option>
            <el-option label="低" value="low"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" prop="startDate">
          <el-date-picker v-model="taskForm.startDate" type="date" placeholder="选择开始日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="结束日期" prop="endDate">
          <el-date-picker v-model="taskForm.endDate" type="date" placeholder="选择结束日期"></el-date-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddTaskDialog = false">取消</el-button>
          <el-button type="primary" @click="saveTask">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElLoading } from 'element-plus'

const store = useStore()
const activeTab = ref('all')
const showAddTaskDialog = ref(false)
const isEditing = ref(false)
const currentTaskId = ref(null)
const taskFormRef = ref(null)
const loading = ref(false)

const tasks = computed(() => store.getters.getTasks)

const taskForm = ref({
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
  startDate: '',
  endDate: ''
})

const rules = {
  title: [
    { required: true, message: '请输入任务标题', trigger: 'blur' }
  ],
  startDate: [
    { required: true, message: '请选择开始日期', trigger: 'blur' }
  ],
  endDate: [
    { required: true, message: '请选择结束日期', trigger: 'blur' }
  ]
}

const filteredTasks = (status) => {
  return tasks.value.filter(task => task.status === status)
}

const getStatusType = (status) => {
  switch (status) {
    case 'completed': return 'success'
    case 'in_progress': return 'warning'
    case 'pending': return 'info'
    default: return ''
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'completed': return '已完成'
    case 'in_progress': return '进行中'
    case 'pending': return '待办'
    default: return ''
  }
}

const getPriorityType = (priority) => {
  switch (priority) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'success'
    default: return ''
  }
}

const getPriorityText = (priority) => {
  switch (priority) {
    case 'high': return '高'
    case 'medium': return '中'
    case 'low': return '低'
    default: return ''
  }
}

const editTask = (task) => {
  isEditing.value = true
  currentTaskId.value = task.id
  taskForm.value = { ...task }
  showAddTaskDialog.value = true
}

const deleteTask = async (id) => {
  try {
    loading.value = true
    await store.dispatch('deleteTask', id)
    ElMessage.success('任务删除成功')
  } catch (error) {
    ElMessage.error('删除任务失败：' + (error.response?.data?.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const saveTask = async () => {
  if (taskFormRef.value) {
    await taskFormRef.value.validate(async (valid) => {
      if (valid) {
        try {
          loading.value = true
          if (isEditing.value) {
            await store.dispatch('updateTask', { id: currentTaskId.value, task: taskForm.value })
            ElMessage.success('任务更新成功')
          } else {
            await store.dispatch('addTask', taskForm.value)
            ElMessage.success('任务添加成功')
          }
          showAddTaskDialog.value = false
          resetForm()
        } catch (error) {
          ElMessage.error('操作失败：' + (error.response?.data?.message || '未知错误'))
        } finally {
          loading.value = false
        }
      }
    })
  }
}

const resetForm = () => {
  taskForm.value = {
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    startDate: '',
    endDate: ''
  }
  isEditing.value = false
  currentTaskId.value = null
}

const fetchTasks = async () => {
  try {
    loading.value = true
    await store.dispatch('fetchTasks')
  } catch (error) {
    ElMessage.error('获取任务失败：' + (error.response?.data?.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.tasks-container {
  width: 100%;
}

.tasks-card {
  margin-bottom: 20px;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tasks-header h2 {
  margin: 0;
  color: #409EFF;
}

.el-tabs {
  margin-top: 20px;
}

.el-table {
  margin-top: 20px;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>