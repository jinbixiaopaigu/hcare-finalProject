import { getDictOptions } from '@/utils/dict'

export const continuousHeartRateConfig = {
  title: '连续心率数据',
  apiModule: 'medical',
  apiPath: 'chr',
  permissionPrefix: 'medical:continuousHeartRate',
  
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
      loading: 'syncLoading'
    }
  ],
  
  tableColumns: [
    {
      prop: 'userId',
      label: '用户ID',
      width: 120
    },
    {
      prop: 'heartRateValue',
      label: '心率(次/分)',
      width: 120
    },
    {
      prop: 'heartRateUnit',
      label: '单位',
      width: 80
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
      prop: 'heartRateValue',
      label: '心率(次/分)',
      type: 'input',
      span: 12,
      props: {
        type: 'number',
        step: 1
      }
    },
    {
      prop: 'heartRateUnit',
      label: '单位',
      type: 'input',
      span: 12,
      props: {
        disabled: true
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
    heartRateValue: [
      { required: true, message: '心率不能为空' },
      { type: 'number', message: '心率必须为数字值' }
    ],
    dataTime: [
      { required: true, message: '数据时间不能为空' }
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
  },

  // 添加方法对象
  methods: {
    syncData(component) {
      component.syncLoading = true;
      component.$api.medical.chr.sync()
        .then(response => {
          const { inserted, updated } = response.data || {};
          component.$modal.msgSuccess(`同步完成！新增${inserted || 0}条记录，更新${updated || 0}条记录`);
          // 刷新数据表格
          if (component.tableRef && component.tableRef.getList) {
            component.tableRef.getList();
          } else {
            component.getList();
          }
        })
        .catch(error => {
          console.error('同步心率数据失败:', error);
          component.$modal.msgError('同步数据失败：' + (error.message || '未知错误'));
        })
        .finally(() => {
          component.syncLoading = false;
        });
    }
  }
} 