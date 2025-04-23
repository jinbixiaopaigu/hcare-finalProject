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
    // 处理不同类型的返回数据
    let names = []
    if (Array.isArray(response.data)) {
      names = response.data
    } else if (response.data && typeof response.data === 'object') {
      names = Object.keys(response.data)
    }
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
  }).then(response => {
    console.log('缓存键名原始数据:', response.data)
    
    // 处理不同类型的返回数据
    let processedData = [];
    if (Array.isArray(response.data)) {
      processedData = response.data.map(item => {
        // 尝试拆分键值对
        const [key, ...valueParts] = item.cacheKey.split(': ')
        const value = valueParts.join(': ').trim()
        
        return {
          cacheKey: key,
          keyValue: value,
          original: item.cacheKey // 保留原始数据用于调试
        }
      });
    } else if (response.data && typeof response.data === 'object') {
      // 检查是否是Redis info命令返回的数据
      if (response.config?.url?.includes('cache/info')) {
        // 按行分割info数据
        const infoLines = response.data.split('\r\n');
        processedData = infoLines
          .filter(line => line && !line.startsWith('#'))
          .map(line => {
            const [key, ...valueParts] = line.split(':');
            const value = valueParts.join(':').trim();
            return {
              cacheKey: key.trim(),
              keyValue: value,
              original: line
            };
          });
      } else {
        // 普通对象数据
        processedData = Object.entries(response.data).map(([key, value]) => {
          return {
            cacheKey: key,
            keyValue: JSON.stringify(value),
            original: key
          }
        });
      }
    }
    
    console.log('转换后的缓存键名数据:', processedData)
    return {
      code: response.code,
      msg: response.msg,
      data: response.data, // 保留原始数据
      processedData: processedData // 明确返回处理后的数据
    }
  }).catch(error => {
    console.error('获取缓存键名失败:', error)
    throw error
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