import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function HomePage() {
  const navigate = useNavigate()
  
  const [sourceType, setSourceType] = useState('git') // 'git' or 'upload'
  const [gitUrl, setGitUrl] = useState('')
  const [gitBranch, setGitBranch] = useState('main')
  const [file, setFile] = useState(null)
  const [sourceLanguage, setSourceLanguage] = useState('java')
  const [targetLanguage, setTargetLanguage] = useState('python')
  const [aiModel, setAiModel] = useState('gpt-4')
  const [loading, setLoading] = useState(false)
  const [languages, setLanguages] = useState([])
  const [models, setModels] = useState([])

  useEffect(() => {
    // 加载支持的语言和模型
    fetchLanguages()
    fetchModels()
  }, [])

  const fetchLanguages = async () => {
    try {
      const response = await axios.get('/api/v1/languages')
      setLanguages(response.data.languages)
    } catch (error) {
      console.error('获取语言列表失败:', error)
    }
  }

  const fetchModels = async () => {
    try {
      const response = await axios.get('/api/v1/models')
      setModels(response.data.models)
    } catch (error) {
      console.error('获取模型列表失败:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      let response
      
      if (sourceType === 'git') {
        // Git 仓库转换
        response = await axios.post('/api/v1/convert', {
          source_type: 'git',
          git_url: gitUrl,
          git_branch: gitBranch,
          source_language: sourceLanguage,
          target_language: targetLanguage,
          ai_model: aiModel
        })
      } else {
        // 文件上传转换
        const formData = new FormData()
        formData.append('file', file)
        formData.append('source_language', sourceLanguage)
        formData.append('target_language', targetLanguage)
        formData.append('ai_model', aiModel)
        
        response = await axios.post('/api/v1/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }

      const taskId = response.data.task_id
      navigate(`/tasks/${taskId}`)
      
    } catch (error) {
      console.error('提交失败:', error)
      alert('提交失败: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          🔄 跨语言代码自动迁移
        </h2>
        <p className="text-xl text-gray-600">
          支持 Java、Python、JavaScript、Go 等多种语言互转
        </p>
        <p className="text-lg text-gray-500 mt-2">
          由 GPT-4、Claude 等先进 AI 模型驱动
        </p>
      </div>

      {/* 转换表单 */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 输入方式选择 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              输入方式
            </label>
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => setSourceType('git')}
                className={`flex-1 py-3 px-4 rounded-lg border-2 transition ${
                  sourceType === 'git'
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                🌐 Git 仓库
              </button>
              <button
                type="button"
                onClick={() => setSourceType('upload')}
                className={`flex-1 py-3 px-4 rounded-lg border-2 transition ${
                  sourceType === 'upload'
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                📁 上传 ZIP
              </button>
            </div>
          </div>

          {/* Git URL 输入 */}
          {sourceType === 'git' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Git 仓库 URL
                </label>
                <input
                  type="url"
                  value={gitUrl}
                  onChange={(e) => setGitUrl(e.target.value)}
                  placeholder="https://github.com/user/repository.git"
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  分支 (可选)
                </label>
                <input
                  type="text"
                  value={gitBranch}
                  onChange={(e) => setGitBranch(e.target.value)}
                  placeholder="main"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          )}

          {/* 文件上传 */}
          {sourceType === 'upload' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                上传项目 ZIP 文件
              </label>
              <input
                type="file"
                accept=".zip"
                onChange={(e) => setFile(e.target.files[0])}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          )}

          {/* 语言选择 */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                源语言
              </label>
              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {languages.map((lang) => (
                  <option key={lang.id} value={lang.id}>
                    {lang.icon} {lang.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                目标语言
              </label>
              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {languages.map((lang) => (
                  <option key={lang.id} value={lang.id}>
                    {lang.icon} {lang.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* AI 模型选择 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              AI 模型
            </label>
            <select
              value={aiModel}
              onChange={(e) => setAiModel(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {models.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.name} ({model.provider}) {model.recommended && '⭐'}
                </option>
              ))}
            </select>
          </div>

          {/* 提交按钮 */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? '处理中...' : '🚀 开始转换'}
          </button>
        </form>
      </div>

      {/* 功能特性 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-3xl mb-3">⚡</div>
          <h3 className="font-bold text-lg mb-2">快速转换</h3>
          <p className="text-gray-600 text-sm">
            基于先进 AI 模型，快速准确地转换代码
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-3xl mb-3">🎯</div>
          <h3 className="font-bold text-lg mb-2">保持语义</h3>
          <p className="text-gray-600 text-sm">
            保留原始逻辑、注释和代码结构
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-3xl mb-3">📦</div>
          <h3 className="font-bold text-lg mb-2">完整项目</h3>
          <p className="text-gray-600 text-sm">
            自动生成项目结构和依赖文件
          </p>
        </div>
      </div>
    </div>
  )
}

export default HomePage

