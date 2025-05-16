import request from '@/utils/request'

// 查询连续心率数据列表
export function list(query) {
  return request({
    url: '/medical/chr/list',
    method: 'get',
    params: query
  })
}

// 查询连续心率数据详细
export function getDetail(id) {
  return request({
    url: '/medical/chr/' + id,
    method: 'get'
  })
}

// 新增连续心率数据
export function add(data) {
  return request({
    url: '/medical/chr',
    method: 'post',
    data: data
  })
}

// 修改连续心率数据
export function update(data) {
  return request({
    url: '/medical/chr',
    method: 'put',
    data: data
  })
}

// 删除连续心率数据
export function del(id) {
  return request({
    url: '/medical/chr/' + id,
    method: 'delete'
  })
}

// 同步连续心率数据
export function sync() {
  return request({
    url: '/medical/chr/sync',
    method: 'post'
  })
} 