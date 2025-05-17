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
            <!-- 默认新增按钮 -->
            <el-col :span="1.5" v-if="!getToolbarButtons().length">
                <el-button type="primary" plain icon="el-icon-plus" size="small" @click="handleAdd"
                    v-hasPermi="[`${config.permissionPrefix}:add`]">新增</el-button>
            </el-col>

            <!-- 自定义工具栏按钮 -->
            <template v-if="getToolbarButtons().length">
                <el-col :span="1.5" v-for="(btn, index) in getToolbarButtons()" :key="index">
                    <el-button :type="btn.type || 'default'" :plain="true" :icon="getIconClass(btn.icon)"
                        :size="btn.size || 'small'" :loading="btn.loading ? this[btn.loading] || false : false"
                        @click="handleButtonClick(btn)" v-if="btn.permission">
                        {{ btn.label }}
                    </el-button>
                </el-col>
            </template>

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
            <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
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
            </el-form>

            <!-- 自定义详情内容插槽 -->
            <div v-if="title.includes('详情') && config.slots && config.slots.detailAfter">
                <component :is="config.slots.detailAfter" />
            </div>

            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="open = false">取 消</el-button>
                    <el-button type="primary" @click="submitForm" v-if="!title.includes('详情')">确 定</el-button>
                </div>
            </template>
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
            syncLoading: false, // 添加同步加载状态
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
        // 获取工具栏按钮 - 同时支持buttons和toolbarButtons属性
        getToolbarButtons() {
            // 首先检查toolbarButtons是否存在
            if (this.config.toolbarButtons && Array.isArray(this.config.toolbarButtons)) {
                return this.config.toolbarButtons;
            }

            // 然后检查buttons是否存在
            if (this.config.buttons && Array.isArray(this.config.buttons)) {
                return this.config.buttons;
            }

            // 如果都不存在，返回空数组
            return [];
        },

        handleAdd() {
            // 使用自定义handleAdd方法（如果存在）
            if (this.config.methods && typeof this.config.methods.handleAdd === 'function') {
                console.log('使用自定义handleAdd方法');
                this.config.methods.handleAdd.call(this);
                return;
            }

            this.reset();
            this.open = true;
            this.title = `添加${this.config.title}`;
        },

        // 处理自定义按钮点击
        handleButtonClick(btn) {
            const methodName = btn.onClick;
            if (methodName && this.config.methods && this.config.methods[methodName]) {
                this.config.methods[methodName](this);
            } else if (methodName && typeof this[methodName] === 'function') {
                this[methodName]();
            } else {
                console.error(`按钮定义了动作 ${methodName}，但没有找到对应的方法`);

                // 尝试触发事件，事件名称为 kebab-case 格式的方法名
                // 例如: syncData -> sync-data
                const eventName = methodName.replace(/([A-Z])/g, '-$1').toLowerCase();
                if (eventName) {
                    console.log(`尝试触发事件: ${eventName}`);
                    this.$emit(eventName);
                }
            }
        },

        // 获取按钮图标类名
        getIconClass(icon) {
            if (!icon) return '';
            return icon.startsWith('el-icon-') ? icon : `el-icon-${icon.toLowerCase()}`;
        },

        getQueryParams() {
            const params = {};
            this.config.searchFields.forEach(field => {
                if (this.queryParams[field.prop] !== undefined && this.queryParams[field.prop] !== '') {
                    // 特殊处理日期范围，转换为后端需要的开始和结束日期参数
                    if (field.type === 'daterange' && Array.isArray(this.queryParams[field.prop])) {
                        // 处理日期范围为开始和结束日期
                        if (field.prop === 'dataTimeRange') {
                            // RRI数据的日期范围特殊处理
                            // 为开始日期添加时间部分 "00:00:00"
                            params['begin_data_time'] = this.queryParams[field.prop][0] + ' 00:00:00';
                            // 为结束日期添加时间部分 "23:59:59"，以包含整天
                            params['end_data_time'] = this.queryParams[field.prop][1] + ' 23:59:59';

                            // 同时添加data_time_range参数，以适配后端处理逻辑
                            params['data_time_range'] = [
                                this.queryParams[field.prop][0] + ' 00:00:00',
                                this.queryParams[field.prop][1] + ' 23:59:59'
                            ];
                        } else {
                            // 通用处理方式
                            const fieldBase = field.prop.replace(/Range$/, '');
                            params[`begin_${fieldBase}`] = this.queryParams[field.prop][0] + ' 00:00:00';
                            params[`end_${fieldBase}`] = this.queryParams[field.prop][1] + ' 23:59:59';
                        }
                    } else {
                        params[field.prop] = this.queryParams[field.prop];
                    }
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
            // 使用自定义handleDetail方法（如果存在）
            if (this.config.methods && typeof this.config.methods.handleDetail === 'function') {
                console.log('使用自定义handleDetail方法');
                this.config.methods.handleDetail.call(this, row);
                return;
            }

            this.form = this.transformResponse(row);
            this.title = `${this.config.title}详情`;
            this.open = true;
            // 触发详情事件，通知父组件
            this.$emit('detail', row);
        },

        handleUpdate(row) {
            // 使用自定义handleUpdate方法（如果存在）
            if (this.config.methods && typeof this.config.methods.handleUpdate === 'function') {
                console.log('使用自定义handleUpdate方法');
                this.config.methods.handleUpdate.call(this, row);
                return;
            }

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

                // 记录日期相关参数
                if (params.begin_data_time || params.end_data_time) {
                    console.log('日期查询参数:', {
                        begin_data_time: params.begin_data_time,
                        end_data_time: params.end_data_time,
                        format: 'YYYY-MM-DD HH:mm:ss'
                    });
                }

                // 使用自定义getList方法（如果存在）
                if (this.config.methods && typeof this.config.methods.getList === 'function') {
                    console.log('使用自定义getList方法');
                    this.config.methods.getList.call(this);
                    return;
                }

                const apiPath = this.resolveApiPath();
                console.log('===== getList中的apiPath ======');
                console.log('apiPath是否存在:', !!apiPath);
                console.log('apiPath对象内容:', apiPath);
                if (apiPath && apiPath.list) {
                    console.log('apiPath.list是否是函数:', typeof apiPath.list === 'function');
                    console.log('apiPath.list的值:', apiPath.list);
                }

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

            console.log('==== 调试API路径 ====');
            console.log('当前组件配置:', this.config);
            console.log('API模块路径:', path);
            console.log('完整的this.$api对象:', this.$api);

            for (const key of path) {
                if (!current[key]) {
                    console.error(`API路径解析失败: ${path.join('.')}`, this.$api);
                    return null;
                }
                current = current[key];
                console.log(`解析路径[${key}]后的current对象:`, current);
            }

            console.log('最终解析的API对象:', current);
            console.log('list属性类型:', typeof current.list);
            console.log('list属性值:', current.list);

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
            try {
                if (value === null || value === undefined) {
                    return '-';
                }

                // 根据字段类型格式化值
                if (field.type === 'date' || field.type === 'datetime') {
                    // 使用导入的parseTime函数格式化日期
                    return parseTime(value);
                } else if (field.type === 'select' && field.props) {
                    // 对于下拉选择框，显示选项标签而不是值
                    const options = Array.isArray(field.props.options)
                        ? field.props.options
                        : [];
                    const option = options.find(opt => opt.value === value);
                    return option ? option.label : value;
                }

                return value;
            } catch (error) {
                console.error('formatFieldValue error:', error);
                return value || '-';
            }
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

        // 提交表单
        submitForm() {
            // 使用自定义submitForm方法（如果存在）
            if (this.config.methods && typeof this.config.methods.submitForm === 'function') {
                console.log('使用自定义submitForm方法');
                this.config.methods.submitForm.call(this);
                return;
            }

            this.$refs.formRef.validate(valid => {
                if (valid) {
                    const apiPath = this.resolveApiPath();
                    if (!apiPath) {
                        return;
                    }

                    const submitData = {};
                    // 转换表单数据为后端期望的格式
                    Object.keys(this.form).forEach(key => {
                        // 将驼峰命名转换为下划线命名
                        const snakeKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
                        submitData[snakeKey] = this.form[key];
                    });

                    const method = this.form.id ? apiPath.update : apiPath.add;
                    const successMsg = this.form.id ? '修改成功' : '新增成功';

                    method(submitData).then(response => {
                        this.$modal.msgSuccess(successMsg);
                        this.open = false;
                        this.getList();
                    }).catch(error => {
                        console.error('提交失败:', error);
                        this.$modal.msgError('提交失败：' + (error.message || '未知错误'));
                    });
                }
            });
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