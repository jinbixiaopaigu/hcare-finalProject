import request from '@/utils/request'

// 获取房颤测量结果列表
export function getAtrialFibrillationList(params) {
  return request({
    url: '/medical/af/list',  // 与其他API保持一致的路径风格
    method: 'get',
    params
  })
}

// 获取房颤测量结果详情
export function getAtrialFibrillationDetail(id) {
  return request({
    url: `/medical/af/${id}`,  // 与其他API保持一致的路径风格
    method: 'get'
  })
}