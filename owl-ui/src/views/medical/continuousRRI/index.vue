<template>
    <BaseTablePage ref="baseTable" :config="config" @tableMounted="onTableMounted" @formMounted="onFormMounted" />
</template>

<script>
import * as crriApi from '@/api/medical/crri'
import BaseTablePage from '@/components/BaseTablePage'

export default {
    name: 'ContinuousRRI',
    components: {
        BaseTablePage
    },
    data() {
        return {
            config: {
                title: '连续RRI数据',
                apiModule: 'medical',
                apiPath: 'crri',
                permissionPrefix: 'medical:continuousRRI',
                searchFields: [
                    {
                        label: '用户ID',
                        prop: 'userId',
                        type: 'input'
                    },
                    {
                        label: '数据时间',
                        prop: 'dataTimeRange',
                        type: 'daterange'
                    }
                ],
                columns: [
                    {
                        label: '用户ID',
                        prop: 'userId',
                        width: 180
                    },
                    {
                        label: '数据时间',
                        prop: 'dataTime',
                        width: 180
                    },
                    {
                        label: '上传时间',
                        prop: 'uploadTime',
                        width: 180
                    },
                    {
                        label: 'RRI数据',
                        prop: 'rriData',
                        width: 180,
                        formatter: (row) => {
                            if (typeof row.rriData === 'object') {
                                return JSON.stringify(row.rriData)
                            }
                            return row.rriData
                        }
                    },
                    {
                        label: '外部ID',
                        prop: 'externalId',
                        width: 180
                    },
                    {
                        label: '元数据版本',
                        prop: 'metadataVersion',
                        width: 100
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
                        label: 'RRI数据',
                        prop: 'rriData',
                        type: 'textarea',
                        rules: [{ required: true, message: '请输入RRI数据', trigger: 'blur' }]
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
                buttons: [
                    {
                        label: '同步数据',
                        type: 'primary',
                        icon: 'el-icon-refresh',
                        onClick: 'handleSyncData',
                        permission: 'medical:continuousRRI:sync'
                    }
                ]
            }
        }
    },
    methods: {
        onTableMounted() {
            // 表格加载完成后的回调
            console.log('表格加载完成')
        },
        onFormMounted() {
            // 表单加载完成后的回调
            console.log('表单加载完成')
        },
        handleSyncData() {
            this.$modal.confirm('是否确认同步连续RRI数据？').then(() => {
                crriApi.syncContinuousRRI().then(response => {
                    this.$modal.msgSuccess('同步成功')
                    this.$refs.baseTable.getList()
                }).catch(error => {
                    console.error('同步失败:', error)
                    this.$modal.msgError('同步失败：' + (error.message || '未知错误'))
                })
            })
        }
    }
}
</script>