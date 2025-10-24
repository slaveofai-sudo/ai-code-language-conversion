import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'

function TaskDetailPage() {
  const { taskId } = useParams()
  const [task, setTask] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTask()
    
    // 如果任务未完成，定时刷新
    const interval = setInterval(() => {
      if (!task || task.status === 'processing' || task.status === 'queued') {
        fetchTask()
      }
    }, 2000)
    
    return () => clearInterval(interval)
  }, [taskId])

  const fetchTask = async () => {
    try {
      const response = await axios.get(`/api/v1/tasks/${taskId}`)
      setTask(response.data)
    } catch (error) {
      console.error('获取任务详情失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    try {
      const response = await axios.get(`/api/v1/tasks/${taskId}/download`, {
        responseType: 'blob'
      })
      
      // 创建下载链接
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${taskId}.zip`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('下载失败:', error)
      alert('下载失败: ' + (error.response?.data?.detail || error.message))
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!task) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <div className="text-6xl mb-4">❌</div>
          <p className="text-gray-600 text-lg">任务不存在</p>
          <Link to="/tasks" className="inline-block mt-4 text-blue-600 hover:text-blue-700">
            返回任务列表 →
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      {/* 面包屑 */}
      <div className="mb-6">
        <Link to="/tasks" className="text-blue-600 hover:text-blue-700">
          ← 返回任务列表
        </Link>
      </div>

      {/* 任务详情卡片 */}
      <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              任务详情
            </h2>
            <p className="text-gray-600">任务 ID: {task.task_id}</p>
          </div>
          
          {task.status === 'completed' && (
            <button
              onClick={handleDownload}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
            >
              📥 下载结果
            </button>
          )}
        </div>

        {/* 转换信息 */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          <div>
            <p className="text-sm text-gray-600 mb-1">源语言</p>
            <p className="text-lg font-semibold">{task.source_language}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">目标语言</p>
            <p className="text-lg font-semibold">{task.target_language}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">AI 模型</p>
            <p className="text-lg font-semibold">{task.ai_model}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">文件数量</p>
            <p className="text-lg font-semibold">{task.total_files} 个</p>
          </div>
        </div>

        {/* 进度 */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <p className="text-sm font-medium text-gray-700">转换进度</p>
            <p className="text-sm font-medium text-gray-700">{task.progress}%</p>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all ${
                task.status === 'completed' ? 'bg-green-600' :
                task.status === 'failed' ? 'bg-red-600' :
                'bg-blue-600'
              }`}
              style={{ width: `${task.progress}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 mt-2">{task.stage}</p>
        </div>

        {/* 状态 */}
        <div className="flex items-center space-x-2">
          <span className="text-sm font-medium text-gray-700">状态:</span>
          {task.status === 'completed' && (
            <span className="px-3 py-1 bg-green-200 text-green-700 rounded-full text-sm font-medium">
              ✅ 已完成
            </span>
          )}
          {task.status === 'processing' && (
            <span className="px-3 py-1 bg-blue-200 text-blue-700 rounded-full text-sm font-medium">
              ⏳ 处理中
            </span>
          )}
          {task.status === 'failed' && (
            <span className="px-3 py-1 bg-red-200 text-red-700 rounded-full text-sm font-medium">
              ❌ 失败
            </span>
          )}
          {task.status === 'queued' && (
            <span className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm font-medium">
              ⏸️ 排队中
            </span>
          )}
        </div>

        {/* 错误信息 */}
        {task.error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm font-medium text-red-800 mb-1">错误信息:</p>
            <p className="text-sm text-red-700">{task.error}</p>
          </div>
        )}

        {/* 时间信息 */}
        <div className="mt-6 pt-6 border-t border-gray-200 text-sm text-gray-600 space-y-1">
          <p>创建时间: {new Date(task.created_at).toLocaleString('zh-CN')}</p>
          <p>更新时间: {new Date(task.updated_at).toLocaleString('zh-CN')}</p>
          {task.completed_at && (
            <p>完成时间: {new Date(task.completed_at).toLocaleString('zh-CN')}</p>
          )}
        </div>
      </div>

      {/* 结果统计 */}
      {task.status === 'completed' && task.result && (
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">📊 转换统计</h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">总文件数</p>
              <p className="text-2xl font-bold text-blue-600">
                {task.result.total_files}
              </p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">源语言</p>
              <p className="text-2xl font-bold text-green-600">
                {task.result.source_language}
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">目标语言</p>
              <p className="text-2xl font-bold text-purple-600">
                {task.result.target_language}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TaskDetailPage

