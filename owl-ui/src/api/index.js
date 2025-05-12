import { listBo, getBo, addBo, updateBo, delBo } from './medical/bo'

export default {
  medical: {
    bo: {
      list: listBo,
      getDetail: getBo,
      add: addBo,
      update: updateBo,
      delete: delBo
    }
  }
}