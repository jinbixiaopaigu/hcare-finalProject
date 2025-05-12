<template>
    <BaseTablePage :config="config" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { bloodOxygenConfig } from '@/config/tableConfigs/bloodOxygen'
import { listBo, getBo, delBo, addBo, updateBo } from "@/api/medical/bo";
import { parseTime } from "@/utils/ruoyi";

export default {
    name: 'BloodOxygen',
    components: { BaseTablePage },
    data() {
        return {
            config: {
                ...bloodOxygenConfig,
                // 覆盖默认方法，保留原有逻辑
                methods: {
                    getList: this.getList,
                    handleDateChange: this.handleDateChange,
                    handleDetail: this.handleDetail,
                    handleUpdate: this.handleUpdate,
                    submitForm: this.submitForm
                }
            }
        }
    },
    methods: {
        /** 查询血氧数据列表 */
        getList() {
            this.loading = true;
            const params = {
                page_num: this.queryParams.page_num,
                page_size: this.queryParams.page_size,
                user_id: this.queryParams.user_id,
                measurement_type: this.queryParams.measurement_type,
                begin_data_time: this.queryParams.begin_data_time,
                end_data_time: this.queryParams.end_data_time
            };

            console.log('发送请求，参数:', JSON.stringify(params, null, 2));

            listBo(params).then(response => {
                console.log('收到响应:', response);
                const rawData = response.data?.items || [];
                console.log('原始数据:', JSON.parse(JSON.stringify(rawData)));

                // 转换字段命名风格
                const newList = rawData.map(item => ({
                    id: item.id,
                    user_id: item.user_id,
                    spo2_value: item.spo2_value,
                    measurement_type: item.measurement_type,
                    data_time: item.data_time,
                    upload_time: item.upload_time,
                    user_notes: item.user_notes || item.userNotes || null
                }));

                this.boList = newList;
                this.total = response.data?.total || 0;
                this.loading = false;
            }).catch(error => {
                console.error('请求出错:', error);
                this.loading = false;
            });
        },

        /** 日期范围变化 */
        handleDateChange(range) {
            console.log('日期变化事件触发，range:', range);
            this.dataTimeRange = range || [];

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
            getBo(id).then(response => {
                this.form = {
                    id: response.data.id,
                    userId: response.data.user_id,
                    spo2Value: response.data.spo2_value,
                    measurementType: response.data.measurement_type,
                    dataTime: response.data.data_time,
                    uploadTime: response.data.upload_time,
                    userNotes: response.data.user_notes || response.data.userNotes || ''
                };
                this.open = true;
                this.title = "血氧数据详情";
            });
        },

        /** 修改按钮操作 */
        handleUpdate(row) {
            console.log('修改按钮点击，行数据:', row);
            this.reset();
            const id = row.id || this.ids;
            console.log('准备获取数据，ID:', id);

            getBo(id).then(response => {
                console.log('获取详情响应:', response);
                this.form = {
                    id: response.data.id,
                    userId: response.data.user_id,
                    spo2Value: response.data.spo2_value,
                    spo2Unit: response.data.spo2_unit || '%',
                    measurementType: response.data.measurement_type,
                    measurementTime: response.data.measurement_time,
                    dataTime: response.data.data_time,
                    uploadTime: response.data.upload_time,
                    userNotes: response.data.user_notes || ''
                };
                this.open = true;
                this.title = "修改血氧数据";
            }).catch(error => {
                console.error('获取详情失败:', error);
                this.$modal.msgError("获取数据失败");
            });
        },

        /** 提交按钮 */
        submitForm() {
            console.log('提交表单，数据:', JSON.parse(JSON.stringify(this.form)));
            this.$refs["form"].validate(valid => {
                if (valid) {
                    console.log('表单验证通过，准备提交');

                    // 转换字段命名风格
                    const submitData = {
                        id: this.form.id,
                        user_id: this.form.userId,
                        spo2_value: this.form.spo2Value,
                        measurement_type: this.form.measurementType,
                        data_time: this.form.dataTime,
                        upload_time: this.form.uploadTime,
                        user_notes: this.form.userNotes
                    };

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
                }
            });
        }
    }
}
</script>

<style scoped>
.el-button--text {
    color: var(--el-color-primary);
    background: transparent;
    border: none;
    padding: 0;
}

.el-button--text:hover {
    color: var(--el-color-primary-light-3);
}
</style>