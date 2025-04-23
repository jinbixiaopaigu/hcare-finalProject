import request from '@/utils/request'

// 查询缓存详细
export function getCache() {
  return request({
    url: '/monitor/cache',
    method: 'get'
  })
}

// 查询缓存名称列表
export function listCacheName() {
  console.log('请求缓存数据...')
  return request({
    url: '/monitor/cache',
    method: 'get'
  }).then(response => {
    console.log('缓存接口响应:', response)
    // 从完整缓存数据中提取名称列表
    const names = response.data ? Object.keys(response.data) : []
    console.log('提取的缓存名称列表:', names)
    return names
  }).catch(error => {
    console.error('获取缓存名称列表失败:', error)
    throw error
  })
}

// 查询缓存键名列表
export function listCacheKey(cacheName) {
  return request({
    url: '/monitor/cache/keys/' + cacheName,
    method: 'get'
  })
}

// 查询缓存内容
export function getCacheValue(cacheName, cacheKey) {
  return request({
    url: '/monitor/cache/getValue/' + cacheName + '/' + cacheKey,
    method: 'get'
  })
}

// 清理指定名称缓存
export function clearCacheName(cacheName) {
  return request({
    url: '/monitor/cache/clearCacheName/' + cacheName,
    method: 'delete'
  })
}

// 清理指定键名缓存
export function clearCacheKey(cacheKey) {
  return request({
    url: '/monitor/cache/clearCacheKey/' + cacheKey,
    method: 'delete'
  })
}

// 清理全部缓存
export function clearCacheAll() {
  return request({
    url: '/monitor/cache/clearCacheAll',
    method: 'delete'
  })
}