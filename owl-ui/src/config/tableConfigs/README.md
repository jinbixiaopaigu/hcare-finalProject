# 通用表格页面配置指南

## 配置文件结构

每个表的配置文件应包含以下部分：

```javascript
export const tableNameConfig = {
  title: '页面标题',
  apiModule: 'API模块名', 
  apiPath: 'API路径',
  permissionPrefix: '权限前缀',
  
  // 搜索字段配置
  searchFields: [],
  
  // 表格列配置  
  tableColumns: [],
  
  // 表单字段配置
  formFields: [],
  
  // 表单验证规则
  rules: {},
  
  // 数据转换方法
  transformRequest: (data) => {},
  transformResponse: (data) => {}
}
```

## 配置项说明

### 1. 搜索字段配置 (searchFields)

```javascript
searchFields: [
  {
    prop: '字段名',
    label: '标签文本',
    type: '组件类型', // input/select/date/daterange等
    props: { // 组件属性
      placeholder: '提示文本',
      options: [] // 仅select类型需要
    }
  }
]
```

### 2. 表格列配置 (tableColumns)

```javascript 
tableColumns: [
  {
    prop: '字段名',
    label: '列名',
    width: '宽度',
    type: '特殊类型', // dict/time等
    formatter: (row) => {} // 自定义格式化函数
  }
]
```

### 3. 表单字段配置 (formFields)

```javascript
formFields: [
  {
    prop: '字段名',
    label: '标签文本', 
    type: '组件类型',
    span: 12, // 占据的列数(24为一整行)
    props: {
      disabled: (config) => {}, // 动态禁用
      options: [] // 仅select需要
    }
  }
]
```

### 4. 表单验证规则 (rules)

```javascript
rules: {
  fieldName: [
    { required: true, message: '错误提示', trigger: '触发方式' },
    { validator: (rule, value, callback) => {} } // 自定义验证
  ]
}
```

### 5. 数据转换方法

```javascript
// 请求数据转换
transformRequest: (data) => {
  return {
    api_field: data.formField
  }
},

// 响应数据转换  
transformResponse: (data) => {
  return {
    formField: data.api_field
  }
}
```

## 添加新表示例

以添加"血压数据"表为例：

1. 创建配置文件 `bloodPressure.js`:

```javascript
import { getDictOptions } from '@/utils/dict'

export const bloodPressureConfig = {
  title: '血压数据',
  apiModule: 'medical',
  apiPath: 'bp',
  permissionPrefix: 'medical:bp',
  
  searchFields: [
    {
      prop: 'user_id',
      label: '用户ID',
      type: 'input',
      props: {
        placeholder: '请输入用户ID'
      }
    },
    {
      prop: 'measure_type',
      label: '测量类型',
      type: 'select',
      props: {
        options: getDictOptions('measure_type'),
        placeholder: '请选择测量类型'
      }
    }
  ],
  
  tableColumns: [
    {
      prop: 'user_id',
      label: '用户ID',
      width: 120
    },
    {
      prop: 'systolic',
      label: '收缩压',
      width: 100
    },
    {
      prop: 'diastolic', 
      label: '舒张压',
      width: 100
    }
  ],
  
  formFields: [
    {
      prop: 'user_id',
      label: '用户ID',
      type: 'input',
      span: 12
    },
    {
      prop: 'systolic',
      label: '收缩压',
      type: 'input',
      span: 12,
      props: {
        type: 'number'
      }
    }
  ],
  
  rules: {
    user_id: [
      { required: true, message: '用户ID不能为空' }
    ],
    systolic: [
      { required: true, message: '收缩压不能为空' }
    ]
  }
}
```

2. 创建页面组件 `bloodPressure/index.vue`:

```vue
<template>
  <BaseTablePage :config="config" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { bloodPressureConfig } from '@/config/tableConfigs/bloodPressure'

export default {
  name: 'BloodPressure',
  components: { BaseTablePage },
  data() {
    return {
      config: bloodPressureConfig
    }
  }
}
</script>
```

## 注意事项

1. 保持字段命名一致性
2. 复杂逻辑可在页面组件中覆盖默认方法
3. 保留必要的调试日志
4. 确保数据转换正确处理字段映射
5. 表单验证规则应与后端验证保持一致