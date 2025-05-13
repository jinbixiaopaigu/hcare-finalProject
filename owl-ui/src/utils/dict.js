import request from '@/utils/request'

export function useDict() {
  const getDict = (dictType) => {
    return request({
      url: '/system/dict/data/type/' + dictType,
      method: 'get'
    })
  }
  return { getDict }
}

export function getDictOptions(dictType) {
  return request({
    url: '/system/dict/data/type/' + dictType,
    method: 'get'
  }).then(res => {
    return res.data.map(item => ({
      label: item.dictLabel,
      value: item.dictValue,
      ...item
    }))
  })
}