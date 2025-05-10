<template>
    <div class="app-container">
        <!-- 查询表单 -->
        <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch">
            <el-form-item label="用户ID" prop="userId">
                <el-input v-model="queryParams.userId" placeholder="请输入用户ID" clearable size="small"
                    @keyup.enter.native="handleQuery" />
            </el-form-item>
            <el-form-item label="测量类型" prop="measurementType">
                <el-select v-model="queryParams.measurementType" placeholder="请选择测量类型" clearable size="small">
                    <el-option v-for="dict in measurementTypeOptions" :key="dict.value" :label="dict.label"
                        :value="dict.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="数据时间" prop="dataTimeRange">
                <el-date-picker v-model="dataTimeRange" type="daterange" range-separator="至" start-placeholder="开始日期"
                    end-placeholder="结束日期" value-format="yyyy-MM-dd" size="small"></el-date-picker>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="el-icon-search" size="small" @click="handleQuery">搜索</el-button>
                <el-button icon="el-icon-refresh" size="small" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>

        <!-- 操作按钮 -->
        <el-row :gutter="10" class="mb8">
            <el-col :span="1.5">
                <el-button type="primary" plain icon="el-icon-plus" size="small" @click="handleAdd"
                    v-hasPermi="['medical:bo:add']">新增</el-button>
            </el-col>
            <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
        </el-row>

        <!-- 数据表格 -->
        <el-table v-loading="loading" :data="boList" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column label="ID" align="center" prop="id" width="120" />
            <el-table-column label="用户ID" align="center" prop="user_id" width="120" />
            <el-table-column label="血氧饱和度" align="center" prop="spo2_value" width="120">
                <template #default="{ row }">
                    {{ row.spo2_value }}%
                </template>
            </el-table-column>
            <el-table-column label="测量类型" align="center" prop="measurement_type" width="120">
                <template #default="{ row }">
                    <dict-tag :options="measurementTypeOptions" :value="row.measurement_type" />
                </template>
            </el-table-column>
            <el-table-column label="数据时间" align="center" prop="data_time" width="180">
                <template #default="{ row }">
                    <span>{{ parseTime(row.data_time) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="上传时间" align="center" prop="upload_time" width="180">
                <template #default="{ row }">
                    <span>{{ parseTime(row.upload_time) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                <template #default="{ row }">
                    <el-button size="mini" type="text" icon="el-icon-view" @click="handleDetail(row)"
                        v-hasPermi="['medical:bo:query']">详情</el-button>
                    <el-button size="mini" type="text" icon="el-icon-edit" @click="handleUpdate(row)"
                        v-hasPermi="['medical:bo:edit']">修改</el-button>
                    <el-button size="mini" type="text" icon="el-icon-delete" @click="handleDelete(row)"
                        v-hasPermi="['medical:bo:remove']">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页组件 -->
        <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum"
            v-model:limit="queryParams.pageSize" @pagination="getList" />

        <!-- 详情对话框 -->
        <el-dialog ref="dialog" :title="title" v-model="open" width="700px" append-to-body
            @open="console.log('对话框打开事件触发')" @opened="console.log('对话框打开动画完成')" @close="console.log('对话框关闭事件触发')">
            <el-form ref="form" :model="form" :rules="rules" label-width="120px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="数据ID" prop="id">
                            <el-input v-model="form.id" :disabled="true" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="用户ID" prop="userId">
                            <el-input v-model="form.userId" :disabled="title === '血氧数据详情'" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="血氧饱和度" prop="spo2Value">
                            <el-input v-model="form.spo2Value" :disabled="title === '血氧数据详情'">
                                <template #append>%</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="测量类型" prop="measurementType">
                            <el-select v-model="form.measurementType" :disabled="title === '血氧数据详情'">
                                <el-option v-for="dict in measurementTypeOptions" :key="dict.value" :label="dict.label"
                                    :value="dict.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="数据时间" prop="dataTime">
                            <el-date-picker v-model="form.dataTime" type="datetime" placeholder="选择日期时间"
                                :disabled="title === '血氧数据详情'" value-format="yyyy-MM-dd HH:mm:ss" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="上传时间" prop="uploadTime">
                            <el-date-picker v-model="form.uploadTime" type="datetime" placeholder="选择日期时间"
                                :disabled="title === '血氧数据详情'" value-format="yyyy-MM-dd HH:mm:ss" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="用户备注" prop="userNotes">
                            <el-input v-model="form.userNotes" type="textarea" :disabled="title === '血氧数据详情'" :rows="2"
                                placeholder="请输入内容" />
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="open = false">关 闭</el-button>
                <el-button type="primary" @click="submitForm" v-if="title !== '血氧数据详情'">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { listBo, getBo, delBo, addBo, updateBo } from "@/api/medical/bo";
import { parseTime } from "@/utils/ruoyi";

export default {
    name: "BloodOxygen",
    data() {
        return {
            // 遮罩层
            loading: true,
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
            // 血氧数据表格数据
            boList: [],
            // 日期范围
            dataTimeRange: [],
            // 弹出层标题
            title: "",
            // 是否显示弹出层
            open: false,
            // 查询参数
            queryParams: {
                pageNum: 1,
                pageSize: 10,
                userId: null,
                measurementType: null,
                beginDataTime: null,
                endDataTime: null
            },
            // 表单参数
            form: {},
            // 表单校验
            rules: {
                userId: [
                    { required: true, message: "用户ID不能为空", trigger: "blur" }
                ],
                spo2Value: [
                    { required: true, message: "血氧饱和度不能为空", trigger: "blur" }
                ],
                dataTime: [
                    { required: true, message: "数据时间不能为空", trigger: "blur" }
                ]
            },
            // 测量类型字典
            measurementTypeOptions: [
                { value: "single", label: "单次测量" },
                { value: "continuous", label: "连续测量" },
                { value: "daily", label: "每日统计" }
            ]
        };
    },
    created() {
        this.getList();
    },
    methods: {
        /** 查询血氧数据列表 */
        getList() {
            this.loading = true;
            if (this.dataTimeRange && this.dataTimeRange.length === 2) {
                this.queryParams.beginDataTime = this.dataTimeRange[0];
                this.queryParams.endDataTime = this.dataTimeRange[1];
            } else {
                this.queryParams.beginDataTime = null;
                this.queryParams.endDataTime = null;
            }

            console.log('发送请求，参数:', JSON.stringify(this.queryParams, null, 2));

            listBo(this.queryParams).then(response => {
                console.log('收到响应:', response);
                console.log('响应数据:', JSON.stringify(response.data, null, 2));

                const rawData = response.data?.items || [];
                console.log('原始数据:', JSON.parse(JSON.stringify(rawData)));

                // 转换字段命名风格为snake_case
                const newList = rawData.map(item => ({
                    id: item.id,
                    user_id: item.user_id,
                    spo2_value: item.spo2_value,
                    measurement_type: item.measurement_type,
                    data_time: item.data_time,
                    upload_time: item.upload_time,
                    // 其他字段...
                }));
                console.log('新数组:', JSON.parse(JSON.stringify(newList)));

                // 彻底替换数组引用
                this.boList = newList;
                this.total = response.data?.total || 0;

                // 添加nextTick确保DOM更新后检查
                this.$nextTick(() => {
                    console.log('DOM更新后数据:', JSON.parse(JSON.stringify(this.boList)));

                    // 详细检查表格状态
                    const table = this.$refs.table;
                    console.log('表格实例:', table);
                    console.log('表格绑定数据:', table?.data);
                    console.log('表格列定义:', table?.columns);

                    // 检查第一行数据是否有效
                    if (this.boList.length > 0) {
                        console.log('第一行数据:', this.boList[0]);
                        console.log('表格是否能显示:', table?.$el.querySelector('.el-table__body-wrapper tbody tr'));
                    }
                });

                this.loading = false;
            }).catch(error => {
                console.error('请求出错:', error);
                console.error('错误详情:', error.response?.data || error.message);
                this.loading = false;
            });
        },
        // 取消按钮
        cancel() {
            this.open = false;
            this.reset();
        },
        // 表单重置
        reset() {
            this.form = {
                id: null,
                userId: null,
                recordGroupId: null,
                uploadTime: null,
                dataTime: null,
                spo2Value: null,
                spo2Unit: null,
                measurementStartTime: null,
                measurementEndTime: null,
                measurementTime: null,
                statisticalMethod: null,
                userNotes: null,
                spo2GroupValues: null,
                measurementType: null,
                externalId: null,
                metadataVersion: null
            };
            this.resetForm("form");
        },
        /** 搜索按钮操作 */
        handleQuery() {
            this.queryParams.pageNum = 1;
            this.getList();
        },
        /** 重置按钮操作 */
        resetQuery() {
            this.dataTimeRange = [];
            this.resetForm("queryForm");
            this.handleQuery();
        },
        // 多选框选中数据
        handleSelectionChange(selection) {
            this.ids = selection.map(item => item.id);
            this.single = selection.length !== 1;
            this.multiple = !selection.length;
        },
        /** 详情按钮操作 */
        handleDetail(row) {
            this.reset();
            const id = row.id || this.ids;
            getBo(id).then(response => {
                this.form = response.data;
                this.open = true;
                this.title = "血氧数据详情";
            });
        },
        /** 新增按钮操作 */
        handleAdd() {
            this.reset();
            this.open = true;
            this.title = "添加血氧数据";
        },
        /** 修改按钮操作 */
        handleUpdate(row) {
            console.log('修改按钮点击，行数据:', row);
            this.reset();
            const id = row.id || this.ids;
            console.log('准备获取数据，ID:', id);

            getBo(id).then(response => {
                console.log('获取详情响应:', response);

                // 完整字段转换（详情/修改对话框）
                this.form = {
                    id: response.data.id,
                    userId: response.data.user_id,
                    spo2Value: response.data.spo2_value,
                    spo2Unit: response.data.spo2_unit || '%',
                    measurementType: response.data.measurement_type,
                    measurementTime: response.data.measurement_time,
                    measurementStartTime: response.data.measurement_start_time,
                    measurementEndTime: response.data.measurement_end_time,
                    statisticalMethod: response.data.statistical_method,
                    dataTime: response.data.data_time,
                    uploadTime: response.data.upload_time,
                    recordGroupId: response.data.record_group_id,
                    externalId: response.data.external_id,
                    metadataVersion: response.data.metadata_version || 1,
                    userNotes: response.data.user_notes || '',
                    spo2GroupValues: response.data.spo2_group_values
                };

                console.log('表单数据:', this.form);
                this.open = true;
                this.title = "修改血氧数据";

                // 添加对话框状态检查
                this.$nextTick(() => {
                    console.log('对话框状态:', this.open);
                    const dialog = document.querySelector('.el-dialog__wrapper');
                    console.log('对话框DOM:', dialog);
                    console.log('对话框可见性:', dialog?.style.display);
                    console.log('对话框类名:', dialog?.className);
                    console.log('对话框z-index:', dialog?.style.zIndex);

                    // 强制检查Vue组件实例
                    if (this.$refs.dialog) {
                        console.log('对话框组件实例:', this.$refs.dialog);
                        console.log('对话框组件visible状态:', this.$refs.dialog?.visible);
                    } else {
                        console.warn('未找到对话框组件引用');
                    }
                });
            }).catch(error => {
                console.error('获取详情失败:', error);
                this.$modal.msgError("获取数据失败");
            });
        },

        /** 详情按钮操作 */
        handleDetail(row) {
            console.log('详情按钮点击，行数据:', row);
            this.reset();
            const id = row.id || this.ids;
            getBo(id).then(response => {
                this.form = {
                    id: response.data.id,
                    userId: response.data.user_id,
                    spo2Value: response.data.spo2_value,
                    measurementType: response.data.measurement_type,
                    dataTime: response.data.data_time,
                    uploadTime: response.data.upload_time,
                };
                this.open = true;
                this.title = "血氧数据详情";

                this.$nextTick(() => {
                    console.log('详情对话框状态:', this.open);
                });
            });
        },
        /** 提交按钮 */
        submitForm() {
            console.log('提交表单，数据:', JSON.parse(JSON.stringify(this.form)));
            this.$refs["form"].validate(valid => {
                if (valid) {
                    console.log('表单验证通过，准备提交');

                    // 转换字段命名风格为snake_case
                    const submitData = {
                        id: this.form.id,
                        user_id: this.form.userId,
                        spo2_value: this.form.spo2Value,
                        measurement_type: this.form.measurementType,
                        data_time: this.form.dataTime,
                        upload_time: this.form.uploadTime,
                        user_notes: this.form.userNotes
                    };

                    console.log('提交数据:', submitData);

                    if (this.form.id != null) {
                        updateBo(submitData).then(response => {
                            console.log('修改成功响应:', response);
                            this.$modal.msgSuccess("修改成功");
                            this.open = false;
                            this.getList();
                        }).catch(error => {
                            console.error('修改失败:', error);
                            this.$modal.msgError("修改失败");
                        });
                    } else {
                        addBo(submitData).then(response => {
                            console.log('新增成功响应:', response);
                            this.$modal.msgSuccess("新增成功");
                            this.open = false;
                            this.getList();
                        }).catch(error => {
                            console.error('新增失败:', error);
                            this.$modal.msgError("新增失败");
                        });
                    }
                } else {
                    console.log('表单验证未通过');
                    return false;
                }
            });
        },
        /** 删除按钮操作 */
        handleDelete(row) {
            const ids = row.id || this.ids;
            this.$modal.confirm('是否确认删除血氧数据ID为"' + ids + '"的数据项？').then(function () {
                return delBo(ids);
            }).then(() => {
                this.getList();
                this.$modal.msgSuccess("删除成功");
            }).catch(() => { });
        }
    }
};
</script>