import request from '@/utils/request'

// 获取6分钟行走测试数据列表
export function listSwd(params) {
  return request({
    url: '/medical/swd/list',
    method: 'get',
    params
  })
}

// 获取6分钟行走测试数据详情
export function getSwd(id) {
  return request({
    url: `/medical/swd/${id}`,
    method: 'get'
  })
}

// 新增6分钟行走测试数据
export function addSwd(data) {
  return request({
    url: '/medical/swd',
    method: 'post',
    data: data
  })
}

// 更新6分钟行走测试数据
export function updateSwd(data) {
  return request({
    url: '/medical/swd',
    method: 'put',
    data: data
  })
}

// 删除6分钟行走测试数据
export function delSwd(id) {
  return request({
    url: `/medical/swd/${id}`,
    method: 'delete'
  })
}

// 同步6分钟行走测试数据
export function syncSwd() {
  return request({
    url: '/medical/swd/sync',
    method: 'post'
  })
} 