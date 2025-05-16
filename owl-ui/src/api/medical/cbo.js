import request from '@/utils/request'

// 查询连续血氧数据列表
export function listCbo(query) {
  return request({
    url: '/medical/cbo/list',
    method: 'get',
    params: query
  })
}

// 查询连续血氧数据详细
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

// 修改连续血氧数据
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

// 同步连续血氧数据
export function syncCbo() {
  return request({
    url: '/medical/cbo/sync',
    method: 'post'
  })
}