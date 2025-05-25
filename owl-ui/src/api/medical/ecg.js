import request from '@/utils/request'

// 查询ECG数据列表
function list(query) {
  return request({
    url: '/medical/ecg/list',
    method: 'get',
    params: query
  })
}

// 查询ECG数据详细
function getECG(id) {
  return request({
    url: '/medical/ecg/' + id,
    method: 'get'
  })
}

// 新增ECG数据
function addECG(data) {
  return request({
    url: '/medical/ecg',
    method: 'post',
    data: data
  })
}

// 修改ECG数据
function updateECG(data) {
  return request({
    url: '/medical/ecg',
    method: 'put',
    data: data
  })
}

// 删除ECG数据
function delECG(id) {
  return request({
    url: '/medical/ecg/' + id,
    method: 'delete'
  })
}

// 同步ECG数据
function syncECG() {
  return request({
    url: '/medical/ecg/sync',
    method: 'post'
  })
}

// 统一导出API函数
export {
  list,
  getECG as getDetail,
  addECG as add,
  updateECG as update,
  delECG as delete,
  syncECG as sync
} 