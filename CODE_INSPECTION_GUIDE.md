# 📚 代码检测与学习文档生成指南

## 🎯 功能概述

这个功能可以帮助您:
- 🔍 **代码检测**: 全面分析项目代码质量、复杂度和结构
- 📊 **复杂度分析**: 计算圈复杂度、认知复杂度、可维护性指数
- 🎨 **设计模式识别**: 自动识别项目中使用的设计模式
- ⚠️ **代码异味检测**: 发现潜在的代码质量问题
- 🔒 **安全漏洞检测**: 识别常见的安全隐患
- 📚 **学习文档生成**: 自动生成详细的学习文档，包括学习路线图、难度分析等

---

## 🚀 快速开始

### API 调用示例

#### 1. 检测Git仓库并生成学习文档

```bash
curl -X POST http://localhost:8000/api/v1/inspect-project \
  -H "Content-Type: application/json" \
  -d '{
    "git_url": "https://github.com/username/project.git",
    "generate_learning_doc": true,
    "output_format": "markdown"
  }'
```

**响应示例:**
```json
{
  "status": "success",
  "project_path": "/data/uploads/abc123/project",
  "inspection_results": {
    "project_metrics": {
      "project_name": "project",
      "total_files": 45,
      "total_lines": 5234,
      "total_functions": 156,
      "total_classes": 23,
      "avg_complexity": 6.8,
      "overall_difficulty": "intermediate"
    },
    "architecture": {
      "patterns": ["MVC", "Service Layer", "Repository Pattern"],
      "structure": "layered"
    },
    "tech_stack": ["Python/pip", "Node.js/npm"],
    "summary": {
      "health_score": 85.5,
      "total_code_smells": 8,
      "total_security_issues": 0,
      "avg_maintainability": 78.3,
      "recommendation": "✅ 代码质量良好"
    }
  },
  "learning_doc": {
    "content": "# 📚 project - 学习文档\n\n...",
    "file_path": "/data/uploads/abc123/project/project_学习文档.md",
    "format": "markdown"
  }
}
```

#### 2. 检测本地项目

```bash
curl -X POST http://localhost:8000/api/v1/inspect-project \
  -H "Content-Type: application/json" \
  -d '{
    "local_path": "/path/to/local/project",
    "generate_learning_doc": true,
    "output_format": "markdown"
  }'
```

#### 3. 只检测不生成文档

```bash
curl -X POST http://localhost:8000/api/v1/inspect-project \
  -H "Content-Type: application/json" \
  -d '{
    "git_url": "https://github.com/username/project.git",
    "generate_learning_doc": false
  }'
```

#### 4. 生成JSON格式文档

```bash
curl -X POST http://localhost:8000/api/v1/inspect-project \
  -H "Content-Type: application/json" \
  -d '{
    "git_url": "https://github.com/username/project.git",
    "generate_learning_doc": true,
    "output_format": "json"
  }'
```

#### 5. 先检测后转换（组合工作流）

```bash
curl -X POST http://localhost:8000/api/v1/inspect-and-convert \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "git",
    "git_url": "https://github.com/username/java-project.git",
    "source_language": "java",
    "target_language": "python",
    "target_framework": "fastapi",
    "generate_learning_doc": true
  }'
```

---

## 📊 生成的学习文档内容

生成的学习文档包含以下10个主要部分：

### 1. 📖 项目概览
- 基本信息（文件数、代码行数、函数数、类数）
- 整体难度评级
- 健康分数
- 编程语言分布

### 2. 🗺️ 学习路线图
- **推荐学习时间**: 根据难度自动计算
- **前置知识要求**: 明确学习该项目需要的基础知识
- **学习阶段**: 分为4个阶段
  - 阶段1: 项目结构理解 (20%)
  - 阶段2: 核心功能学习 (40%)
  - 阶段3: 设计模式理解 (20%)
  - 阶段4: 实践与优化 (20%)

### 3. 📊 难度分析
- 整体难度等级 (Beginner / Intermediate / Advanced / Expert)
- 难度构成分析（代码量、复杂度、架构、依赖）
- 文件难度分布可视化

### 4. 🛠️ 技术栈分析
- 检测到的技术和框架
- 学习资源推荐（官方文档链接）

### 5. 🏛️ 架构设计
- 架构类型识别
- 检测到的架构模式（MVC、Service Layer等）
- 项目结构树

### 6. 🎨 设计模式
- 识别的设计模式及解释
- 使用场景说明
- 难度评级

### 7. 🧮 代码复杂度
- 整体复杂度指标
- 最复杂的文件Top 5
- 复杂度理解指南

### 8. 📁 文件结构分析
- 文件统计表（行数、函数数、类数、复杂度）
- 按代码量排序展示主要文件

### 9. 💡 学习建议
- 针对不同难度的个性化学习策略
- 学习资源推荐

### 10. 🔍 代码质量报告
- 整体健康分数
- 质量指标（可维护性、代码异味、安全问题）
- 检测到的代码异味列表
- 检测到的安全问题列表
- 改进建议

---

## 📈 检测指标说明

### 复杂度指标

#### 1. 圈复杂度 (Cyclomatic Complexity)
**定义**: 衡量代码中独立路径的数量

**计算公式**: CC = E - N + 2P
- E = 边的数量
- N = 节点数量
- P = 连接组件数量

**简化计算**: 决策点数量 + 1

**评级标准**:
- **1-5**: 🟢 简单易懂
- **6-10**: 🟡 中等复杂
- **11-20**: 🟠 较复杂
- **20+**: 🔴 非常复杂

**示例**:
```python
# CC = 1 (简单)
def simple():
    return "hello"

# CC = 2 (1个if)
def with_if(x):
    if x > 0:
        return "positive"
    return "non-positive"

# CC = 5 (4个if)
def complex(a, b, c, d):
    if a:
        return 1
    if b:
        return 2
    if c:
        return 3
    if d:
        return 4
    return 5
```

#### 2. 认知复杂度 (Cognitive Complexity)
**定义**: 衡量代码理解的难度，考虑嵌套和控制流

**特点**:
- 关注代码的可读性
- 嵌套结构增加复杂度
- 布尔运算符增加复杂度

**示例**:
```python
# 认知复杂度 = 1
def simple_if(x):
    if x > 0:  # +1
        return True

# 认知复杂度 = 3
def nested_if(x, y):
    if x > 0:        # +1
        if y > 0:    # +2 (嵌套)
            return True
```

#### 3. 可维护性指数 (Maintainability Index)
**定义**: 0-100的分数，表示代码的可维护性

**公式**: MI = max(0, (171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(L)) * 100 / 171)
- V = Halstead Volume (代码体积)
- G = 圈复杂度
- L = 代码行数

**评级标准**:
- **80-100**: 🟢 优秀
- **60-79**: 🟡 良好
- **40-59**: 🟠 需改进
- **0-39**: 🔴 难以维护

### 代码异味类型

#### 1. Long Method (过长方法)
**定义**: 方法代码行数超过50行

**问题**: 难以理解、测试和维护

**解决方案**: 拆分为多个小方法

#### 2. Too Many Parameters (参数过多)
**定义**: 方法参数超过5个

**问题**: 调用复杂，容易出错

**解决方案**: 使用参数对象封装

#### 3. High Complexity (高复杂度)
**定义**: 圈复杂度超过10

**问题**: 逻辑复杂，难以测试

**解决方案**: 简化逻辑，提取方法

#### 4. Large Class (过大类)
**定义**: 类的方法数超过20个

**问题**: 违反单一职责原则

**解决方案**: 拆分为多个类

### 安全问题检测

#### 1. Dangerous Functions (危险函数)
- `eval()`: 代码注入风险
- `exec()`: 代码注入风险
- SQL拼接: SQL注入风险

#### 2. Hardcoded Secrets (硬编码密钥)
- 硬编码密码
- 硬编码API密钥
- 硬编码token

**建议**: 使用环境变量或配置文件

---

## 💡 使用场景

### 场景1: 学习新项目
**目标**: 快速理解陌生项目的结构和复杂度

**步骤**:
1. 使用 `/api/v1/inspect-project` 检测项目
2. 查看生成的学习文档
3. 按照学习路线图逐步学习
4. 关注标记为"困难"的文件

### 场景2: 代码审查
**目标**: 评估代码质量，发现潜在问题

**步骤**:
1. 检测项目并生成报告
2. 查看代码质量报告
3. 检查代码异味和安全问题
4. 根据建议进行优化

### 场景3: 重构前评估
**目标**: 了解哪些部分需要重构

**步骤**:
1. 检测项目获取复杂度数据
2. 找出最复杂的文件和方法
3. 优先重构高复杂度代码
4. 重构后再次检测验证改进

### 场景4: 技术债务评估
**目标**: 量化技术债务，制定改进计划

**步骤**:
1. 定期检测项目
2. 跟踪健康分数变化
3. 监控代码异味数量
4. 制定技术债务偿还计划

### 场景5: 团队培训
**目标**: 帮助新成员快速上手

**步骤**:
1. 为每个项目生成学习文档
2. 新成员按照学习路线图学习
3. 关注设计模式和架构讲解
4. 结合代码一起学习

---

## 📝 生成文档示例

### 示例项目: FastAPI应用

**检测结果概览:**
```
项目名称: fastapi-app
代码文件数: 25
代码总行数: 3,456
函数数量: 89
类数量: 15
整体难度: INTERMEDIATE
健康分数: 88.5/100 🟢
```

**语言分布:**
```
Python: 3,200 行 (92.6%)
YAML: 180 行 (5.2%)
Shell: 76 行 (2.2%)
```

**学习路线图:**
```
推荐学习时间: 3-5 天

前置知识要求:
- 熟悉基本语法和数据结构

学习阶段:
  阶段1: 项目结构理解 (20%) - 1-2小时
  阶段2: 核心功能学习 (40%) - 根据难度而定
    重点学习文件:
    1. main.py - 12 个函数, 0 个类
    2. routers/users.py - 8 个函数, 0 个类
    3. services/auth.py - 6 个函数, 1 个类
  
  阶段3: 设计模式理解 (20%) - 2-4小时
  阶段4: 实践与优化 (20%) - 根据项目复杂度而定
```

**难度分析:**
```
难度构成分析:
| 维度 | 评分 | 说明 |
|------|------|------|
| 代码量 | 3.5/10 | 3,456 行代码 |
| 复杂度 | 6.8/10 | 平均圈复杂度 6.8 |
| 架构设计 | 5.8/10 | 15 个类 |
| 依赖管理 | 5.0/10 | 中等复杂度 |

文件难度分布:
简单 (Easy):    ████████████ 12 个文件
中等 (Medium):  ████████ 8 个文件
困难 (Hard):    ███ 3 个文件
专家 (Expert):  █ 2 个文件
```

**质量报告:**
```
整体健康分数: 88.5/100
✅ 良好！代码质量不错

质量指标:
| 指标 | 值 | 状态 |
|------|----|----|
| 平均可维护性 | 82.3/100 | 🟢 优秀 |
| 代码异味数量 | 5 | 🟡 少量 |
| 安全问题数量 | 0 | 🟢 无 |

检测到的代码异味:
- long_method in user_service.py: 方法过长 (68 行)，建议拆分
- high_complexity in auth.py: 圈复杂度过高 (12)，难以理解和测试
```

---

## 🎓 最佳实践

### 1. 定期检测
建议每周或每次重大更新后检测项目，跟踪代码质量变化。

### 2. 设置质量门禁
在CI/CD流程中集成代码检测，设置最低健康分数要求。

### 3. 优先重构
按照复杂度和代码异味的严重程度，优先重构问题最严重的代码。

### 4. 团队共享
将生成的学习文档添加到项目文档中，方便团队成员查阅。

### 5. 持续改进
根据检测报告制定改进计划，逐步提升代码质量。

---

## 🔗 相关API

- `POST /api/v1/inspect-project` - 检测项目并生成学习文档
- `GET /api/v1/inspect-project/{task_id}/download` - 下载学习文档
- `POST /api/v1/inspect-and-convert` - 检测项目后进行代码转换

---

## 💬 常见问题

### Q1: 支持哪些编程语言？
A: 目前完整支持Python（使用AST），对Java、JavaScript、Go、Rust等提供基础支持。

### Q2: 检测需要多长时间？
A: 取决于项目大小，通常1000行代码需要10-30秒。

### Q3: 学习文档可以自定义吗？
A: 目前提供Markdown和JSON两种格式，未来会支持更多自定义选项。

### Q4: 如何提高检测准确性？
A: 确保项目代码符合标准规范，使用明确的命名和注释。

### Q5: 可以只检测特定文件吗？
A: 当前版本检测整个项目，未来会支持单文件检测。

---

**🎉 开始使用代码检测功能，让学习和维护代码变得更简单！**

