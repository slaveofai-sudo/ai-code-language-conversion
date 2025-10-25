"""
Framework Mapper / 框架映射器

Maps source frameworks to equivalent target frameworks.
将源框架映射到等效的目标框架。

Example mappings / 映射示例:
- Spring Boot (Java) → FastAPI/Django/Flask (Python)
- Express (JavaScript) → FastAPI/Flask (Python) or Gin (Go)
- Django (Python) → Spring Boot (Java) or NestJS (TypeScript)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from loguru import logger


@dataclass
class FrameworkMapping:
    """
    Framework mapping definition / 框架映射定义
    
    Attributes:
        source_framework: Source framework name / 源框架名称
        source_language: Source programming language / 源编程语言
        target_framework: Target framework name / 目标框架名称
        target_language: Target programming language / 目标编程语言
        compatibility_score: Compatibility score (0.0-1.0) / 兼容性分数
        required_adaptations: List of required code adaptations / 所需的代码适配列表
    """
    source_framework: str
    source_language: str
    target_framework: str
    target_language: str
    compatibility_score: float
    required_adaptations: List[str]
    migration_notes: str = ""


class FrameworkMapper:
    """
    Framework Mapper / 框架映射器
    
    Provides intelligent framework mapping suggestions based on:
    基于以下因素提供智能框架映射建议:
    - Feature compatibility / 特性兼容性
    - Architectural patterns / 架构模式
    - Community support / 社区支持
    - Performance characteristics / 性能特征
    """
    
    # Framework mapping database / 框架映射数据库
    FRAMEWORK_MAPPINGS = {
        # Java to Python / Java到Python
        ("spring-boot", "java", "python"): [
            {
                "target": "fastapi",
                "score": 0.95,
                "adaptations": [
                    "REST API annotations → FastAPI decorators",
                    "Dependency Injection → FastAPI Depends()",
                    "JPA/Hibernate → SQLAlchemy ORM",
                    "application.properties → .env / config.yaml"
                ],
                "notes": "最佳选择：FastAPI架构与Spring Boot最相似，支持依赖注入和异步"
            },
            {
                "target": "django",
                "score": 0.85,
                "adaptations": [
                    "REST Controllers → Django views/viewsets",
                    "JPA Entities → Django Models",
                    "Spring Security → Django authentication",
                    "application.properties → settings.py"
                ],
                "notes": "Django提供完整的Web框架，适合大型应用"
            },
            {
                "target": "flask",
                "score": 0.75,
                "adaptations": [
                    "@RestController → @app.route",
                    "Manual dependency injection setup",
                    "JPA → SQLAlchemy (manual setup)",
                    "More manual configuration required"
                ],
                "notes": "Flask更轻量，但需要更多手动配置"
            }
        ],
        
        # Python Django to Java / Python Django到Java
        ("django", "python", "java"): [
            {
                "target": "spring-boot",
                "score": 0.90,
                "adaptations": [
                    "Django Models → JPA Entities",
                    "Django views → REST Controllers",
                    "settings.py → application.properties",
                    "Django ORM → Hibernate/JPA"
                ],
                "notes": "Spring Boot是Java中最接近Django的全功能框架"
            },
            {
                "target": "quarkus",
                "score": 0.80,
                "adaptations": [
                    "Similar to Spring Boot migration",
                    "Better native compilation support",
                    "Reactive programming model"
                ],
                "notes": "Quarkus性能更好，适合云原生应用"
            }
        ],
        
        # Python FastAPI to Other / Python FastAPI到其他语言
        ("fastapi", "python", "java"): [
            {
                "target": "spring-boot",
                "score": 0.88,
                "adaptations": [
                    "FastAPI routes → @RestController",
                    "Pydantic models → Java POJOs with validation",
                    "Async functions → CompletableFuture/Reactor",
                    "Depends() → @Autowired"
                ],
                "notes": "Spring Boot提供类似的依赖注入和REST支持"
            }
        ],
        
        ("fastapi", "python", "go"): [
            {
                "target": "gin",
                "score": 0.85,
                "adaptations": [
                    "FastAPI routes → Gin routes",
                    "Pydantic models → Go structs with tags",
                    "Async → Goroutines",
                    "Manual dependency injection"
                ],
                "notes": "Gin提供类似的路由和中间件系统"
            },
            {
                "target": "fiber",
                "score": 0.83,
                "adaptations": [
                    "FastAPI-like API design",
                    "Express-inspired but in Go",
                    "Very fast performance"
                ],
                "notes": "Fiber API设计更接近Express和FastAPI"
            }
        ],
        
        # JavaScript Express to Python / JavaScript Express到Python
        ("express", "javascript", "python"): [
            {
                "target": "flask",
                "score": 0.90,
                "adaptations": [
                    "app.get() → @app.route()",
                    "Middleware → Flask middleware",
                    "npm packages → pip packages",
                    "package.json → requirements.txt"
                ],
                "notes": "Flask API风格与Express最相似"
            },
            {
                "target": "fastapi",
                "score": 0.85,
                "adaptations": [
                    "Express routes → FastAPI routes",
                    "Add type hints and Pydantic models",
                    "Async/await pattern preserved",
                    "Automatic API documentation"
                ],
                "notes": "FastAPI提供更现代的特性和自动文档"
            }
        ],
        
        # TypeScript NestJS to Other / TypeScript NestJS到其他语言
        ("nestjs", "typescript", "python"): [
            {
                "target": "fastapi",
                "score": 0.92,
                "adaptations": [
                    "@Controller → FastAPI router class",
                    "@Injectable → Depends()",
                    "TypeORM → SQLAlchemy",
                    "Decorators preserved conceptually"
                ],
                "notes": "FastAPI最接近NestJS的架构模式"
            }
        ],
        
        ("nestjs", "typescript", "java"): [
            {
                "target": "spring-boot",
                "score": 0.95,
                "adaptations": [
                    "@Controller → @RestController",
                    "@Injectable → @Service/@Component",
                    "TypeORM → JPA/Hibernate",
                    "Dependency injection → @Autowired"
                ],
                "notes": "NestJS受Spring启发，迁移很自然"
            }
        ],
        
        # Go Gin to Other / Go Gin到其他语言
        ("gin", "go", "python"): [
            {
                "target": "fastapi",
                "score": 0.85,
                "adaptations": [
                    "Gin routes → FastAPI routes",
                    "Go structs → Pydantic models",
                    "Goroutines → async/await",
                    "Manual error handling → exception handling"
                ],
                "notes": "FastAPI提供类似的性能和异步支持"
            },
            {
                "target": "flask",
                "score": 0.80,
                "adaptations": [
                    "Similar route mapping",
                    "More manual setup required",
                    "Good for simpler APIs"
                ],
                "notes": "Flask更简单但功能较少"
            }
        ],
        
        # Frontend Frameworks / 前端框架
        ("react", "javascript", "vue"): [
            {
                "target": "vue",
                "score": 0.80,
                "adaptations": [
                    "JSX → Vue template syntax",
                    "useState → ref/reactive",
                    "useEffect → watch/watchEffect",
                    "Component structure similar"
                ],
                "notes": "Vue 3 Composition API与React Hooks类似"
            }
        ],
        
        ("vue", "javascript", "react"): [
            {
                "target": "react",
                "score": 0.78,
                "adaptations": [
                    "Vue templates → JSX",
                    "ref/reactive → useState",
                    "watch → useEffect",
                    "Composition API → Hooks"
                ],
                "notes": "React生态系统更大，更多第三方库"
            }
        ]
    }
    
    # Framework feature compatibility / 框架特性兼容性
    FRAMEWORK_FEATURES = {
        "spring-boot": ["rest-api", "dependency-injection", "orm", "security", "testing", "microservices"],
        "django": ["rest-api", "orm", "admin-panel", "authentication", "testing", "full-stack"],
        "fastapi": ["rest-api", "async", "auto-docs", "dependency-injection", "validation", "high-performance"],
        "flask": ["rest-api", "lightweight", "flexible", "extensions"],
        "express": ["rest-api", "middleware", "routing", "lightweight"],
        "nestjs": ["rest-api", "dependency-injection", "decorators", "typescript", "microservices"],
        "gin": ["rest-api", "middleware", "high-performance", "lightweight"],
        "quarkus": ["rest-api", "microservices", "native-compilation", "reactive"],
    }
    
    def __init__(self):
        """Initialize framework mapper / 初始化框架映射器"""
        pass
    
    def get_compatible_frameworks(
        self,
        source_framework: str,
        source_language: str,
        target_language: str
    ) -> List[Dict[str, Any]]:
        """
        Get compatible target frameworks / 获取兼容的目标框架
        
        Args:
            source_framework: Source framework name / 源框架名称
            source_language: Source language / 源语言
            target_language: Target language / 目标语言
            
        Returns:
            List of compatible frameworks with scores / 兼容框架列表及评分
        """
        key = (source_framework, source_language, target_language)
        
        if key in self.FRAMEWORK_MAPPINGS:
            mappings = self.FRAMEWORK_MAPPINGS[key]
            logger.info(f"✅ 找到 {len(mappings)} 个兼容的目标框架")
            return mappings
        else:
            logger.warning(f"⚠️ 未找到 {source_framework} ({source_language}) → {target_language} 的映射")
            return self._suggest_generic_frameworks(target_language)
    
    def _suggest_generic_frameworks(self, target_language: str) -> List[Dict[str, Any]]:
        """
        Suggest generic frameworks when no specific mapping exists
        当不存在特定映射时建议通用框架
        
        Args:
            target_language: Target language / 目标语言
            
        Returns:
            List of generic framework suggestions / 通用框架建议列表
        """
        generic_mappings = {
            "python": [
                {
                    "target": "fastapi",
                    "score": 0.70,
                    "adaptations": ["Manual migration required", "Use FastAPI modern features"],
                    "notes": "FastAPI是Python中最现代的Web框架"
                },
                {
                    "target": "flask",
                    "score": 0.65,
                    "adaptations": ["Manual migration required", "Flexible but requires more setup"],
                    "notes": "Flask轻量灵活，适合小型项目"
                }
            ],
            "java": [
                {
                    "target": "spring-boot",
                    "score": 0.70,
                    "adaptations": ["Manual migration required", "Use Spring Boot ecosystem"],
                    "notes": "Spring Boot是Java生态的标准选择"
                }
            ],
            "typescript": [
                {
                    "target": "nestjs",
                    "score": 0.70,
                    "adaptations": ["Manual migration required", "Use NestJS architecture"],
                    "notes": "NestJS提供企业级TypeScript框架"
                }
            ],
            "go": [
                {
                    "target": "gin",
                    "score": 0.70,
                    "adaptations": ["Manual migration required", "Use Gin for performance"],
                    "notes": "Gin是Go中最流行的Web框架"
                }
            ]
        }
        
        return generic_mappings.get(target_language, [])
    
    def get_best_match(
        self,
        source_framework: str,
        source_language: str,
        target_language: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get the best matching target framework / 获取最佳匹配的目标框架
        
        Args:
            source_framework: Source framework / 源框架
            source_language: Source language / 源语言
            target_language: Target language / 目标语言
            
        Returns:
            Best matching framework / 最佳匹配框架
        """
        frameworks = self.get_compatible_frameworks(
            source_framework,
            source_language,
            target_language
        )
        
        if frameworks:
            best = max(frameworks, key=lambda x: x["score"])
            logger.info(f"🎯 最佳匹配: {best['target']} (相似度: {best['score']:.0%})")
            return best
        
        return None
    
    def compare_frameworks(
        self,
        source_framework: str,
        target_frameworks: List[str]
    ) -> Dict[str, float]:
        """
        Compare feature compatibility between frameworks
        比较框架之间的特性兼容性
        
        Args:
            source_framework: Source framework / 源框架
            target_frameworks: List of target frameworks / 目标框架列表
            
        Returns:
            Dictionary of compatibility scores / 兼容性分数字典
        """
        source_features = set(self.FRAMEWORK_FEATURES.get(source_framework, []))
        
        if not source_features:
            return {fw: 0.5 for fw in target_frameworks}  # Unknown framework
        
        scores = {}
        for target in target_frameworks:
            target_features = set(self.FRAMEWORK_FEATURES.get(target, []))
            if target_features:
                # Calculate Jaccard similarity / 计算Jaccard相似度
                intersection = len(source_features & target_features)
                union = len(source_features | target_features)
                scores[target] = intersection / union if union > 0 else 0.0
            else:
                scores[target] = 0.5  # Unknown target framework
        
        return scores

