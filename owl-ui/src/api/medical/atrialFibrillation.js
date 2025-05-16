import request from '@/utils/request'

// 查询房颤检测结果列表
export function getAtrialFibrillationList(query) {
  return request({
    url: '/medical/af/list',
    method: 'get',
    params: query
  })
}

// 同步房颤检测结果数据
export function syncAtrialFibrillation() {
  return request({
    url: '/medical/af/sync',
    method: 'post'
  })
}

// 获取房颤测量结果详情
export function getAtrialFibrillationDetail(id) {
  return request({
    url: `/medical/af/${id}`,  // 与其他API保持一致的路径风格
    method: 'get'
  })
}