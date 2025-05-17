import * as bo from './bo'
import * as cbo from './cbo'
import * as af from './atrialFibrillation'
import * as cbt from './cbt'
import * as chr from './chr'
import * as crri from './crri'
import * as swd from './swd'

// 添加调试日志
console.log('医疗模块加载:', {
  bo,
  cbo,
  af,
  cbt,
  chr,
  crri,
  swd
});

export default {
  bo,
  cbo,
  af,
  cbt,
  chr,
  crri,
  swd
}

