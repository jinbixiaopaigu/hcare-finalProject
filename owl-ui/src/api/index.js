import { listBo, getBo, addBo, updateBo, delBo } from './medical/bo'
import { listCbo, getCbo, addCbo, updateCbo, delCbo } from './medical/cbo'
import { listCbt, getCbt, addCbt, updateCbt, delCbt } from './medical/cbt'
import { listContinuousRRI, getContinuousRRI, addContinuousRRI, updateContinuousRRI, delContinuousRRI, syncContinuousRRI } from './medical/crri'
import medical from './medical'

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
    },
    cbt: {
      list: listCbt,
      getDetail: getCbt,
      add: addCbt,
      update: updateCbt,
      delete: delCbt
    },
    crri: {
      list: listContinuousRRI,
      getDetail: getContinuousRRI,
      add: addContinuousRRI,
      update: updateContinuousRRI,
      delete: delContinuousRRI,
      sync: syncContinuousRRI
    }
  },
  medical
}

export * from './medical'