import request from '@/utils/request'

// 查询连续RRI数据列表
export function listContinuousRRI(query) {
  return request({
    url: '/medical/continuousRRI/list',
    method: 'get',
    params: query
  })
}

// 查询连续RRI数据详细
export function getContinuousRRI(id) {
  return request({
    url: '/medical/continuousRRI/' + id,
    method: 'get'
  })
}

// 新增连续RRI数据
export function addContinuousRRI(data) {
  return request({
    url: '/medical/continuousRRI',
    method: 'post',
    data: data
  })
}

// 修改连续RRI数据
export function updateContinuousRRI(data) {
  return request({
    url: '/medical/continuousRRI',
    method: 'put',
    data: data
  })
}

// 删除连续RRI数据
export function delContinuousRRI(id) {
  return request({
    url: '/medical/continuousRRI/' + id,
    method: 'delete'
  })
}

// 同步连续RRI数据
export function syncContinuousRRI() {
  return request({
    url: '/medical/continuousRRI/sync',
    method: 'post'
  })
} 