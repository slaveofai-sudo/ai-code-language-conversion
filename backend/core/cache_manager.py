"""
Cache Manager / 缓存管理器

Provides caching functionality for translation results using Redis.
使用Redis为翻译结果提供缓存功能。

Features / 功能:
- Translation result caching / 翻译结果缓存
- Automatic expiration / 自动过期
- Cache statistics / 缓存统计
- Cache invalidation / 缓存失效
"""

import hashlib
import json
from typing import Optional, Any, Dict
from functools import wraps
import asyncio
from loguru import logger

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, caching will be disabled")


class CacheManager:
    """
    Cache Manager for translation results / 翻译结果缓存管理器
    
    Uses Redis for high-performance caching with automatic expiration.
    使用Redis进行高性能缓存，支持自动过期。
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        default_ttl: int = 3600  # 1 hour
    ):
        """
        Initialize cache manager / 初始化缓存管理器
        
        Args:
            redis_url: Redis connection URL / Redis连接URL
            default_ttl: Default cache TTL in seconds / 默认缓存TTL（秒）
        """
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.redis_client = None
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "errors": 0
        }
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                logger.info(f"✅ Redis cache initialized: {redis_url}")
            except Exception as e:
                logger.error(f"❌ Failed to connect to Redis: {e}")
                self.redis_client = None
        else:
            logger.warning("⚠️ Redis not installed, using in-memory fallback cache")
            self._memory_cache: Dict[str, Any] = {}
    
    def _generate_cache_key(
        self,
        source_code: str,
        source_language: str,
        target_language: str,
        ai_model: str,
        **kwargs
    ) -> str:
        """
        Generate unique cache key / 生成唯一的缓存键
        
        Uses SHA256 hash of code content and parameters.
        使用代码内容和参数的SHA256哈希。
        
        Args:
            source_code: Source code / 源代码
            source_language: Source language / 源语言
            target_language: Target language / 目标语言
            ai_model: AI model name / AI模型名称
            **kwargs: Additional parameters / 额外参数
            
        Returns:
            str: Cache key / 缓存键
        """
        # Create a unique string from all parameters / 从所有参数创建唯一字符串
        key_data = f"{source_code}:{source_language}:{target_language}:{ai_model}"
        
        # Add additional parameters / 添加额外参数
        for key, value in sorted(kwargs.items()):
            key_data += f":{key}:{value}"
        
        # Generate hash / 生成哈希
        hash_obj = hashlib.sha256(key_data.encode('utf-8'))
        cache_key = f"translation:{hash_obj.hexdigest()}"
        
        return cache_key
    
    async def get(self, cache_key: str) -> Optional[str]:
        """
        Get cached value / 获取缓存值
        
        Args:
            cache_key: Cache key / 缓存键
            
        Returns:
            Cached value or None / 缓存值或None
        """
        try:
            if self.redis_client:
                # Get from Redis / 从Redis获取
                value = await self.redis_client.get(cache_key)
                if value:
                    self.stats["hits"] += 1
                    logger.debug(f"✅ Cache HIT: {cache_key[:16]}...")
                    return value
                else:
                    self.stats["misses"] += 1
                    logger.debug(f"❌ Cache MISS: {cache_key[:16]}...")
                    return None
            else:
                # Fallback to in-memory cache / 回退到内存缓存
                value = self._memory_cache.get(cache_key)
                if value:
                    self.stats["hits"] += 1
                    return value
                else:
                    self.stats["misses"] += 1
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Cache get error: {e}")
            self.stats["errors"] += 1
            return None
    
    async def set(
        self,
        cache_key: str,
        value: str,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set cache value / 设置缓存值
        
        Args:
            cache_key: Cache key / 缓存键
            value: Value to cache / 要缓存的值
            ttl: Time to live in seconds / 生存时间（秒）
            
        Returns:
            bool: Success status / 成功状态
        """
        try:
            ttl = ttl or self.default_ttl
            
            if self.redis_client:
                # Set in Redis with expiration / 在Redis中设置并带过期时间
                await self.redis_client.setex(cache_key, ttl, value)
                self.stats["sets"] += 1
                logger.debug(f"💾 Cache SET: {cache_key[:16]}... (TTL: {ttl}s)")
                return True
            else:
                # Fallback to in-memory cache / 回退到内存缓存
                self._memory_cache[cache_key] = value
                self.stats["sets"] += 1
                # Schedule cleanup (simple approach) / 安排清理
                asyncio.create_task(self._cleanup_memory_cache(cache_key, ttl))
                return True
                
        except Exception as e:
            logger.error(f"❌ Cache set error: {e}")
            self.stats["errors"] += 1
            return False
    
    async def _cleanup_memory_cache(self, key: str, ttl: int):
        """Clean up expired memory cache entries / 清理过期的内存缓存条目"""
        await asyncio.sleep(ttl)
        if key in self._memory_cache:
            del self._memory_cache[key]
    
    async def delete(self, cache_key: str) -> bool:
        """
        Delete cache entry / 删除缓存条目
        
        Args:
            cache_key: Cache key / 缓存键
            
        Returns:
            bool: Success status / 成功状态
        """
        try:
            if self.redis_client:
                await self.redis_client.delete(cache_key)
            else:
                if cache_key in self._memory_cache:
                    del self._memory_cache[cache_key]
            return True
        except Exception as e:
            logger.error(f"❌ Cache delete error: {e}")
            return False
    
    async def clear_all(self) -> bool:
        """
        Clear all cache entries / 清空所有缓存条目
        
        Returns:
            bool: Success status / 成功状态
        """
        try:
            if self.redis_client:
                # Delete all translation keys / 删除所有翻译键
                cursor = 0
                while True:
                    cursor, keys = await self.redis_client.scan(
                        cursor,
                        match="translation:*",
                        count=100
                    )
                    if keys:
                        await self.redis_client.delete(*keys)
                    if cursor == 0:
                        break
            else:
                self._memory_cache.clear()
            
            logger.info("🧹 Cache cleared successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Cache clear error: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics / 获取缓存统计
        
        Returns:
            dict: Cache statistics / 缓存统计
        """
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "sets": self.stats["sets"],
            "errors": self.stats["errors"],
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "cache_backend": "redis" if self.redis_client else "memory"
        }
    
    async def get_cache_size(self) -> int:
        """
        Get total number of cached items / 获取缓存项总数
        
        Returns:
            int: Number of cached items / 缓存项数量
        """
        try:
            if self.redis_client:
                cursor = 0
                count = 0
                while True:
                    cursor, keys = await self.redis_client.scan(
                        cursor,
                        match="translation:*",
                        count=100
                    )
                    count += len(keys)
                    if cursor == 0:
                        break
                return count
            else:
                return len(self._memory_cache)
        except Exception as e:
            logger.error(f"❌ Error getting cache size: {e}")
            return 0
    
    async def close(self):
        """Close Redis connection / 关闭Redis连接"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed")


def cache_translation(cache_manager: CacheManager, ttl: Optional[int] = None):
    """
    Decorator to cache translation results / 装饰器用于缓存翻译结果
    
    Usage / 使用方法:
    ```python
    @cache_translation(cache_manager, ttl=3600)
    async def translate_code(source_code, source_lang, target_lang, ai_model):
        # Translation logic here
        return translated_code
    ```
    
    Args:
        cache_manager: CacheManager instance / CacheManager实例
        ttl: Cache TTL in seconds / 缓存TTL（秒）
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(source_code: str, source_language: str, target_language: str, ai_model: str, *args, **kwargs):
            # Generate cache key / 生成缓存键
            cache_key = cache_manager._generate_cache_key(
                source_code,
                source_language,
                target_language,
                ai_model,
                **kwargs
            )
            
            # Try to get from cache / 尝试从缓存获取
            cached_result = await cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"🎯 Using cached translation (saved API call)")
                return cached_result
            
            # Execute translation / 执行翻译
            logger.info(f"🔄 No cache, executing translation...")
            result = await func(source_code, source_language, target_language, ai_model, *args, **kwargs)
            
            # Store in cache / 存入缓存
            if result:
                await cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator


# Global cache manager instance / 全局缓存管理器实例
_cache_manager_instance = None

def get_cache_manager() -> CacheManager:
    """
    Get global cache manager instance / 获取全局缓存管理器实例
    
    Returns:
        CacheManager: Cache manager instance / 缓存管理器实例
    """
    global _cache_manager_instance
    if _cache_manager_instance is None:
        import os
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        _cache_manager_instance = CacheManager(redis_url=redis_url)
    return _cache_manager_instance

