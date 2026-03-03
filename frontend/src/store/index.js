import { createStore } from 'vuex'
import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 10000,
  withCredentials: true
})

const store = createStore({
  state: {
    isAuthenticated: false,
    user: null,
    tasks: [],
    filter: 'all'
  },
  mutations: {
    login(state, user) {
      state.isAuthenticated = true
      state.user = user
    },
    logout(state) {
      state.isAuthenticated = false
      state.user = null
    },
    setTasks(state, tasks) {
      state.tasks = tasks
    },
    addTask(state, task) {
      state.tasks.push(task)
    },
    updateTask(state, { id, task }) {
      const index = state.tasks.findIndex(t => t.id === id)
      if (index !== -1) {
        state.tasks[index] = { ...state.tasks[index], ...task }
      }
    },
    deleteTask(state, id) {
      state.tasks = state.tasks.filter(t => t.id !== id)
    },
    setFilter(state, filter) {
      state.filter = filter
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/auth/login', credentials)
        commit('login', response.data.user)
        return response.data
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },
    async logout({ commit }) {
      try {
        await api.post('/auth/logout')
        commit('logout')
      } catch (error) {
        console.error('Logout error:', error)
        throw error
      }
    },
    async fetchTasks({ commit }) {
      try {
        const response = await api.get('/todos')
        // 转换API响应格式以匹配前端预期
        const formattedTasks = response.data.map(task => ({
          id: task.id,
          title: task.title,
          description: task.description,
          status: task.status,
          priority: task.priority,
          startDate: task.start_time,
          endDate: task.end_time,
          createdAt: task.created_at
        }))
        commit('setTasks', formattedTasks)
      } catch (error) {
        console.error('Fetch tasks error:', error)
        throw error
      }
    },
    async addTask({ commit }, task) {
      try {
        const response = await api.post('/todos', {
          title: task.title,
          description: task.description,
          status: task.status,
          priority: task.priority,
          start_time: task.startDate,
          end_time: task.endDate
        })
        const newTask = {
          id: response.data.id,
          title: response.data.title,
          description: response.data.description,
          status: response.data.status,
          priority: response.data.priority,
          startDate: response.data.start_time,
          endDate: response.data.end_time,
          createdAt: response.data.created_at
        }
        commit('addTask', newTask)
        return newTask
      } catch (error) {
        console.error('Add task error:', error)
        throw error
      }
    },
    async updateTask({ commit }, { id, task }) {
      try {
        const response = await api.put(`/todos/${id}`, {
          title: task.title,
          description: task.description,
          status: task.status,
          priority: task.priority,
          start_time: task.startDate,
          end_time: task.endDate,
          completed: task.status === 'completed'
        })
        const updatedTask = {
          id: response.data.id,
          title: response.data.title,
          description: response.data.description,
          status: response.data.status,
          priority: response.data.priority,
          startDate: response.data.start_time,
          endDate: response.data.end_time,
          createdAt: response.data.created_at
        }
        commit('updateTask', { id, task: updatedTask })
        return updatedTask
      } catch (error) {
        console.error('Update task error:', error)
        throw error
      }
    },
    async deleteTask({ commit }, id) {
      try {
        await api.delete(`/todos/${id}`)
        commit('deleteTask', id)
      } catch (error) {
        console.error('Delete task error:', error)
        throw error
      }
    }
  },
  getters: {
    getTasks: state => {
      if (state.filter === 'all') {
        return state.tasks
      }
      return state.tasks.filter(task => task.status === state.filter)
    },
    getTaskById: state => id => {
      return state.tasks.find(task => task.id === id)
    },
    taskStats: state => {
      const total = state.tasks.length
      const completed = state.tasks.filter(t => t.status === 'completed').length
      const inProgress = state.tasks.filter(t => t.status === 'in_progress').length
      const pending = state.tasks.filter(t => t.status === 'pending').length
      
      return {
        total,
        completed,
        inProgress,
        pending,
        completionRate: total > 0 ? Math.round((completed / total) * 100) : 0
      }
    }
  }
})

export default store