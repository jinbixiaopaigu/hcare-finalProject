<template>
    <div class="app-container">
        <!-- 查询表单 -->
        <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch">
            <template v-for="(field, index) in config.searchFields" :key="index">
                <el-form-item :label="field.label" :prop="field.prop">
                    <component :is="getComponentType(field.type)" v-model="queryParams[field.prop]"
                        v-bind="field.props || {}" @keyup.enter.native="handleQuery" />
                </el-form-item>
            </template>
            <el-form-item>
                <el-button type="primary" icon="el-icon-search" size="small" @click="handleQuery">搜索</el-button>
                <el-button icon="el-icon-refresh" size="small" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>

        <!-- 操作按钮 -->
        <el-row :gutter="10" class="mb8">
            <el-col :span="1.5">
                <el-button type="primary" plain icon="el-icon-plus" size="small" @click="handleAdd"
                    v-hasPermi="[`${config.permissionPrefix}:add`]">新增</el-button>
            </el-col>
            <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
        </el-row>

        <!-- 数据表格 -->
        <el-table v-loading="loading" :data="tableData" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" align="center" />
            <template v-for="(column, index) in config.tableColumns" :key="index">
                <el-table-column :label="column.label" :align="column.align || 'center'" :prop="column.prop"
                    :width="column.width">
                    <template #default="{ row }">
                        <template v-if="column.type === 'dict'">
                            <dict-tag :options="column.dictOptions" :value="row[column.prop]" />
                        </template>
                        <template v-else-if="column.type === 'time'">
                            <span>{{ parseTime(row[column.prop]) }}</span>
                        </template>
                        <template v-else>
                            {{ row[column.prop] }}
                        </template>
                    </template>
                </el-table-column>
            </template>
            <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                <template #default="{ row }">
                    <el-button size="small" type="text" icon="el-icon-view" @click="handleDetail(row)"
                        v-hasPermi="[`${config.permissionPrefix}:query`]">详情</el-button>
                    <el-button size="small" type="text" icon="el-icon-edit" @click="handleUpdate(row)"
                        v-hasPermi="[`${config.permissionPrefix}:edit`]">修改</el-button>
                    <el-button size="small" type="text" icon="el-icon-delete" @click="handleDelete(row)"
                        v-hasPermi="[`${config.permissionPrefix}:remove`]">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页组件 -->
        <pagination v-show="total > 0" :total="total" v-model:page="queryParams.page_num"
            v-model:limit="queryParams.page_size" @pagination="getList" />

        <!-- 详情/编辑对话框 -->
        <el-dialog :title="title" v-model="open" width="700px" append-to-body>
            <el-form ref="form" :model="form" :rules="rules" label-width="120px">
                <el-row>
                    <template v-for="(field, index) in config.formFields" :key="index">
                        <el-col :span="field.span || 12">
                            <el-form-item :label="field.label" :prop="field.prop">
                                <component :is="getComponentType(field.type)" v-model="form[field.prop]"
                                    v-bind="field.props || {}" :disabled="title.includes('详情')" />
                            </el-form-item>
                        </el-col>
                    </template>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="open = false">关 闭</el-button>
                <el-button type="primary" @click="submitForm" v-if="!title.includes('详情')">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { parseTime } from "@/utils/ruoyi";

export default {
    name: "BaseTablePage",
    props: {
        config: {
            type: Object,
            required: true,
            validator: (value) => {
                return [
                    'apiModule',
                    'apiPath',
                    'permissionPrefix',
                    'searchFields',
                    'tableColumns',
                    'formFields',
                    'rules'
                ].every(key => key in value)
            }
        }
    },
    data() {
        return {
            loading: true,
            ids: [],
            single: true,
            multiple: true,
            showSearch: true,
            total: 0,
            tableData: [],
            title: "",
            open: false,
            queryParams: {
                page_num: 1,
                page_size: 10,
                ...this.getDefaultQueryParams()
            },
            form: this.getDefaultFormData(),
            rules: this.config.rules || {}
        };
    },
    created() {
        this.getList();
    },
    methods: {
        getList() {
            this.loading = true;
            try {
                const params = {
                    page_num: this.queryParams.page_num,
                    page_size: this.queryParams.page_size,
                    ...this.getQueryParams()
                };

                console.log('API请求参数:', params);

                const apiPath = this.resolveApiPath();
                if (!apiPath) {
                    this.loading = false;
                    return;
                }

                apiPath.list(params)
                    .then(response => {
                        this.tableData = response.data?.items || [];
                        this.total = response.data?.total || 0;
                        this.loading = false;
                    })
                    .catch(error => {
                        console.error('获取数据失败:', error);
                        this.loading = false;
                        this.$modal.msgError("获取数据失败");
                    });
            } catch (error) {
                console.error('请求处理异常:', error);
                this.loading = false;
                this.$modal.msgError("请求处理异常");
            }
        },

        // 其他方法保持不变...
        resolveApiPath() {
            if (!this.$api) {
                console.error('$api未注入到Vue实例');
                return null;
            }

            let current = this.$api;
            const path = [this.config.apiModule, this.config.apiPath];

            for (const key of path) {
                if (!current[key]) {
                    console.error(`API路径解析失败: ${path.join('.')}`, this.$api);
                    return null;
                }
                current = current[key];
            }

            return current;
        },

        getDefaultQueryParams() {
            const params = {};
            this.config.searchFields.forEach(field => {
                params[field.prop] = undefined;
            });
            return params;
        },

        getDefaultFormData() {
            const form = {};
            this.config.formFields.forEach(field => {
                form[field.prop] = null;
            });
            return form;
        },

        getComponentType(type) {
            const componentMap = {
                'input': 'el-input',
                'select': 'el-select',
                'date': 'el-date-picker',
                'datetime': 'el-date-picker',
                'daterange': 'el-date-picker',
            };
            return componentMap[type] || 'el-input';
        },

        // 其他辅助方法...
    }
}
</script>

<style scoped>
.app-container {
    padding: 20px;
}
</style>