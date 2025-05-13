export const continuousBloodOxygenConfig = {
  title: '连续血氧数据',
  apiModule: 'medical',
  apiPath: 'cbo',
  permissionPrefix: 'medical:cbo',
  
  // 搜索字段配置
  searchFields: [
    {
      prop: 'userId',
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
        valueFormat: 'YYYY-MM-DD HH:mm:ss',
        format: 'YYYY-MM-DD',
        rangeSeparator: '至',
        startPlaceholder: '开始日期',
        endPlaceholder: '结束日期'
      }
    }
  ],
  
  // 表格列配置
  tableColumns: [
    {
      prop: 'userId',
      label: '用户ID',
      width: 120,
      field: 'userId',
      align: 'center'
    },
    {
      prop: 'spo2Value',
      label: '血氧饱和度',
      width: 120,
      field: 'spo2Value',
      align: 'center',
      formatter: (row) => {
        const value = row.spo2Value ? Number(row.spo2Value).toFixed(2) : '--'
        const unit = row.spo2Unit || '%'
        return `${value}${unit}`
      }
    },
    {
      prop: 'dataTime',
      label: '数据时间',
      width: 180,
      field: 'dataTime',
      type: 'time',
      align: 'center'
    },
    {
      prop: 'uploadTime',
      label: '上传时间',
      width: 180,
      field: 'uploadTime',
      type: 'time',
      align: 'center'
    }
  ],
  
  // 表单字段配置
  formFields: [
    {
      prop: 'id',
      label: '数据ID',
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
      prop: 'spo2Value',
      label: '血氧饱和度',
      type: 'input',
      span: 12,
      props: {
        append: '%',
        type: 'number',
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
  rules: {
    userId: [
      { required: true, message: '用户ID不能为空', trigger: 'blur' }
    ],
    spo2Value: [
      { required: true, message: '血氧饱和度不能为空', trigger: 'blur' },
      { type: 'number', min: 0, max: 100, message: '血氧饱和度必须在0-100之间', trigger: 'blur' }
    ],
    heartRate: [
      { required: true, message: '心率不能为空', trigger: 'blur' },
      { type: 'number', min: 0, max: 300, message: '心率必须在0-300之间', trigger: 'blur' }
    ],
    dataTime: [
      { required: true, message: '数据时间不能为空', trigger: 'blur' }
    ],
    deviceId: [
      { required: true, message: '设备ID不能为空', trigger: 'blur' }
    ]
  },
  
  // 数据转换方法
  transformRequest: (data) => {
    // 处理搜索参数
    if (data.userId) {
      data.user_id = data.userId
      delete data.userId
    }
    
    // 处理表单数据
    if (data.spo2Value !== undefined) {
      return {
        id: data.id,
        user_id: data.userId,
        spo2_value: data.spo2Value,
        data_time: data.dataTime,
        upload_time: data.uploadTime
      }
    }
    
    return data
  },
  
  transformResponse: (response) => {
    // 处理列表数据
    if (Array.isArray(response)) {
      return response.map(item => ({
        id: item.id,
        userId: item.user_id,
        spo2Value: item.spo2_value,
        spo2Unit: item.spo2_unit,
        dataTime: item.data_time,
        uploadTime: item.upload_time
      }))
    }
    
    // 处理单条数据
    return {
      id: response.id,
      userId: response.user_id,
      spo2Value: response.spo2_value,
      spo2Unit: response.spo2_unit,
      dataTime: response.data_time,
      uploadTime: response.upload_time
    }
  }
}