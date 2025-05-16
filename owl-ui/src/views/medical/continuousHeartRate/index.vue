<template>
    <BaseTablePage ref="baseTable" :config="config" @table-mounted="onTableMounted" @form-mounted="onFormMounted"
        @sync-data="handleSyncData" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { continuousHeartRateConfig } from '@/config/tableConfigs/continuousHeartRate'
import { sync } from '@/api/medical/chr'
import { ElMessage } from 'element-plus'

export default {
    name: 'ContinuousHeartRate',
    components: { BaseTablePage },
    data() {
        return {
            config: {
                ...continuousHeartRateConfig,
                methods: {
                    syncData: this.handleSyncData
                }
            },
            syncLoading: false
        }
    },
    methods: {
        onTableMounted(tableRef) {
            console.log('[ContinuousHeartRate] Table mounted:', tableRef)
            console.log('ContinuousHeartRate table initialized')
        },
        onFormMounted(formRef) {
            console.log('[ContinuousHeartRate] Form mounted:', formRef)
            console.log('ContinuousHeartRate form initialized')
        },
        // 处理同步数据
        async handleSyncData() {
            try {
                this.syncLoading = true
                const res = await sync()
                const { inserted, updated } = res.data || {}
                ElMessage.success(`同步完成！新增${inserted || 0}条记录，更新${updated || 0}条记录`)

                // 使用 baseTable ref 刷新数据表格
                this.$refs.baseTable.getList()
            } catch (error) {
                console.error('同步心率数据失败:', error)
                ElMessage.error('同步数据失败：' + (error.message || '未知错误'))
            } finally {
                this.syncLoading = false
            }
        }
    },
    created() {
        console.log('ContinuousHeartRate page created')
    },
    mounted() {
        console.log('ContinuousHeartRate page mounted')
    }
}
</script>

<style scoped>
/* 自定义样式可以放在这里 */
</style> 