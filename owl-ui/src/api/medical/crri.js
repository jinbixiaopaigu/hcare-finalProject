import request from '@/utils/request'

// 查询连续RRI数据列表
function list(query) {
  return request({
    url: '/medical/crri/list',
    method: 'get',
    params: query,
    timeout: 60000  // 增加超时时间到60秒，以便处理大量数据
  })
}

// 查询连续RRI数据详细
function getContinuousRRI(id) {
  return request({
    url: '/medical/crri/' + id,
    method: 'get'
  })
}

// 新增连续RRI数据
function addContinuousRRI(data) {
  return request({
    url: '/medical/crri',
    method: 'post',
    data: data
  })
}

// 修改连续RRI数据
function updateContinuousRRI(data) {
  return request({
    url: '/medical/crri',
    method: 'put',
    data: data
  })
}

// 删除连续RRI数据
function delContinuousRRI(id) {
  return request({
    url: '/medical/crri/' + id,
    method: 'delete'
  })
}

// 同步连续RRI数据
function syncContinuousRRI() {
  return request({
    url: '/medical/crri/sync',
    method: 'post'
  })
}

// 获取RRI数据图表
function getRRIChart(query) {
  return request({
    url: '/medical/crri/chart',
    method: 'get',
    params: query,
    timeout: 120000  // 设置更长的超时时间(2分钟)，因为图表生成可能需要处理大量数据
  })
}

// 统一导出API函数
export {
  list,
  getContinuousRRI as getDetail,
  addContinuousRRI as add,
  updateContinuousRRI as update,
  delContinuousRRI as delete,
  syncContinuousRRI as sync,
  getRRIChart as getChart
} 