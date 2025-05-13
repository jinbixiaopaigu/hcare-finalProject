<template>
    <div class="app-container">
        <!-- 查询表单 -->
        <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch">
            <template v-for="(field, index) in config.searchFields" :key="index">
                <el-form-item :label="field.label" :prop="field.prop">
                    <template v-if="field.type === 'select'">
                        <el-select v-model="queryParams[field.prop]" v-bind="field.props || {}"
                            @keyup.enter.native="handleQuery" style="width: 200px">
                            <el-option v-for="item in field.props.options" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </template>
                    <template v-else-if="field.type === 'daterange'">
                        <el-date-picker v-model="queryParams[field.prop]" type="daterange" range-separator="至"
                            start-placeholder="开始日期" end-placeholder="结束日期" value-format="YYYY-MM-DD"
                            style="width: 240px" @keyup.enter.native="handleQuery" v-bind="field.props || {}" />
                    </template>
                    <component v-else :is="getComponentType(field.type)" v-model="queryParams[field.prop]"
                        v-hasPermi="[`${config.permissionPrefix}:add`]">新增</component>
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
        <pagination v-show="total > 0" :total="total" :page.sync="queryParams.page_num"
            :limit.sync="queryParams.page_size" @pagination="handlePaginationChange" />

        <!-- 详情/编辑对话框 -->
        <el-dialog :title="title" v-model="open" width="700px" append-to-body>
            <el-row>
                <template v-for="(field, index) in config.formFields" :key="index">
                    <el-col :span="field.span || 12">
                        <el-form-item :label="field.label" :prop="field.prop">
                            <!-- 详情模式下显示纯文本 -->
                            <template v-if="title.includes('详情')">
                                <div class="form-text-display">{{ formatFieldValue(field, form[field.prop]) }}</div>
                            </template>
                            <!-- 修改模式下，只有特定字段可编辑，其他显示纯文本 -->
                            <template v-else-if="!isEditableField(field.prop)">
                                <div class="form-text-display">{{ formatFieldValue(field, form[field.prop]) }}</div>
                            </template>
                            <!-- 可编辑字段使用组件 -->
                            <template v-else>
                                <component :is="getComponentType(field.type)" v-model="form[field.prop]"
                                    v-bind="getComponentProps(field)">
                                    <!-- 如果是select类型，渲染选项 -->
                                    <template v-if="field.type === 'select' && field.props && field.props.options">
                                        <el-option v-for="option in field.props.options" :key="option.value"
                                            :label="option.label" :value="option.value">
                                        </el-option>
                                    </template>
                                </component>
                            </template>
                        </el-form-item>
                    </el-col>
                </template>
            </el-row>

            <div slot="footer" class="dialog-footer">
                <el-button @click="open = false">关 闭</el-button>
                <el-button type="primary" @click="submitForm" v-if="!title.includes('详情')">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { parseTime } from '@/utils/ruoyi';

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
        handleAdd() {
            this.reset();
            this.open = true;
            this.title = `添加${this.config.title}`;
        },

        getQueryParams() {
            const params = {};
            this.config.searchFields.forEach(field => {
                if (this.queryParams[field.prop] !== undefined && this.queryParams[field.prop] !== '') {
                    params[field.prop] = this.queryParams[field.prop];
                }
            });
            return params;
        },

        handleSelectionChange(selection) {
            this.ids = selection.map(item => item.id);
            this.single = selection.length !== 1;
            this.multiple = !selection.length;
        },

        handleQuery() {
            this.queryParams.page_num = 1;
            this.getList();
        },

        transformResponse(data) {
            // 将后端snake_case字段名转换为前端camelCase
            const transformed = {};
            for (const key in data) {
                const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
                transformed[camelKey] = data[key];
            }
            return transformed;
        },

        handleDetail(row) {
            this.form = this.transformResponse(row);
            this.title = `${this.config.title}详情`;
            this.open = true;
        },

        handleUpdate(row) {
            this.form = this.transformResponse(row);
            this.title = `修改${this.config.title}`;
            this.open = true;
        },

        reset() {
            this.form = {};
            this.$refs.formRef?.resetFields();
        },

        resetQuery() {
            this.resetForm("queryForm");
            this.handleQuery();
        },

        getList() {
            this.loading = true;
            try {
                // 转换参数名适配后端API
                const params = {
                    page: this.queryParams.page_num,  // 后端可能使用page而不是page_num
                    pageSize: this.queryParams.page_size, // 后端可能使用pageSize而不是page_size
                    ...this.getQueryParams()
                };

                console.log('转换后的请求参数:', params);

                console.log('API请求参数:', JSON.stringify(params, null, 2));

                const apiPath = this.resolveApiPath();
                if (!apiPath) {
                    this.loading = false;
                    return;
                }

                apiPath.list(params)
                    .then(response => {
                        // console.log('API完整响应:', JSON.stringify(response.data, null, 2));
                        // console.log('请求页码:', params.page_num, '响应页码:', response.data.current_page);

                        // if (params.page_num !== response.data.current_page) {
                        //     console.warn('警告：请求页码与响应页码不一致！');
                        // }

                        console.group('[BaseTablePage] 数据加载');
                        console.log('完整响应:', response);
                        console.log('items字段:', response.data?.items);
                        console.log('rows字段:', response.data?.rows);

                        // 兼容两种数据格式
                        const data = response.data || {};
                        this.tableData = data.items || data.rows || [];
                        this.total = data.total || 0;

                        console.log('绑定到表格的数据:', this.tableData);
                        console.log('总记录数:', this.total);
                        console.groupEnd();

                        this.loading = false;

                        // 检查表格渲染状态
                        this.$nextTick(() => {
                            console.log('表格渲染完成, 可见行数:',
                                this.$el.querySelectorAll('.el-table__body-wrapper tr').length);
                        });
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
        handlePaginationChange({ page, limit }) {
            console.log('分页变化:', { page, limit });
            this.queryParams.page_num = page;
            this.queryParams.page_size = limit;
            this.getList();
        },

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

        // 判断字段是否可编辑（在修改模式下）
        isEditableField(prop) {
            // 只有userNotes和measurementType字段可编辑
            return ['userNotes', 'measurementType'].includes(prop);
        },

        // 格式化字段值显示
        formatFieldValue(field, value) {
            if (value === null || value === undefined) {
                return '-';
            }

            // 根据字段类型格式化值
            if (field.type === 'date' || field.type === 'datetime') {
                // 使用导入的parseTime函数格式化日期
                return parseTime(value);
            } else if (field.type === 'select' && field.props && field.props.options) {
                // 对于下拉选择框，显示选项标签而不是值
                const option = field.props.options.find(opt => opt.value === value);
                return option ? option.label : value;
            }

            return value;
        },

        // 处理组件属性
        getComponentProps(field) {
            // 获取字段的props配置
            const props = { ...(field.props || {}) };

            // 如果是可编辑字段（在修改模式下），不使用disabled属性
            if (!this.title.includes('详情') && this.isEditableField(field.prop)) {
                delete props.disabled;
            }
            // 否则，如果props中有disabled函数，执行它获取实际的disabled值
            else if (typeof props.disabled === 'function') {
                props.disabled = props.disabled(this.config);
            }

            return props;
        },

        // 其他辅助方法...
    }
}
</script>

<style scoped>
.app-container {
    padding: 20px;
}

.form-text-display {
    min-height: 32px;
    line-height: 32px;
    color: #606266;
    word-break: break-all;
}
</style>