import { listBo, getBo, addBo, updateBo, delBo } from './medical/bo'
import { listCbo, getCbo, addCbo, updateCbo, delCbo } from './medical/cbo'
import { listCbt, getCbt, addCbt, updateCbt, delCbt } from './medical/cbt'
import { listSwd, getSwd, addSwd, updateSwd, delSwd } from './medical/swd'
import medical from './medical'

// 添加调试日志
console.log('医疗模块定义:', medical);
console.log('crri API路径:', medical.crri);

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
    swd: {
      list: listSwd,
      getDetail: getSwd,
      add: addSwd,
      update: updateSwd,
      delete: delSwd
    }
  },
  medical
}

export * from './medical'