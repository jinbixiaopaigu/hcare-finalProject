export const continuousRRIConfig = {
  title: '连续RRI数据',
  apiModule: 'medical',
  apiPath: 'crri',
  permissionPrefix: 'medical:continuousRRI',
  
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
      prop: 'dataTimeRange',
      label: '数据时间范围',
      type: 'daterange',
      props: {
        'value-format': 'YYYY-MM-DD',
        'start-placeholder': '开始日期',
        'end-placeholder': '结束日期',
        'range-separator': '至',
        'clearable': true,
        'type': 'daterange'
      }
    }
  ],
  
  tableColumns: [
    {
      prop: 'userId',
      label: '用户ID',
      width: 180
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
    },
    {
      label: '操作',
      width: 160,
      buttons: [
        {
          label: '查看图表',
          type: 'text',
          size: 'mini',
          icon: 'el-icon-view',
          onClick: 'viewRRIChart'
        }
      ]
    }
  ],
  
  formFields: [
    {
      label: '用户ID',
      prop: 'userId',
      type: 'input',
      rules: [{ required: true, message: '请输入用户ID', trigger: 'blur' }]
    },
    {
      label: '数据时间',
      prop: 'dataTime',
      type: 'datetime',
      rules: [{ required: true, message: '请选择数据时间', trigger: 'change' }]
    },
    {
      label: '记录分组ID',
      prop: 'recordGroupId',
      type: 'input'
    },
    {
      label: '上传时间',
      prop: 'uploadTime',
      type: 'datetime'
    },
    {
      label: '外部ID',
      prop: 'externalId',
      type: 'input'
    },
    {
      label: '元数据版本',
      prop: 'metadataVersion',
      type: 'number'
    }
  ],
  
  // 添加验证规则
  rules: {
    userId: [
      { required: true, message: '请输入用户ID', trigger: 'blur' }
    ],
    dataTime: [
      { required: true, message: '请选择数据时间', trigger: 'change' }
    ]
  },
  
  // 同时使用两种属性名称，确保兼容性
  toolbarButtons: [
    {
      label: '同步数据',
      type: 'primary',
      icon: 'el-icon-refresh',
      onClick: 'syncData',
      permission: 'sync'
    }
  ],
  
  // 保留buttons属性以确保兼容性
  buttons: [
    {
      label: '同步数据',
      type: 'primary',
      icon: 'el-icon-refresh',
      onClick: 'syncData',
      permission: 'sync'
    }
  ]
} 