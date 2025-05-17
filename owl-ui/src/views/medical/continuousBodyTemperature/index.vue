<template>
    <BaseTablePage ref="baseTable" :config="config" @table-mounted="onTableMounted" @form-mounted="onFormMounted"
        @sync-data="handleSyncData" />
</template>

<script>
import BaseTablePage from '@/components/BaseTablePage'
import { continuousBodyTemperatureConfig } from '@/config/tableConfigs/continuousBodyTemperature'
import { listCbt, getCbt, delCbt, addCbt, updateCbt, syncCbt } from "@/api/medical/cbt";
import { ElMessage } from 'element-plus'

export default {
    name: 'ContinuousBodyTemperature',
    components: { BaseTablePage },
    data() {
        return {
            // 查询参数
            queryParams: {
                page_num: 1,
                page_size: 10,
                user_id: undefined,
                measurement_part: undefined,
                begin_data_time: undefined,
                end_data_time: undefined
            },
            cbtList: [],
            total: 0,
            loading: false,
            syncLoading: false,
            config: {
                ...continuousBodyTemperatureConfig,
                // 确保所有必要的属性都存在
                searchFields: continuousBodyTemperatureConfig.searchFields || [],
                tableColumns: continuousBodyTemperatureConfig.tableColumns || [],
                formFields: continuousBodyTemperatureConfig.formFields || [],
                apiModule: 'medical',
                apiPath: 'cbt',
                permissionPrefix: 'medical:continuousBodyTemperature',
                rules: continuousBodyTemperatureConfig.rules || {},
                // 覆盖默认方法，保留原有逻辑
                methods: {
                    getList: this.getList,
                    handleDetail: this.handleDetail,
                    handleUpdate: this.handleUpdate,
                    submitForm: this.submitForm,
                    syncData: this.handleSyncData,
                    handleAdd: this.handleAdd
                }
            }
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
        },
        // 查询体温数据列表
        getList() {
            this.loading = true;
            // 确保queryParams一定存在
            const params = {
                page_num: this.queryParams?.page_num || 1,
                page_size: this.queryParams?.page_size || 10,
                user_id: this.queryParams?.user_id,
                measurement_part: this.queryParams?.measurement_part,
                begin_data_time: this.queryParams?.begin_data_time,
                end_data_time: this.queryParams?.end_data_time
            };

            console.log('发送请求，参数:', JSON.stringify(params, null, 2));

            listCbt(params).then(response => {
                console.log('收到响应:', response);
                // 修改：同时支持items和rows字段
                const rawData = response.data?.items || response.data?.rows || [];
                console.log('原始数据:', rawData);

                // 数据已经是驼峰式命名，直接使用
                this.cbtList = rawData;
                this.total = response.data?.total || 0;
                this.loading = false;

                // 更新BaseTablePage的数据
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.tableData = this.cbtList;
                    this.$refs.baseTable.total = this.total;
                    this.$refs.baseTable.loading = false;
                }
            }).catch(error => {
                console.error('请求出错:', error);
                this.loading = false;
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.loading = false;
                }
                ElMessage.error("获取数据失败");
            });
        },

        // 处理详情
        handleDetail(row) {
            console.log('详情按钮点击，行数据:', row);
            this.reset();
            const id = row.id || this.ids;
            getCbt(id).then(response => {
                // 转换字段命名风格
                const formData = this.transformResponse(response.data);
                // 更新BaseTablePage的表单数据
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.form = formData;
                    this.$refs.baseTable.title = "持续体温数据详情";
                    this.$refs.baseTable.open = true;
                }
            });
        },

        // 处理修改
        handleUpdate(row) {
            console.log('修改按钮点击，行数据:', row);
            this.reset();
            const id = row.id || this.ids;
            getCbt(id).then(response => {
                // 转换字段命名风格
                const formData = this.transformResponse(response.data);
                // 更新BaseTablePage的表单数据
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.form = formData;
                    this.$refs.baseTable.title = "修改持续体温数据";
                    this.$refs.baseTable.open = true;
                }
            });
        },

        // 处理新增
        handleAdd() {
            this.reset();
            // 更新BaseTablePage的表单数据
            if (this.$refs.baseTable) {
                this.$refs.baseTable.title = "新增持续体温数据";
                this.$refs.baseTable.open = true;
            }
        },

        // 提交表单
        submitForm() {
            if (this.$refs.baseTable && this.$refs.baseTable.$refs.formRef) {
                this.$refs.baseTable.$refs.formRef.validate(valid => {
                    if (valid) {
                        const formData = this.$refs.baseTable.form;
                        // 转换为后端需要的格式
                        const submitData = this.transformRequest(formData);

                        if (formData.id) {
                            updateCbt(submitData).then(response => {
                                ElMessage.success("修改成功");
                                this.$refs.baseTable.open = false;
                                this.getList();
                            }).catch(error => {
                                console.error('修改失败:', error);
                                ElMessage.error("修改失败");
                            });
                        } else {
                            addCbt(submitData).then(response => {
                                ElMessage.success("新增成功");
                                this.$refs.baseTable.open = false;
                                this.getList();
                            }).catch(error => {
                                console.error('新增失败:', error);
                                ElMessage.error("新增失败");
                            });
                        }
                    }
                });
            }
        },

        // 重置表单
        reset() {
            this.form = {};
            if (this.$refs.baseTable && this.$refs.baseTable.$refs.formRef) {
                this.$refs.baseTable.$refs.formRef.resetFields();
            }
        },

        // 处理同步数据
        async handleSyncData() {
            try {
                this.syncLoading = true;
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.syncLoading = true;
                }
                const res = await syncCbt();
                const { added, updated } = res.data || {};
                ElMessage.success(`同步完成！新增${added || 0}条记录，更新${updated || 0}条记录`);

                // 刷新数据表格
                this.getList();
            } catch (error) {
                console.error('同步体温数据失败:', error);
                ElMessage.error('同步数据失败：' + (error.message || '未知错误'));
            } finally {
                this.syncLoading = false;
                if (this.$refs.baseTable) {
                    this.$refs.baseTable.syncLoading = false;
                }
            }
        },

        // 转换响应数据为前端格式
        transformResponse(data) {
            return {
                id: data.id,
                userId: data.user_id,
                measurementPart: data.measurement_part,
                temperatureValue: data.body_temperature,
                skinTemperature: data.skin_temperature,
                dataTime: data.data_time,
                uploadTime: data.upload_time
            };
        },

        // 转换请求数据为后端格式
        transformRequest(data) {
            return {
                id: data.id,
                user_id: data.userId,
                measurement_part: data.measurementPart,
                body_temperature: data.temperatureValue,
                skin_temperature: data.skinTemperature,
                data_time: data.dataTime,
                upload_time: data.uploadTime
            };
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