import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

function TasksPage() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTasks()
    const interval = setInterval(fetchTasks, 3000) // 每3秒刷新
    return () => clearInterval(interval)
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await axios.get('/api/v1/tasks')
      setTasks(response.data.tasks)
    } catch (error) {
      console.error('获取任务列表失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status) => {
    const badges = {
      queued: 'bg-gray-200 text-gray-700',
      processing: 'bg-blue-200 text-blue-700',
      completed: 'bg-green-200 text-green-700',
      failed: 'bg-red-200 text-red-700'
    }
    
    const labels = {
      queued: '排队中',
      processing: '处理中',
      completed: '已完成',
      failed: '失败'
    }
    
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${badges[status]}`}>
        {labels[status]}
      </span>
    )
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h2 className="text-3xl font-bold text-gray-900 mb-8">
        📋 任务列表
      </h2>

      {tasks.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <div className="text-6xl mb-4">📭</div>
          <p className="text-gray-600 text-lg">暂无任务</p>
          <Link
            to="/"
            className="inline-block mt-4 text-blue-600 hover:text-blue-700"
          >
            创建新任务 →
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <Link
              key={task.task_id}
              to={`/tasks/${task.task_id}`}
              className="block bg-white rounded-lg shadow hover:shadow-md transition p-6"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-semibold">
                      {task.source_language} → {task.target_language}
                    </h3>
                    {getStatusBadge(task.status)}
                  </div>
                  
                  <p className="text-gray-600 mb-3">{task.stage}</p>
                  
                  <div className="flex space-x-6 text-sm text-gray-500">
                    <span>🤖 {task.ai_model}</span>
                    <span>📁 {task.total_files} 个文件</span>
                    <span>🕐 {new Date(task.created_at).toLocaleString('zh-CN')}</span>
                  </div>
                  
                  {task.status === 'processing' && (
                    <div className="mt-4">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all"
                          style={{ width: `${task.progress}%` }}
                        ></div>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        {task.progress}% 完成
                      </p>
                    </div>
                  )}
                </div>
                
                <div className="text-gray-400">
                  →
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default TasksPage

