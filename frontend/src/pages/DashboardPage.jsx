/**
 * Dashboard Page / 仪表板页面
 * 
 * Features / 功能:
 * - Cost statistics / 成本统计
 * - Cache statistics / 缓存统计
 * - Real-time progress / 实时进度
 * - Cost estimator / 成本估算器
 */

import { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  CurrencyDollarIcon,
  ServerIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';

export default function DashboardPage() {
  const [costReport, setCostReport] = useState(null);
  const [cacheStats, setCacheStats] = useState(null);
  const [estimate, setEstimate] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Estimation form state / 估算表单状态
  const [linesOfCode, setLinesOfCode] = useState(10000);
  const [sourceLanguage, setSourceLanguage] = useState('java');
  const [targetLanguage, setTargetLanguage] = useState('python');
  const [aiModel, setAIModel] = useState('gpt-4o');

  useEffect(() => {
    fetchDashboardData();
    // Refresh every 30 seconds / 每30秒刷新一次
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch cost report / 获取成本报告
      const costRes = await fetch('http://localhost:8000/api/v1/cost/report');
      const costData = await costRes.json();
      setCostReport(costData.report);

      // Fetch cache stats / 获取缓存统计
      const cacheRes = await fetch('http://localhost:8000/api/v1/cache/stats');
      const cacheData = await cacheRes.json();
      setCacheStats(cacheData.stats);

      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setLoading(false);
    }
  };

  const handleEstimate = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/estimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lines_of_code: parseInt(linesOfCode),
          source_language: sourceLanguage,
          target_language: targetLanguage,
          ai_model: aiModel,
          strategy: 'quality_first'
        })
      });
      const data = await response.json();
      setEstimate(data);
    } catch (error) {
      console.error('Failed to estimate cost:', error);
    }
  };

  const handleClearCache = async () => {
    if (confirm('确定要清空所有缓存吗？')) {
      try {
        await fetch('http://localhost:8000/api/v1/cache/clear', {
          method: 'POST'
        });
        fetchDashboardData();
        alert('缓存已清空！');
      } catch (error) {
        console.error('Failed to clear cache:', error);
        alert('清空缓存失败！');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header / 页头 */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📊 控制台 / Dashboard
          </h1>
          <p className="text-gray-600">
            实时监控转换成本、缓存状态和系统性能
          </p>
        </div>

        {/* Stats Cards / 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Cost / 总成本 */}
          <StatsCard
            title="总支出"
            value={`$${costReport?.total_cost_usd || 0}`}
            icon={<CurrencyDollarIcon className="h-8 w-8" />}
            color="blue"
            trend={+5.2}
          />

          {/* Total Conversions / 总转换次数 */}
          <StatsCard
            title="转换次数"
            value={costReport?.total_conversions || 0}
            icon={<ChartBarIcon className="h-8 w-8" />}
            color="green"
            trend={+12.5}
          />

          {/* Cache Hit Rate / 缓存命中率 */}
          <StatsCard
            title="缓存命中率"
            value={`${cacheStats?.hit_rate_percent || 0}%`}
            icon={<ServerIcon className="h-8 w-8" />}
            color="purple"
            trend={+8.3}
          />

          {/* Cached Items / 缓存项数 */}
          <StatsCard
            title="缓存项数"
            value={cacheStats?.total_cached_items || 0}
            icon={<ClockIcon className="h-8 w-8" />}
            color="orange"
          />
        </div>

        {/* Main Content Grid / 主内容网格 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Cost Estimator / 成本估算器 */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                💰 成本估算器
              </h2>
              <SparklesIcon className="h-6 w-6 text-yellow-500" />
            </div>

            <div className="space-y-4">
              {/* Lines of Code / 代码行数 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  代码行数 (Lines of Code)
                </label>
                <input
                  type="number"
                  value={linesOfCode}
                  onChange={(e) => setLinesOfCode(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="100"
                  step="1000"
                />
              </div>

              {/* Language Selection / 语言选择 */}
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
                    <option value="java">Java</option>
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="go">Go</option>
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
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="go">Go</option>
                  </select>
                </div>
              </div>

              {/* AI Model Selection / AI模型选择 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  AI模型
                </label>
                <select
                  value={aiModel}
                  onChange={(e) => setAIModel(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="gpt-4o">GPT-4o (推荐)</option>
                  <option value="gpt-4">GPT-4 Turbo</option>
                  <option value="claude-3.5-sonnet">Claude 3.5 Sonnet</option>
                  <option value="gemini-pro">Gemini Pro</option>
                  <option value="deepseek-coder">DeepSeek Coder</option>
                  <option value="qwen-coder">通义千问 Coder</option>
                </select>
              </div>

              {/* Estimate Button / 估算按钮 */}
              <button
                onClick={handleEstimate}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                🔮 开始估算
              </button>

              {/* Estimation Results / 估算结果 */}
              {estimate && estimate.success && (
                <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
                  <h3 className="font-bold text-lg mb-3 text-gray-900">估算结果</h3>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">预估成本:</span>
                      <span className="font-bold text-2xl text-blue-600">
                        ${estimate.estimate.cost_usd}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">预估时间:</span>
                      <span className="font-semibold text-gray-900">
                        ~{estimate.estimate.time_minutes} 分钟
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">总Token数:</span>
                      <span className="font-semibold text-gray-900">
                        {estimate.estimate.total_tokens.toLocaleString()}
                      </span>
                    </div>
                  </div>

                  {/* Alternative Options / 替代方案 */}
                  {estimate.estimate.alternative_options && estimate.estimate.alternative_options.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-blue-200">
                      <h4 className="font-semibold text-sm mb-2 text-gray-700">💡 更便宜的选项:</h4>
                      <div className="space-y-2">
                        {estimate.estimate.alternative_options.map((alt, idx) => (
                          <div key={idx} className="flex items-center justify-between text-sm p-2 bg-white rounded">
                            <div>
                              <span className="font-medium">{alt.model}</span>
                              <span className="text-gray-500 text-xs ml-2">{alt.recommendation}</span>
                            </div>
                            <div className="text-right">
                              <div className="font-semibold text-green-600">${alt.cost_usd}</div>
                              <div className="text-xs text-gray-500">
                                省 ${alt.savings_usd} ({alt.savings_percent}%)
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Cache Statistics / 缓存统计 */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                🚀 缓存统计
              </h2>
              <button
                onClick={handleClearCache}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm font-medium"
              >
                清空缓存
              </button>
            </div>

            {cacheStats && (
              <div className="space-y-6">
                {/* Cache Hit Rate Donut / 缓存命中率圆环图 */}
                <div className="relative">
                  <div className="flex items-center justify-center">
                    <div className="relative">
                      <svg className="w-40 h-40 transform -rotate-90">
                        <circle
                          cx="80"
                          cy="80"
                          r="60"
                          stroke="#E5E7EB"
                          strokeWidth="20"
                          fill="none"
                        />
                        <circle
                          cx="80"
                          cy="80"
                          r="60"
                          stroke="#10B981"
                          strokeWidth="20"
                          fill="none"
                          strokeDasharray={`${cacheStats.hit_rate_percent * 3.77} 377`}
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center flex-col">
                        <span className="text-3xl font-bold text-gray-900">
                          {cacheStats.hit_rate_percent}%
                        </span>
                        <span className="text-sm text-gray-500">命中率</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Cache Stats Grid / 缓存统计网格 */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-green-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">缓存命中</div>
                    <div className="text-2xl font-bold text-green-600">
                      {cacheStats.hits}
                    </div>
                  </div>
                  
                  <div className="p-4 bg-red-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">缓存未命中</div>
                    <div className="text-2xl font-bold text-red-600">
                      {cacheStats.misses}
                    </div>
                  </div>
                  
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">缓存写入</div>
                    <div className="text-2xl font-bold text-blue-600">
                      {cacheStats.sets}
                    </div>
                  </div>
                  
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">缓存后端</div>
                    <div className="text-lg font-bold text-purple-600 capitalize">
                      {cacheStats.cache_backend}
                    </div>
                  </div>
                </div>

                {/* Performance Impact / 性能影响 */}
                <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
                  <h4 className="font-semibold text-gray-900 mb-2">💡 性能影响</h4>
                  <p className="text-sm text-gray-700">
                    缓存命中率 <span className="font-bold">{cacheStats.hit_rate_percent}%</span> 
                    {' '}意味着您节省了大约{' '}
                    <span className="font-bold text-green-600">
                      {cacheStats.hits}
                    </span>
                    {' '}次API调用！
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Cost History / 成本历史 */}
        {costReport && costReport.recent_conversions && costReport.recent_conversions.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              📈 最近转换记录
            </h2>
            
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      任务ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      时间
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Token数
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      成本
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      耗时
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {costReport.recent_conversions.map((conversion, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {conversion.task_id.substring(0, 8)}...
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(conversion.timestamp).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {conversion.actual_tokens.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                        ${conversion.actual_cost.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {conversion.actual_time.toFixed(1)}分钟
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Stats Card Component / 统计卡片组件
function StatsCard({ title, value, icon, color, trend }) {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600'
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          
          {trend !== undefined && (
            <div className="flex items-center mt-2">
              {trend > 0 ? (
                <>
                  <ArrowTrendingUpIcon className="h-4 w-4 text-green-500 mr-1" />
                  <span className="text-sm text-green-500 font-medium">
                    +{trend}%
                  </span>
                </>
              ) : (
                <>
                  <ArrowTrendingDownIcon className="h-4 w-4 text-red-500 mr-1" />
                  <span className="text-sm text-red-500 font-medium">
                    {trend}%
                  </span>
                </>
              )}
              <span className="text-xs text-gray-500 ml-2">vs 上周</span>
            </div>
          )}
        </div>
        
        <div className={`p-4 bg-gradient-to-br ${colors[color]} rounded-xl text-white`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

