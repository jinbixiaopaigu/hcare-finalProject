<template>
    <div class="app-container">
        <!-- 搜索表单 -->
        <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch">
            <el-form-item label="用户ID" prop="user_id">
                <el-input v-model="queryParams.user_id" placeholder="请输入用户ID" clearable style="width: 200px" />
            </el-form-item>
            <el-form-item label="测量类型" prop="measurement_type">
                <el-select v-model="queryParams.measurement_type" placeholder="请选择测量类型" clearable style="width: 200px">
                    <el-option value="continuous" label="连续测量" />
                    <el-option value="daily" label="每日统计" />
                </el-select>
            </el-form-item>
            <el-form-item label="时间范围" prop="dateRange">
                <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期"
                    end-placeholder="结束日期" value-format="YYYY-MM-DD" style="width: 240px"
                    @change="handleDateRangeChange" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
                <el-button icon="Refresh" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>

        <!-- 操作工具栏 -->
        <el-row :gutter="10" class="mb8">
            <el-col :span="1.5">
                <el-button type="primary" plain icon="Plus" @click="handleAdd">新增</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button type="success" plain icon="Refresh" :loading="syncLoading" @click="handleSync">同步</el-button>
            </el-col>
            <right-toolbar v-model:show-search="showSearch" @query-table="getList"></right-toolbar>
        </el-row>

        <!-- 数据表格 -->
        <el-table v-loading="loading" :data="dataList">
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column label="用户ID" align="center" prop="user_id" />
            <el-table-column label="血氧值" align="center" prop="spo2_avg_value">
                <template #default="{ row }">
                    {{ (row.spo2_avg_value || '-') + (row.spo2_avg_unit || '%') }}
                </template>
            </el-table-column>
            <el-table-column label="数据时间" align="center" prop="data_time" width="180">
                <template #default="{ row }">
                    {{ parseTime(row.data_time) }}
                </template>
            </el-table-column>
            <el-table-column label="上传时间" align="center" prop="upload_time" width="180">
                <template #default="{ row }">
                    {{ parseTime(row.upload_time) }}
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                <template #default="{ row }">
                    <el-button type="text" icon="View" @click="handleDetail(row)">详情</el-button>
                    <el-button type="text" icon="Edit" @click="handleUpdate(row)">修改</el-button>
                    <el-button type="text" icon="Delete" @click="handleDelete(row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页 -->
        <pagination v-show="total > 0" :total="total" v-model:page="queryParams.page_num"
            v-model:limit="queryParams.page_size" @pagination="getList" />

        <!-- 详情/编辑对话框 -->
        <el-dialog :title="title" v-model="open" width="700px" append-to-body>
            <el-form ref="form" :model="form" :rules="rules" label-width="120px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="ID" prop="id">
                            <el-input v-model="form.id" disabled />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="用户ID" prop="userId">
                            <el-input v-model="form.userId" :disabled="title.includes('详情')" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="血氧值" prop="spo2AvgValue">
                            <el-input v-model="form.spo2AvgValue" :disabled="title.includes('详情')">
                                <template #append>%</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="数据时间" prop="dataTime">
                            <el-date-picker v-model="form.dataTime" type="datetime" placeholder="选择日期时间"
                                format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%"
                                :disabled="title.includes('详情')" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="上传时间" prop="uploadTime">
                            <el-date-picker v-model="form.uploadTime" type="datetime" placeholder="选择日期时间"
                                format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%"
                                disabled />
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="cancel">取 消</el-button>
                    <el-button type="primary" @click="submitForm" v-if="!title.includes('详情')">确 定</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { listCbo, getCbo, delCbo, addCbo, updateCbo, syncCbo } from "@/api/medical/cbo";
import { parseTime } from "@/utils/ruoyi";

export default {
    name: "ContinuousBloodOxygen",
    data() {
        return {
            // 遮罩层
            loading: false,
            // 同步按钮loading
            syncLoading: false,
            // 选中数组
            ids: [],
            // 非单个禁用
            single: true,
            // 非多个禁用
            multiple: true,
            // 显示搜索条件
            showSearch: true,
            // 总条数
            total: 0,
            // 连续血氧数据表格数据
            dataList: [],
            // 弹出层标题
            title: "",
            // 是否显示弹出层
            open: false,
            // 日期范围
            dateRange: [],
            // 查询参数
            queryParams: {
                page_num: 1,
                page_size: 10,
                user_id: undefined,
                measurement_type: undefined,
                begin_data_time: undefined,
                end_data_time: undefined
            },
            // 表单参数
            form: {},
            // 表单校验
            rules: {
                userId: [
                    { required: true, message: "用户ID不能为空", trigger: "blur" }
                ],
                measurementType: [
                    { required: true, message: "测量类型不能为空", trigger: "change" }
                ]
            }
        };
    },
    created() {
        this.getList();
    },
    methods: {
        /** 查询连续血氧数据列表 */
        getList() {
            this.loading = true;
            listCbo(this.queryParams).then(response => {
                console.log('[连续血氧] 获取到的原始响应:', response);

                // 检查response格式，从response.data中获取数据
                const responseData = response.data || {};
                const rows = responseData.rows || [];
                const total = responseData.total || 0;

                // 确保赋值给组件数据
                this.total = parseInt(total) || 0;

                // 处理数据
                if (rows && rows.length > 0) {
                    // 将驼峰命名的字段映射为下划线命名
                    this.dataList = rows.map(item => ({
                        id: item.id,
                        user_id: item.userId || item.user_id,
                        spo2_avg_value: item.spo2AvgValue || item.spo2_avg_value,
                        spo2_avg_unit: item.spo2AvgUnit || item.spo2_avg_unit || '%',
                        data_time: item.dataTime || item.data_time,
                        upload_time: item.uploadTime || item.upload_time
                    }));
                } else {
                    this.dataList = [];
                }

                this.loading = false;
                console.log('[连续血氧] 获取数据成功，共', this.total, '条记录，当前页', this.dataList.length, '条');
            }).catch(error => {
                console.error('[连续血氧] 获取数据失败', error);
                this.dataList = [];
                this.total = 0;
                this.loading = false;
            });
        },
        // 日期范围处理
        handleDateRangeChange(dates) {
            if (dates) {
                this.queryParams.begin_data_time = dates[0] + ' 00:00:00';
                this.queryParams.end_data_time = dates[1] + ' 23:59:59';
            } else {
                this.queryParams.begin_data_time = undefined;
                this.queryParams.end_data_time = undefined;
            }
        },
        // 同步按钮操作
        handleSync() {
            this.$modal.confirm('确认要从华为Research同步连续血氧数据吗？').then(() => {
                this.syncLoading = true;
                syncCbo().then(response => {
                    console.log('[连续血氧] 同步响应:', response);
                    const syncData = response.data || {};
                    const inserted = syncData.inserted || 0;
                    const updated = syncData.updated || 0;

                    this.$modal.msgSuccess(`同步成功，新增 ${inserted} 条，更新 ${updated} 条数据`);
                    this.getList(); // 刷新列表
                    this.syncLoading = false;
                }).catch(error => {
                    this.syncLoading = false;
                    console.error('[连续血氧] 同步失败', error);
                    this.$modal.msgError('同步失败：' + (error.message || '未知错误'));
                });
            }).catch(() => { });
        },
        /** 搜索按钮操作 */
        handleQuery() {
            this.queryParams.page_num = 1;
            this.getList();
        },
        /** 重置按钮操作 */
        resetQuery() {
            this.dateRange = [];
            this.resetForm("queryForm");
            this.handleQuery();
        },
        /** 新增按钮操作 */
        handleAdd() {
            this.reset();
            this.open = true;
            this.title = "添加连续血氧数据";
        },
        /** 详情按钮操作 */
        handleDetail(row) {
            this.reset();
            getCbo(row.id).then(response => {
                this.form = this.convertToForm(response.data);
                this.open = true;
                this.title = "连续血氧数据详情";
            });
        },
        /** 修改按钮操作 */
        handleUpdate(row) {
            this.reset();
            getCbo(row.id).then(response => {
                this.form = this.convertToForm(response.data);
                this.open = true;
                this.title = "修改连续血氧数据";
            });
        },
        /** 提交按钮 */
        submitForm() {
            this.$refs["form"].validate(valid => {
                if (valid) {
                    // 转换为snake_case格式
                    const data = {
                        id: this.form.id,
                        user_id: this.form.userId,
                        spo2_avg_value: this.form.spo2AvgValue,
                        data_time: this.form.dataTime,
                        upload_time: this.form.uploadTime
                    };

                    if (this.form.id) {
                        updateCbo(data).then(response => {
                            this.$modal.msgSuccess("修改成功");
                            this.open = false;
                            this.getList();
                        });
                    } else {
                        addCbo(data).then(response => {
                            this.$modal.msgSuccess("新增成功");
                            this.open = false;
                            this.getList();
                        });
                    }
                }
            });
        },
        /** 删除按钮操作 */
        handleDelete(row) {
            const ids = row.id || this.ids;
            this.$modal.confirm('是否确认删除连续血氧数据编号为"' + ids + '"的数据项?').then(() => {
                return delCbo(ids);
            }).then(() => {
                this.getList();
                this.$modal.msgSuccess("删除成功");
            }).catch(() => { });
        },
        /** 表单重置 */
        reset() {
            this.form = {
                id: undefined,
                userId: undefined,
                spo2Value: undefined,
                spo2AvgValue: undefined,
                spo2MinValue: undefined,
                spo2MaxValue: undefined,
                measurementType: undefined,
                dataTime: undefined,
                uploadTime: undefined,
                userNotes: undefined
            };
            this.resetForm("form");
        },
        /** 取消按钮 */
        cancel() {
            this.open = false;
            this.reset();
        },
        // 将Snake格式转为Camel格式
        convertToForm(data) {
            return {
                id: data.id,
                userId: data.user_id,
                spo2AvgValue: data.spo2_avg_value,
                spo2AvgUnit: data.spo2_avg_unit || '%',
                dataTime: data.data_time,
                uploadTime: data.upload_time
            };
        },
        // 同步数据方法 - 用于支持BaseTablePage配置
        syncData() {
            this.handleSync();
        },
        // 工具函数
        parseTime
    }
};
</script>