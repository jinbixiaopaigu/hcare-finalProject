<template>
    <div class="app-container">
        <el-card shadow="never">
            <div class="filter-container">
                <el-form :inline="true" :model="queryParams" class="demo-form-inline">
                    <el-form-item label="用户ID">
                        <el-input v-model="queryParams.user_id" placeholder="用户ID" clearable />
                    </el-form-item>
                    <el-form-item label="时间范围">
                        <el-date-picker v-model="dateRange" type="daterange" range-separator="至"
                            start-placeholder="开始日期" end-placeholder="结束日期" value-format="YYYY-MM-DD"
                            @change="handleDateChange" />
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleQuery">查询</el-button>
                        <el-button @click="resetQuery">重置</el-button>
                        <el-button type="success" @click="handleSync" :loading="syncing">同步数据</el-button>
                    </el-form-item>
                </el-form>
            </div>

            <el-table v-loading="loading" :data="list" border fit highlight-current-row style="width: 100%">
                <el-table-column label="ID" prop="id" width="180" />
                <el-table-column label="用户ID" prop="user_id" width="180" />
                <el-table-column label="检测结果" prop="af_result" />
                <el-table-column label="风险等级" prop="risk_level" />
                <el-table-column label="上传时间" prop="upload_time" width="180">
                    <template #default="{ row }">
                        {{ parseTime(row.upload_time) }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button type="text" size="small" @click="handleDetail(row)">详情</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination v-show="total > 0" :total="Number(total)" v-model:current-page="queryParams.pageNum"
                v-model:page-size="queryParams.pageSize" @current-change="getList" @size-change="getList"
                layout="total, sizes, prev, pager, next, jumper" :page-sizes="[10, 20, 50, 100]" />
        </el-card>

        <!-- 详情对话框 -->
        <el-dialog title="房颤检测详情" v-model="detailVisible" width="50%">
            <el-descriptions :column="1" border>
                <el-descriptions-item label="ID">{{ currentRow.id }}</el-descriptions-item>
                <el-descriptions-item label="用户ID">{{ currentRow.user_id }}</el-descriptions-item>
                <el-descriptions-item label="分组ID">{{ currentRow.group_id }}</el-descriptions-item>
                <el-descriptions-item label="上传时间">{{ parseTime(currentRow.upload_time) }}</el-descriptions-item>
                <el-descriptions-item label="数据时间">{{ parseTime(currentRow.data_time) }}</el-descriptions-item>
                <el-descriptions-item label="检测结果">{{ currentRow.af_result }}</el-descriptions-item>
                <el-descriptions-item label="风险等级">{{ currentRow.risk_level }}</el-descriptions-item>
                <el-descriptions-item label="外部ID">{{ currentRow.external_id }}</el-descriptions-item>
                <el-descriptions-item label="元数据版本">{{ currentRow.metadata_version }}</el-descriptions-item>
            </el-descriptions>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineOptions } from 'vue'
import { getAtrialFibrillationList, syncAtrialFibrillation } from '@/api/medical/atrialFibrillation'
import { parseTime } from '@/utils/ruoyi'
import Pagination from '@/components/Pagination'
import { ElMessage } from 'element-plus'

// 定义组件名
defineOptions({
    name: 'AtrialFibrillation',
    title: '房颤检测结果'
})

// 定义页面标题，用于标签页显示
const pageTitle = '房颤检测结果'

const loading = ref(false)
const syncing = ref(false)
const list = ref([])
const total = ref(0)
const detailVisible = ref(false)
const currentRow = ref({})
const dateRange = ref([])

const queryParams = reactive({
    pageNum: 1,
    pageSize: 10,
    user_id: undefined,
    start_time: undefined,
    end_time: undefined
})

// 获取列表数据
function getList() {
    loading.value = true
    getAtrialFibrillationList(queryParams).then(response => {
        console.log('API完整响应:', response) // 调试日志
        // 兼容不同响应结构
        const data = response.data || response
        console.log('处理后数据:', data) // 调试日志

        list.value = data.rows || []
        total.value = Number(data.total || 0)

        if (list.value.length === 0) {
            console.warn('数据为空，请检查响应结构') // 警告日志
        }
    }).catch(error => {
        console.error('请求出错:', error) // 错误日志
    }).finally(() => {
        loading.value = false
    })
}

// 处理查询
function handleQuery() {
    queryParams.pageNum = 1
    getList()
}

// 重置查询
function resetQuery() {
    dateRange.value = []
    queryParams.user_id = undefined
    queryParams.start_time = undefined
    queryParams.end_time = undefined
    handleQuery()
}

// 处理日期变化
function handleDateChange(val) {
    if (val && val.length === 2) {
        queryParams.start_time = val[0]
        queryParams.end_time = val[1]
    } else {
        queryParams.start_time = undefined
        queryParams.end_time = undefined
    }
}

// 查看详情
function handleDetail(row) {
    currentRow.value = row
    detailVisible.value = true
}

// 同步数据
async function handleSync() {
    try {
        syncing.value = true
        const response = await syncAtrialFibrillation()

        if (response.code === 200) {
            ElMessage.success('数据同步成功')
            // 刷新列表
            getList()
        } else {
            ElMessage.error(response.msg || '数据同步失败')
        }
    } catch (error) {
        console.error('同步出错:', error)
        ElMessage.error('数据同步失败')
    } finally {
        syncing.value = false
    }
}

onMounted(() => {
    getList()
})
</script>

<style scoped>
.filter-container {
    margin-bottom: 20px;
}
</style>