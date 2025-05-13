<template>
    <BaseTablePage :config="config" @load="handleLoad" @error="handleError" ref="tablePage" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { continuousBloodOxygenConfig } from '@/config/tableConfigs/continuousBloodOxygen'

export default {
    name: 'ContinuousBloodOxygen',
    components: {
        BaseTablePage
    },
    data() {
        return {
            config: continuousBloodOxygenConfig
        }
    },
    methods: {
        handleLoad(response) {
            console.group('[连续血氧] 数据加载完成')
            console.log('API响应:', response)
            console.log('表格数据:', this.$refs.tablePage.tableData)
            console.log('分页信息:', {
                page: this.$refs.tablePage.queryParams.page_num,
                size: this.$refs.tablePage.queryParams.page_size,
                total: this.$refs.tablePage.total
            })
            console.groupEnd()
        },
        handleError(error) {
            console.error('[连续血氧] 加载错误:', error)
        }
    },
    mounted() {
        console.log('[连续血氧] 组件挂载完成')
    }
}
</script>