import React from 'react'
import { Link } from 'react-router-dom'

function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-3">
            <div className="text-3xl">🚀</div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI Code Migration Platform
              </h1>
              <p className="text-sm text-gray-600">多语言代码智能转换系统</p>
            </div>
          </Link>
          
          <nav className="flex space-x-6">
            <Link
              to="/"
              className="text-gray-700 hover:text-blue-600 font-medium transition"
            >
              首页
            </Link>
            <Link
              to="/tasks"
              className="text-gray-700 hover:text-blue-600 font-medium transition"
            >
              任务列表
            </Link>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-700 hover:text-blue-600 font-medium transition"
            >
              API 文档
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header

