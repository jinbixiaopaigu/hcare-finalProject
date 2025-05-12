export const bloodOxygenConfig = {
  title: '血氧数据',
  apiModule: 'medical', // API模块名
  apiPath: 'bo', // API路径
  permissionPrefix: 'medical:bo', // 权限前缀
  
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
      prop: 'measurement_type',
      label: '测量类型',
      type: 'select',
      props: {
        options: [
          { value: "single", label: "单次测量" },
          { value: "continuous", label: "连续测量" },
          { value: "daily", label: "每日统计" }
        ],
        placeholder: '请选择测量类型'
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
  
  // 表格列配置
  tableColumns: [
    {
      prop: 'user_id',
      label: '用户ID',
      width: 120
    },
    {
      prop: 'spo2_value',
      label: '血氧饱和度',
      width: 120,
      formatter: (row) => `${row.spo2_value}%`
    },
    {
      prop: 'measurement_type',
      label: '测量类型',
      width: 120,
      type: 'dict',
      dictOptions: [
        { value: "single", label: "单次测量" },
        { value: "continuous", label: "连续测量" },
        { value: "daily", label: "每日统计" }
      ]
    },
    {
      prop: 'data_time',
      label: '数据时间',
      width: 180,
      type: 'time'
    },
    {
      prop: 'upload_time',
      label: '上传时间',
      width: 180,
      type: 'time'
    },
    {
      prop: 'user_notes',
      label: '备注',
      width: 150,
      formatter: (row) => row.user_notes || '-'
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
        disabled: (config) => config.title.includes('详情')
      }
    },
    {
      prop: 'measurementType',
      label: '测量类型',
      type: 'select',
      span: 12,
      props: {
        options: [
          { value: "single", label: "单次测量" },
          { value: "continuous", label: "连续测量" },
          { value: "daily", label: "每日统计" }
        ],
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
    },
    {
      prop: 'userNotes',
      label: '用户备注',
      type: 'textarea',
      span: 24,
      props: {
        rows: 2,
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
      { required: true, message: '血氧饱和度不能为空', trigger: 'blur' }
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
      spo2_value: data.spo2Value,
      measurement_type: data.measurementType,
      data_time: data.dataTime,
      upload_time: data.uploadTime,
      user_notes: data.userNotes
    }
  },
  
  transformResponse: (data) => {
    // 转换字段命名风格为camelCase
    return {
      id: data.id,
      userId: data.user_id,
      spo2Value: data.spo2_value,
      measurementType: data.measurement_type,
      dataTime: data.data_time,
      uploadTime: data.upload_time,
      userNotes: data.user_notes
    }
  }
}