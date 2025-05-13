import { getDictOptions } from '@/utils/dict'

export const continuousBodyTemperatureConfig = {
  title: '持续体温数据',
  apiModule: 'medical',
  apiPath: 'cbt',
  permissionPrefix: 'medical:continuousBodyTemperature',
  
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
      prop: 'measurementPart',
      label: '测量部位',
      type: 'select',
      props: {
        options: [],
        placeholder: '请选择测量部位'
      },
      async created() {
        this.props.options = await getDictOptions('measurement_part') || []
      }
    },
    {
      prop: 'dataTime',
      label: '数据时间范围',
      type: 'daterange',
      props: {
        'value-format': 'yyyy-MM-dd',
        'start-placeholder': '开始日期',
        'end-placeholder': '结束日期'
      }
    }
  ],
  
  tableColumns: [
    {
      prop: 'userId',
      label: '用户ID',
      width: 120
    },
    {
      prop: 'measurementPart',
      label: '测量部位',
      width: 120
    },
    {
      prop: 'bodyTemperature',
      label: '体温(℃)',
      width: 100
    },
    {
      prop: 'skinTemperature',
      label: '皮肤温度(℃)',
      width: 120
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
  
  formFields: [
    {
      prop: 'userId',
      label: '用户ID',
      type: 'input',
      span: 12,
      props: {
        disabled: true
      }
    },
    {
      prop: 'measurementPart',
      label: '测量部位',
      type: 'select',
      span: 12,
      props: {
        options: getDictOptions('measurement_part')
      }
    },
    {
      prop: 'bodyTemperature',
      label: '体温(℃)',
      type: 'input',
      span: 12,
      props: {
        type: 'number',
        step: 0.1
      }
    },
    {
      prop: 'skinTemperature',
      label: '皮肤温度(℃)',
      type: 'input',
      span: 12,
      props: {
        type: 'number',
        step: 0.1
      }
    },
    {
      prop: 'dataTime',
      label: '数据时间',
      type: 'datetime',
      span: 12
    }
  ],
  
  rules: {
    userId: [
      { required: true, message: '用户ID不能为空' }
    ],
    measurementPart: [
      { required: true, message: '请选择测量部位' }
    ],
    bodyTemperature: [
      { required: true, message: '体温不能为空' },
      { type: 'number', message: '体温必须为数字值' }
    ]
  },

  // 数据转换方法
  transformRequest: (data) => {
    return {
      ...data
    }
  },

  transformResponse: (data) => {
    return {
      ...data
    }
  }
}