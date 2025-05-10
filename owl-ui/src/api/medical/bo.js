import request from '@/utils/request'

// 获取血氧饱和度数据列表
export function listBo(params) {
  return request({
    url: '/medical/bo/list',
    method: 'get',
    params
  })
}

// 获取血氧饱和度数据详情
export function getBo(id) {
  return request({
    url: `/medical/bo/${id}`,
    method: 'get'
  })
}

// 新增血氧饱和度数据
export function addBo(data) {
  return request({
    url: '/medical/bo',
    method: 'post',
    data: data
  })
}

// 更新血氧饱和度数据
export function updateBo(data) {
  return request({
    url: '/medical/bo',
    method: 'put',
    data: data
  })
}

// 删除血氧饱和度数据
export function delBo(id) {
  return request({
    url: `/medical/bo/${id}`,
    method: 'delete'
  })
}