export const continuousBloodOxygenConfig = {
  // 模块配置
  module: 'medical',
  apiPath: 'cbo',
  title: '连续血氧数据',
  
  // 搜索字段配置
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
      prop: 'data_time_range',
      label: '时间范围',
      type: 'daterange',
      props: {
        valueFormat: 'YYYY-MM-DD',
        format: 'YYYY-MM-DD',
        rangeSeparator: '至',
        startPlaceholder: '开始日期',
        endPlaceholder: '结束日期'
      }
    }
  ],
  
  // 工具栏按钮
  toolbarButtons: [
    {
      icon: 'Plus',
      label: '新增',
      type: 'primary',
      permission: 'add',
      onClick: 'handleAdd'
    },
    {
      icon: 'Refresh',
      label: '同步',
      type: 'success',
      permission: 'sync',
      onClick: 'syncData',
      loading: 'syncLoading' // 关联加载状态
    }
  ],
  
  // 表格列配置
  tableColumns: [
    {
      prop: 'userId',
      label: '用户ID',
      width: 180
    },
    {
      prop: 'spo2AvgValue',
      label: '血氧值',
      width: 100,
      formatter: (row) => `${row.spo2AvgValue || '-'}${row.spo2AvgUnit || '%'}`
    },
    {
      prop: 'dataTime',
      label: '数据时间',
      width: 180,
      type: 'time'
    },
    {
      prop: 'uploadTime',
      label: '上传时间',
      width: 180,
      type: 'time'
    }
  ],
  
  // 表单字段配置
  formFields: [
    {
      prop: 'id',
      label: 'ID',
      type: 'input',
      span: 12,
      props: {
        disabled: true
      }
    },
    {
      prop: 'userId',
      label: '用户ID',
      type: 'input',
      span: 12,
      props: {
        disabled: (config) => config.title.includes('详情')
      }
    },
    {
      prop: 'spo2AvgValue',
      label: '血氧值',
      type: 'input',
      span: 12,
      props: {
        append: '%',
        disabled: (config) => config.title.includes('详情')
      }
    },
    {
      prop: 'dataTime',
      label: '数据时间',
      type: 'datetime',
      span: 12,
      props: {
        valueFormat: 'yyyy-MM-dd HH:mm:ss',
        disabled: (config) => config.title.includes('详情')
      }
    },
    {
      prop: 'uploadTime',
      label: '上传时间',
      type: 'datetime',
      span: 12,
      props: {
        valueFormat: 'yyyy-MM-dd HH:mm:ss',
        disabled: (config) => config.title.includes('详情')
      }
    }
  ],
  
  // 表单验证规则
  formRules: {
    userId: [
      { required: true, message: '用户ID不能为空', trigger: 'blur' }
    ],
    dataTime: [
      { required: true, message: '数据时间不能为空', trigger: 'blur' }
    ]
  },
  
  // 数据转换方法
  transformRequest: (data) => {
    // 转换字段命名风格为snake_case
    return {
      id: data.id,
      user_id: data.userId,
      spo2_avg_value: data.spo2AvgValue,
      data_time: data.dataTime,
      upload_time: data.uploadTime
    }
  },
  
  transformResponse: (data) => {
    // 转换字段命名风格为camelCase
    return {
      id: data.id,
      userId: data.user_id,
      spo2AvgValue: data.spo2_avg_value,
      spo2AvgUnit: data.spo2_avg_unit || '%',
      dataTime: data.data_time,
      uploadTime: data.upload_time
    }
  }
}