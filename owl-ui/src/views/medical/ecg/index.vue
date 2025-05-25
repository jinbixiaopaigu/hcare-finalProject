<template>
    <div>
        <BaseTablePage ref="baseTable" :config="config" @table-mounted="onTableMounted" @form-mounted="onFormMounted" />
    </div>
</template>

<script>
import * as ecgApi from '@/api/medical/ecg'
import BaseTablePage from '@/components/BaseTablePage'
import { ecgConfig } from '@/config/tableConfigs/ecg'

export default {
    name: 'ECGData',
    components: {
        BaseTablePage
    },
    data() {
        return {
            config: {
                ...ecgConfig,
                toolbarButtons: ecgConfig.toolbarButtons || [],
                buttons: ecgConfig.toolbarButtons || [],
                methods: {
                    syncData: this.handleSyncData
                }
            }
        }
    },
    methods: {
        onTableMounted() {
            // 表格加载完成后的回调
            console.log('ECG表格加载完成')
        },
        onFormMounted() {
            // 表单加载完成后的回调
            console.log('ECG表单加载完成')
        },
        handleSyncData() {
            this.$modal.confirm('是否确认同步ECG数据？').then(() => {
                ecgApi.sync().then(response => {
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

<style scoped></style>