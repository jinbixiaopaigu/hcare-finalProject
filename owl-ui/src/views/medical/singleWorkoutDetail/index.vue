<template>
    <BaseTablePage ref="baseTable" :config="config" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { singleWorkoutDetailConfig } from '@/config/tableConfigs/singleWorkoutDetail'
import { listSwd, getSwd, delSwd, addSwd, updateSwd, syncSwd } from "@/api/medical/swd";
import { parseTime } from "@/utils/ruoyi";

export default {
    name: 'SingleWorkoutDetail',
    components: { BaseTablePage },
    data() {
        return {
            queryParams: {
                page_num: 1,
                page_size: 10,
                user_id: undefined,
                workout_type: undefined,
                begin_data_time: undefined,
                end_data_time: undefined
            },
            swdList: [],
            total: 0,
            loading: false,
            config: {
                ...singleWorkoutDetailConfig,
                // 添加searchFields属性，使用searchItems的值
                searchFields: singleWorkoutDetailConfig.searchItems || [],
                // 添加tableColumns属性，使用columns的值
                tableColumns: singleWorkoutDetailConfig.columns || [],
                // 添加formFields属性，使用formItems的值
                formFields: singleWorkoutDetailConfig.formItems || [],
                // API模块和路径
                apiModule: 'medical',
                apiPath: 'swd',
                // 权限前缀
                permissionPrefix: 'medical:swd',
                // 添加空的规则对象
                rules: {},
                // 添加工具栏按钮
                toolbarButtons: [
                    { label: '新增', icon: 'plus', type: 'primary', permission: 'add', onClick: 'handleAdd' },
                    { label: '同步数据', icon: 'refresh', type: 'success', permission: 'sync', onClick: 'syncData', loading: 'syncLoading' }
                ],
                // 覆盖默认方法，保留原有逻辑
                methods: {
                    getList: this.getList,
                    handleDateChange: this.handleDateChange,
                    handleDetail: this.handleDetail,
                    handleUpdate: this.handleUpdate,
                    submitForm: this.submitForm,
                    syncData: this.syncData,
                    handleAdd: this.handleAdd
                }
            }
        }
    },
    methods: {
        /** 查询6分钟行走测试数据列表 */
        getList() {
            this.loading = true;
            // 确保queryParams一定存在
            const params = {
                page_num: this.queryParams?.page_num || 1,
                page_size: this.queryParams?.page_size || 10,
                user_id: this.queryParams?.user_id,
                workout_type: this.queryParams?.workout_type,
                begin_data_time: this.queryParams?.begin_data_time,
                end_data_time: this.queryParams?.end_data_time
            };

            console.log('发送请求，参数:', JSON.stringify(params, null, 2));

            listSwd(params).then(response => {
                console.log('收到响应:', response);
                // 同时支持items和rows字段
                const rawData = response.data?.items || response.data?.rows || [];
                console.log('原始数据:', JSON.parse(JSON.stringify(rawData)));

                // 转换字段命名风格
                const newList = rawData.map(item => ({
                    id: item.id,
                    user_id: item.user_id,
                    step_count: item.step_count,
                    distance: item.distance,
                    distance_unit: item.distance_unit,
                    heart_rate: item.heart_rate,
                    speed: item.speed,
                    speed_unit: item.speed_unit,
                    step_frequency: item.step_frequency,
                    calories: item.calories,
                    workout_type: item.workout_type,
                    workout_status: item.workout_status,
                    data_time: item.data_time,
                    upload_time: item.upload_time,
                    user_notes: item.user_notes || item.userNotes || null
                }));

                this.swdList = newList;
                this.total = response.data?.total || 0;
                this.loading = false;

                // 更新BaseTablePage组件的数据
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.tableData = this.swdList;
                    this.$refs.baseTable.total = this.total;
                    this.$refs.baseTable.loading = false;
                }
            }).catch(error => {
                console.error('请求出错:', error);
                this.loading = false;
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.loading = false;
                }
            });
        },

        /** 日期范围变化 */
        handleDateChange(range) {
            console.log('日期变化事件触发，range:', range);
            this.dataTimeRange = range || [];

            // 确保queryParams一定存在
            if (!this.queryParams) {
                this.queryParams = {
                    page_num: 1,
                    page_size: 10
                };
            }

            if (range && range.length === 2) {
                this.queryParams.begin_data_time = range[0] + ' 00:00:00';
                this.queryParams.end_data_time = range[1] + ' 23:59:59';
            } else {
                this.queryParams.begin_data_time = undefined;
                this.queryParams.end_data_time = undefined;
            }
        },

        /** 详情按钮操作 */
        handleDetail(row) {
            console.log('详情按钮点击，行数据:', row);
            this.reset();
            const id = row.id || this.ids;
            getSwd(id).then(response => {
                this.form = {
                    id: response.data.id,
                    userId: response.data.user_id,
                    stepCount: response.data.step_count,
                    distance: response.data.distance,
                    distanceUnit: response.data.distance_unit,
                    heartRate: response.data.heart_rate,
                    speed: response.data.speed,
                    speedUnit: response.data.speed_unit,
                    stepFrequency: response.data.step_frequency,
                    calories: response.data.calories,
                    workoutType: response.data.workout_type,
                    workoutStatus: response.data.workout_status,
                    dataTime: response.data.data_time,
                    uploadTime: response.data.upload_time,
                    userNotes: response.data.user_notes || response.data.userNotes || ''
                };

                // 使用baseTable组件处理表单展示
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.form = this.form;
                    this.$refs.baseTable.open = true;
                    this.$refs.baseTable.title = "6分钟行走测试数据详情";
                } else {
                    this.open = true;
                    this.title = "6分钟行走测试数据详情";
                }
            });
        },

        /** 修改按钮操作 */
        handleUpdate(row) {
            console.log('修改按钮点击，行数据:', row);
            this.reset();
            const id = row.id || this.ids;
            console.log('准备获取数据，ID:', id);

            getSwd(id).then(response => {
                console.log('获取详情响应:', response);
                this.form = {
                    id: response.data.id,
                    userId: response.data.user_id,
                    stepCount: response.data.step_count,
                    distance: response.data.distance,
                    distanceUnit: response.data.distance_unit || 'm',
                    heartRate: response.data.heart_rate,
                    speed: response.data.speed,
                    speedUnit: response.data.speed_unit || 'm/s',
                    stepFrequency: response.data.step_frequency,
                    calories: response.data.calories,
                    workoutType: response.data.workout_type,
                    workoutStatus: response.data.workout_status,
                    dataTime: response.data.data_time,
                    uploadTime: response.data.upload_time,
                    userNotes: response.data.user_notes || ''
                };

                // 使用baseTable组件处理表单展示
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.form = this.form;
                    this.$refs.baseTable.open = true;
                    this.$refs.baseTable.title = "修改6分钟行走测试数据";
                } else {
                    this.open = true;
                    this.title = "修改6分钟行走测试数据";
                }
            }).catch(error => {
                console.error('获取详情失败:', error);
                this.$modal.msgError("获取数据失败");
            });
        },

        /** 提交按钮 */
        submitForm() {
            console.log('提交表单，数据:', JSON.parse(JSON.stringify(this.form)));

            // 使用baseTable组件或当前组件的表单引用
            const formRef = (this.$refs.baseTable && this.$refs.baseTable.$refs.formRef) || this.$refs.form;
            const formData = (this.$refs.baseTable && this.$refs.baseTable.form) || this.form;

            formRef.validate(valid => {
                if (valid) {
                    console.log('表单验证通过，准备提交');

                    // 转换字段命名风格
                    const submitData = {
                        id: formData.id,
                        user_id: formData.userId,
                        step_count: formData.stepCount,
                        distance: formData.distance,
                        distance_unit: formData.distanceUnit,
                        heart_rate: formData.heartRate,
                        speed: formData.speed,
                        speed_unit: formData.speedUnit,
                        step_frequency: formData.stepFrequency,
                        calories: formData.calories,
                        workout_type: formData.workoutType,
                        workout_status: formData.workoutStatus,
                        data_time: formData.dataTime,
                        upload_time: formData.uploadTime,
                        user_notes: formData.userNotes
                    };

                    if (formData.id != null) {
                        updateSwd(submitData).then(response => {
                            console.log('修改成功响应:', response);
                            this.$modal.msgSuccess("修改成功");

                            // 关闭对话框
                            if (this.$refs.baseTable) {
                                this.$refs.baseTable.open = false;
                            } else {
                                this.open = false;
                            }

                            this.getList();
                        }).catch(error => {
                            console.error('修改失败:', error);
                            this.$modal.msgError("修改失败");
                        });
                    } else {
                        addSwd(submitData).then(response => {
                            console.log('新增成功响应:', response);
                            this.$modal.msgSuccess("新增成功");

                            // 关闭对话框
                            if (this.$refs.baseTable) {
                                this.$refs.baseTable.open = false;
                            } else {
                                this.open = false;
                            }

                            this.getList();
                        }).catch(error => {
                            console.error('新增失败:', error);
                            this.$modal.msgError("新增失败");
                        });
                    }
                }
            });
        },

        /** 同步数据 */
        syncData() {
            this.$modal.confirm('确认要从华为Research同步6分钟行走测试数据吗？').then(() => {
                this.syncLoading = true;
                syncSwd().then(response => {
                    console.log('同步响应:', response);
                    this.$modal.msgSuccess("同步成功，新增 " + response.data.added + " 条数据");
                    this.syncLoading = false;
                    this.getList();
                }).catch(error => {
                    console.error('同步失败:', error);
                    this.$modal.msgError("同步失败");
                    this.syncLoading = false;
                });
            });
        },

        // 重置表单
        reset() {
            this.form = {
                id: undefined,
                userId: undefined,
                stepCount: undefined,
                distance: undefined,
                distanceUnit: 'm',
                heartRate: undefined,
                speed: undefined,
                speedUnit: 'm/s',
                stepFrequency: undefined,
                calories: undefined,
                workoutType: undefined,
                workoutStatus: undefined,
                dataTime: undefined,
                uploadTime: undefined,
                userNotes: undefined
            };
            this.resetForm("form");
        }
    }
}
</script>