<template>
    <BaseTablePage :config="config" @table-mounted="onTableMounted" @form-mounted="onFormMounted"
        @sync-data="handleSyncData" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { continuousBodyTemperatureConfig } from '@/config/tableConfigs/continuousBodyTemperature'
import { syncCbt } from '@/api/medical/cbt'
import { ElMessage } from 'element-plus'

export default {
    name: 'ContinuousBodyTemperature',
    components: { BaseTablePage },
    data() {
        return {
            config: {
                ...continuousBodyTemperatureConfig,
                methods: {
                    syncData: this.handleSyncData
                }
            },
            syncLoading: false
        }
    },
    methods: {
        onTableMounted(tableRef) {
            console.log('[ContinuousBodyTemperature] Table mounted:', tableRef)
            this.tableRef = tableRef
            console.log('ContinuousBodyTemperature table initialized')
        },
        onFormMounted(formRef) {
            console.log('[ContinuousBodyTemperature] Form mounted:', formRef)
            console.log('ContinuousBodyTemperature form initialized')
        },
        // 处理同步数据
        async handleSyncData() {
            try {
                this.syncLoading = true
                const res = await syncCbt()
                const { inserted, updated } = res.data || {}
                ElMessage.success(`同步完成！新增${inserted || 0}条记录，更新${updated || 0}条记录`)

                // 刷新数据表格
                if (this.tableRef && this.tableRef.getList) {
                    this.tableRef.getList()
                }
            } catch (error) {
                console.error('同步体温数据失败:', error)
                ElMessage.error('同步数据失败：' + (error.message || '未知错误'))
            } finally {
                this.syncLoading = false
            }
        }
    },
    created() {
        console.log('ContinuousBodyTemperature page created')
    },
    mounted() {
        console.log('ContinuousBodyTemperature page mounted')
    }
}
</script>

<style scoped>
/* 自定义样式可以放在这里 */
</style>