import request from '@/utils/request'

const apiPath = '/medical/cbt'

export function listCbt(params) {
  console.log('[API] listCbt params:', params)
  return request({
    url: apiPath + '/list',
    method: 'get',
    params
  })
}

export function getCbt(id) {
  console.log('[API] getCbt id:', id)
  return request({
    url: apiPath + '/' + id,
    method: 'get'
  })
}

export function addCbt(data) {
  console.log('[API] addCbt data:', data)
  return request({
    url: apiPath,
    method: 'post',
    data
  })
}

export function updateCbt(data) {
  console.log('[API] updateCbt data:', data)
  return request({
    url: apiPath,
    method: 'put',
    data
  })
}

export function delCbt(id) {
  console.log('[API] delCbt id:', id)
  return request({
    url: apiPath + '/' + id,
    method: 'delete'
  })
}

// 批量删除
export function batchDelCbt(ids) {
  console.log('[API] batchDelCbt ids:', ids)
  return request({
    url: apiPath + '/batch',
    method: 'delete',
    data: ids
  })
}

// 导出数据
export function exportCbt(params) {
  console.log('[API] exportCbt params:', params)
  return request({
    url: apiPath + '/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}