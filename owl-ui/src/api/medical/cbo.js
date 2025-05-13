import request from '@/utils/request'

// 获取连续血氧数据列表
export function listCbo(params) {
  console.log('发送连续血氧列表请求，参数:', params)
  return request({
    url: '/medical/cbo/list',
    method: 'get',
    params
  }).then(response => {
    console.log('收到连续血氧列表响应:', response)
    return response
  }).catch(error => {
    console.error('连续血氧列表请求错误:', error)
    throw error
  })
}

// 获取连续血氧数据详情
export function getCbo(id) {
  return request({
    url: `/medical/cbo/${id}`,
    method: 'get'
  })
}

// 新增连续血氧数据
export function addCbo(data) {
  return request({
    url: '/medical/cbo',
    method: 'post',
    data: data
  })
}

// 更新连续血氧数据
export function updateCbo(data) {
  return request({
    url: '/medical/cbo',
    method: 'put',
    data: data
  })
}

// 删除连续血氧数据
export function delCbo(id) {
  return request({
    url: `/medical/cbo/${id}`,
    method: 'delete'
  })
}