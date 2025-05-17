export const singleWorkoutDetailConfig = {
  title: '6分钟行走测试数据',
  primaryKey: 'id',
  columns: [
    { prop: 'user_id', label: '用户ID', width: 280 },
    { prop: 'data_time', label: '测量时间', width: 180, sortable: true },
    { prop: 'step_count', label: '步数', width: 100 },
    { prop: 'distance', label: '距离(m)', width: 100 },
    { prop: 'heart_rate', label: '心率(bpm)', width: 100 },
    { prop: 'speed', label: '速度(m/s)', width: 100 },
    { prop: 'speed_unit', label: '速度单位', width: 100 },
    { prop: 'calories', label: '卡路里(kcal)', width: 100 },
    { prop: 'upload_time', label: '上传时间', width: 180, sortable: true }
  ],
  searchItems: [
    { label: '用户ID', prop: 'user_id' },
    { label: '运动类型', prop: 'workout_type' },
    { 
      label: '测量时间', 
      prop: 'data_time_range', 
      type: 'daterange', 
      startProp: 'begin_data_time',
      endProp: 'end_data_time'
    }
  ],
  formItems: [
    { label: '用户ID', prop: 'userId', required: true },
    { label: '测量时间', prop: 'dataTime', type: 'datetime', required: true },
    { label: '步数', prop: 'stepCount', type: 'number' },
    { label: '距离', prop: 'distance', type: 'number' },
    { label: '距离单位', prop: 'distanceUnit', default: 'm' },
    { label: '心率', prop: 'heartRate', type: 'number' },
    { label: '速度', prop: 'speed', type: 'number' },
    { label: '速度单位', prop: 'speedUnit', default: 'm/s' },
    { label: '步频', prop: 'stepFrequency', type: 'number' },
    { label: '卡路里', prop: 'calories', type: 'number' },
    { label: '运动类型', prop: 'workoutType' },
    { label: '运动状态', prop: 'workoutStatus' },
    { label: '备注', prop: 'userNotes', type: 'textarea' }
  ],
  hasToolbar: true,
  hasDateFilter: true,
  hasAdd: true,
  hasEdit: true,
  hasDelete: true,
  hasSync: true
} 