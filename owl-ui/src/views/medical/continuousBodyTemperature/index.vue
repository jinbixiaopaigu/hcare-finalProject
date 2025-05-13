<template>
    <BaseTablePage :config="config" @table-mounted="onTableMounted" @form-mounted="onFormMounted" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { continuousBodyTemperatureConfig } from '@/config/tableConfigs/continuousBodyTemperature'

export default {
    name: 'ContinuousBodyTemperature',
    components: { BaseTablePage },
    data() {
        return {
            config: continuousBodyTemperatureConfig
        }
    },
    methods: {
        onTableMounted(tableRef) {
            console.log('[ContinuousBodyTemperature] Table mounted:', tableRef)
            console.log('ContinuousBodyTemperature table initialized')
        },
        onFormMounted(formRef) {
            console.log('[ContinuousBodyTemperature] Form mounted:', formRef)
            console.log('ContinuousBodyTemperature form initialized')
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