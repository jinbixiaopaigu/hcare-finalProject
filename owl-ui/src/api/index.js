import { listBo, getBo, addBo, updateBo, delBo } from './medical/bo'
import { listCbo, getCbo, addCbo, updateCbo, delCbo } from './medical/cbo'

export default {
  medical: {
    bo: {
      list: listBo,
      getDetail: getBo,
      add: addBo,
      update: updateBo,
      delete: delBo
    },
    cbo: {
      list: listCbo,
      getDetail: getCbo,
      add: addCbo,
      update: updateCbo,
      delete: delCbo
    }
  }
}