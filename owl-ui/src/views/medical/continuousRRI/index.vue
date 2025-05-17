<template>
    <div>
        <!-- 直接添加分组图表按钮 -->
        <div style="margin-bottom: 10px;">
            <el-button type="primary" icon="el-icon-picture" @click="viewGroupedRRIChart">查看分组图表</el-button>
            <el-checkbox v-model="useCache" style="margin-left: 10px;">使用缓存</el-checkbox>
            <el-tooltip content="启用缓存会大幅提高加载速度，但数据可能不是最新的" placement="top">
                <i class="el-icon-question" style="margin-left: 5px;"></i>
            </el-tooltip>
            <el-button v-if="useCache" type="text" icon="el-icon-refresh" @click="clearCache">清除缓存</el-button>
        </div>

        <BaseTablePage ref="baseTable" :config="config" @table-mounted="onTableMounted" @form-mounted="onFormMounted"
            @detail="onViewDetail" />

        <!-- 单条RRI图表对话框 -->
        <el-dialog :title="'RRI数据可视化 - ' + currentUser" v-model="chartVisible" width="80%" append-to-body>
            <div v-loading="chartLoading">
                <div id="rriChart" style="width: 100%; height: 400px;"></div>
                <div class="chart-info" v-if="chartData.length > 0">
                    <el-row>
                        <el-col :span="8">
                            <div class="info-item">
                                <span class="label">有效数据点：</span>
                                <span class="value">{{ validPoints }}个</span>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <div class="info-item">
                                <span class="label">平均值：</span>
                                <span class="value">{{ avgRRI }}ms</span>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <div class="info-item">
                                <span class="label">数据范围：</span>
                                <span class="value">{{ minRRI }}-{{ maxRRI }}ms</span>
                            </div>
                        </el-col>
                    </el-row>
                </div>
                <div class="no-data" v-else>
                    <el-empty description="无有效RRI数据"></el-empty>
                </div>
            </div>
        </el-dialog>

        <!-- 分组图表对话框 -->
        <el-dialog title="RRI数据分组图表" v-model="groupChartVisible" width="90%" :destroy-on-close="true"
            :close-on-click-modal="false" @opened="onDialogOpened">
            <div v-loading="groupChartLoading">
                <div class="group-selector" v-if="serverChartGroups.length > 0">
                    <span>请选择数据分组：</span>
                    <el-select v-model="currentGroupIndex" @change="switchServerChart" placeholder="请选择数据分组">
                        <el-option v-for="(group, index) in serverChartGroups" :key="index"
                            :label="`分组${group.groupId}: ${group.startTime} - ${group.endTime}, ${group.validPoints}条数据`"
                            :value="index">
                        </el-option>
                    </el-select>
                </div>

                <!-- 显示图表区域 -->
                <div v-if="currentServerChart" class="server-chart-container">
                    <div id="groupRRIChart" style="width: 100%; height: 450px; margin-top: 15px;"></div>

                    <!-- 图表信息 -->
                    <div class="chart-info" style="margin-top: 20px;">
                        <el-row>
                            <el-col :span="6">
                                <div class="info-item">
                                    <span class="label">时间范围：</span>
                                    <span class="value">{{ currentServerChart.startTime }} - {{
                                        currentServerChart.endTime }}</span>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="info-item">
                                    <span class="label">有效数据点：</span>
                                    <span class="value">{{ currentServerChart.validPoints }}个</span>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="info-item">
                                    <span class="label">平均值：</span>
                                    <span class="value">{{ currentServerChart.avgRRI }}ms</span>
                                </div>
                            </el-col>
                            <el-col :span="6">
                                <div class="info-item">
                                    <span class="label">数据范围：</span>
                                    <span class="value">{{ currentServerChart.minRRI }}-{{ currentServerChart.maxRRI
                                        }}ms</span>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                </div>

                <div class="no-data" v-else-if="!groupChartLoading">
                    <el-empty description="无有效RRI数据图表"></el-empty>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import * as echarts from 'echarts'
import * as crriApi from '@/api/medical/crri'
import BaseTablePage from '@/components/BaseTablePage'
import { continuousRRIConfig } from '@/config/tableConfigs/continuousRRI'

export default {
    name: 'ContinuousRRI',
    components: {
        BaseTablePage
    },
    data() {
        return {
            config: {
                ...continuousRRIConfig,
                toolbarButtons: continuousRRIConfig.toolbarButtons || [],
                buttons: continuousRRIConfig.toolbarButtons || [],
                methods: {
                    syncData: this.handleSyncData,
                    viewRRIChart: this.viewRRIChart,
                    viewGroupedRRIChart: this.viewGroupedRRIChart
                }
            },
            chartVisible: false,
            chartLoading: false,
            chartInstance: null,
            chartData: [],
            currentUser: '',
            currentRow: null,
            validPoints: 0,
            avgRRI: 0,
            minRRI: 0,
            maxRRI: 0,
            dataFieldFixed: false,

            // 分组图表相关数据
            groupChartVisible: false,
            groupChartLoading: false,
            groupChartInstance: null,
            rriGroups: [],
            currentGroupIndex: 0,
            groupChartData: [],
            groupValidPoints: 0,
            groupAvgRRI: 0,
            groupMinRRI: 0,
            groupMaxRRI: 0,
            currentGroupStartTime: null,
            currentGroupEndTime: null,

            // 服务器端生成的图表数据
            serverChartGroups: [],
            currentServerChart: null,
            useCache: true
        }
    },
    methods: {
        onTableMounted() {
            // 表格加载完成后的回调
            console.log('表格加载完成')
        },
        onFormMounted() {
            // 表单加载完成后的回调
            console.log('表单加载完成')
        },
        handleSyncData() {
            this.$modal.confirm('是否确认同步连续RRI数据？').then(() => {
                crriApi.sync().then(response => {
                    this.$modal.msgSuccess('同步成功')
                    this.$refs.baseTable.getList()
                }).catch(error => {
                    console.error('同步失败:', error)
                    this.$modal.msgError('同步失败：' + (error.message || '未知错误'))
                })
            })
        },
        onViewDetail(row) {
            // 当查看详情时，保存当前行数据，但不再显示图表
            console.log('详情页面打开，不显示图表')
            this.currentRow = row
            this.currentUser = row.userId || '未知用户'
        },

        // 分组图表相关方法
        viewGroupedRRIChart() {
            console.warn('==== [DEBUG-1] 开始查看RRI分组图表 ====');
            try {
                // 在打开弹窗前，查找并移除可能已经存在的重复容器
                console.warn('==== [DEBUG-1.0] 检查并清理现有容器 ====');
                const existingContainers = document.querySelectorAll('.server-chart-container');
                console.warn(`找到 ${existingContainers.length} 个现有容器`);

                // 如果有多个容器，仅保留第一个（Vue模板渲染的）
                if (existingContainers.length > 1) {
                    console.warn('==== [DEBUG-1.01] 清理多余容器 ====');
                    for (let i = 1; i < existingContainers.length; i++) {
                        if (existingContainers[i].parentNode) {
                            existingContainers[i].parentNode.removeChild(existingContainers[i]);
                        }
                    }
                }

                // 打开弹窗，但等待弹窗打开事件处理获取数据
                this.groupChartLoading = true;
                this.serverChartGroups = [];
                this.currentServerChart = null;

                // 检查当前组件结构
                console.warn('==== [DEBUG-1.1] 检查当前组件结构 ====');
                console.warn(`组件DOM元素存在: ${!!this.$el}`);
                console.warn(`弹窗容器类名: ${this.$el.className}`);
                console.warn(`子元素数量: ${this.$el.children.length}`);

                // 强制创建弹窗容器
                if (!document.querySelector('.dialog-container')) {
                    console.warn('==== [DEBUG-1.2] 尝试创建弹窗容器 ====');
                    const dialogContainer = document.createElement('div');
                    dialogContainer.className = 'dialog-container';
                    this.$el.appendChild(dialogContainer);
                }

                // 先显示弹窗，在opened事件中处理后续操作
                this.groupChartVisible = true;
                console.warn('==== [DEBUG-2] 弹窗显示标志已设置 ====');

                // 添加直接DOM检查，延长超时时间，确保DOM有足够时间渲染
                setTimeout(() => {
                    console.warn('==== [DEBUG-3] 检查DOM状态 ====');
                    const dialogs = document.querySelectorAll('.el-dialog');
                    console.warn(`发现 ${dialogs.length} 个弹窗元素`);
                    if (dialogs.length === 0) {
                        console.warn('==== [DEBUG-3.1] 尝试查找不同类名的弹窗 ====');
                        const possibleDialogs = [
                            document.querySelectorAll('.el-overlay'),
                            document.querySelectorAll('.el-overlay-dialog'),
                            document.querySelectorAll('[role="dialog"]')
                        ];
                        possibleDialogs.forEach((elems, idx) => {
                            console.warn(`备选弹窗选择器 ${idx + 1}: 找到 ${elems.length} 个元素`);
                        });
                    }

                    const chartContainers = document.querySelectorAll('.server-chart-container');
                    console.warn(`发现 ${chartContainers.length} 个图表容器`);
                    const chartElements = document.querySelectorAll('#groupRRIChart');
                    console.warn(`发现 ${chartElements.length} 个图表元素`);

                    // 如果DOM仍未渲染，手动触发打开事件
                    if (dialogs.length === 0 && chartElements.length === 0) {
                        console.warn('==== [DEBUG-3.2] DOM未正确渲染，手动触发事件 ====');
                        this.onDialogOpened();
                    }
                }, 2000);  // 延长到2秒
            } catch (error) {
                console.error('==== [ERROR] 打开弹窗失败 ====', error);
                this.$modal.msgError('打开图表失败: ' + (error.message || '未知错误'));
                this.groupChartLoading = false;
            }
        },

        onDialogOpened() {
            console.warn('==== [DEBUG-4] 弹窗打开事件触发 ====');
            try {
                // 先检查是否已经有VUE模板渲染的容器
                const vueRenderedContainer = document.querySelector('[data-v-9a2b367d].server-chart-container');
                if (vueRenderedContainer) {
                    console.warn('==== [DEBUG-4.0] 已找到Vue渲染的容器，使用现有容器 ====');
                    // 使用现有容器，直接获取数据
                    this.fetchServerGeneratedCharts();
                    return;
                }

                // 检查是否有任何其他.server-chart-container容器
                const otherContainers = document.querySelectorAll('.server-chart-container');
                if (otherContainers.length > 0) {
                    console.warn(`==== [DEBUG-4.1] 找到${otherContainers.length}个非Vue渲染的容器 ====`);
                    // 删除多余的容器
                    otherContainers.forEach(container => {
                        if (container.parentNode) {
                            container.parentNode.removeChild(container);
                        }
                    });
                }

                // 确保弹窗容器存在
                let dialogBody = document.querySelector('.el-dialog__body');
                if (!dialogBody) {
                    console.warn('==== [DEBUG-4.2] 未找到弹窗主体，尝试备选选择器 ====');
                    const selectors = [
                        '.el-overlay-dialog .el-dialog__body',
                        '.el-overlay [role="dialog"] .el-dialog__body',
                        '[role="dialog"] .el-dialog__body'
                    ];

                    for (const selector of selectors) {
                        dialogBody = document.querySelector(selector);
                        if (dialogBody) {
                            console.warn(`找到弹窗主体: ${selector}`);
                            break;
                        }
                    }
                }

                if (!dialogBody) {
                    console.warn('==== [DEBUG-4.3] 无法找到弹窗主体，无法创建图表容器 ====');
                    // 直接获取数据，不创建容器
                    this.fetchServerGeneratedCharts();
                    return;
                }

                // 获取数据
                console.warn('==== [DEBUG-7] 开始获取数据 ====');
                this.fetchServerGeneratedCharts();
            } catch (error) {
                console.error('==== [ERROR] 弹窗打开事件处理失败 ====', error);
                // 不管发生什么错误，尝试获取数据
                this.fetchServerGeneratedCharts();
            }
        },

        createChartContainer() {
            try {
                console.warn('==== [DEBUG-10] 开始创建图表容器 ====');

                // 首先检查是否已经存在Vue渲染的server-chart-container容器
                const existingContainer = document.querySelector('.server-chart-container');
                if (existingContainer) {
                    console.warn('==== [DEBUG-10.1] 已找到Vue渲染的图表容器，不再创建重复容器 ====');
                    return true;
                }

                // 策略1: 查找弹窗主体 .el-dialog__body
                let dialogBody = document.querySelector('.el-dialog__body');
                console.warn(`==== [DEBUG-11] 查找弹窗主体: ${!!dialogBody} ====`);

                // 策略2: 如果找不到常规弹窗，尝试新版Element Plus弹窗结构
                if (!dialogBody) {
                    console.warn('==== [DEBUG-12] 尝试查找新版Element Plus弹窗结构 ====');
                    const newDialogSelectors = [
                        '.el-overlay-dialog .el-dialog__body',
                        '.el-overlay [role="dialog"] .el-dialog__body',
                        '[role="dialog"] .el-dialog__body'
                    ];

                    for (const selector of newDialogSelectors) {
                        dialogBody = document.querySelector(selector);
                        if (dialogBody) {
                            console.warn(`==== [DEBUG-13] 找到弹窗主体: ${selector} ====`);
                            break;
                        }
                    }
                }

                // 策略3: 如果仍然找不到，尝试获取任何可用的弹窗或覆盖层元素
                if (!dialogBody) {
                    console.warn('==== [DEBUG-14] 尝试查找任何弹窗相关元素 ====');
                    const fallbackSelectors = [
                        '.el-overlay-dialog',
                        '.el-overlay',
                        '[role="dialog"]',
                        '.el-dialog',
                        '.temp-chart-container'
                    ];

                    for (const selector of fallbackSelectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            console.warn(`==== [DEBUG-15] 找到备选容器: ${selector} ====`);
                            dialogBody = element;
                            break;
                        }
                    }
                }

                // 策略4: 实在找不到任何容器，创建一个临时容器附加到body
                if (!dialogBody) {
                    console.warn('==== [DEBUG-16] 无法找到容器，创建临时容器 ====');
                    dialogBody = document.createElement('div');
                    dialogBody.className = 'temp-chart-container';
                    dialogBody.style.cssText = 'position:fixed;top:10%;left:10%;width:80%;height:80%;z-index:9999;background:#fff;padding:20px;border-radius:4px;box-shadow:0 0 10px rgba(0,0,0,0.2);';

                    // 添加一个标题
                    const title = document.createElement('h3');
                    title.textContent = 'RRI数据分组图表';
                    title.style.cssText = 'margin-bottom:20px;font-size:18px;border-bottom:1px solid #eee;padding-bottom:10px;';
                    dialogBody.appendChild(title);

                    // 添加一个关闭按钮
                    const closeBtn = document.createElement('button');
                    closeBtn.textContent = '关闭';
                    closeBtn.style.cssText = 'position:absolute;top:10px;right:10px;border:none;background:#f56c6c;color:#fff;padding:5px 10px;border-radius:3px;cursor:pointer;';
                    closeBtn.onclick = () => {
                        document.body.removeChild(dialogBody);
                        this.groupChartVisible = false;
                    };
                    dialogBody.appendChild(closeBtn);

                    document.body.appendChild(dialogBody);
                }

                // 检查是否已有容器
                if (dialogBody.querySelector('#groupRRIChart')) {
                    console.warn('==== [DEBUG-17] 图表容器已存在 ====');
                    return true;
                }

                // 创建图表容器
                console.warn('==== [DEBUG-18] 手动创建图表容器 ====');
                const container = document.createElement('div');
                container.className = 'server-chart-container';
                container.innerHTML = `
                    <div id="groupRRIChart" style="width: 100%; height: 450px; margin-top: 15px;"></div>
                    <div class="chart-info" style="margin-top: 20px;">
                        <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
                            <div class="info-item" style="width: 48%; margin-bottom: 10px;">
                                <span class="label" style="font-weight: bold;">时间范围：</span>
                                <span class="value" style="color: #409EFF;">加载中...</span>
                            </div>
                            <div class="info-item" style="width: 48%; margin-bottom: 10px;">
                                <span class="label" style="font-weight: bold;">有效数据点：</span>
                                <span class="value" style="color: #409EFF;">加载中...</span>
                            </div>
                            <div class="info-item" style="width: 48%; margin-bottom: 10px;">
                                <span class="label" style="font-weight: bold;">平均值：</span>
                                <span class="value" style="color: #409EFF;">加载中...</span>
                            </div>
                            <div class="info-item" style="width: 48%; margin-bottom: 10px;">
                                <span class="label" style="font-weight: bold;">数据范围：</span>
                                <span class="value" style="color: #409EFF;">加载中...</span>
                            </div>
                        </div>
                    </div>
                `;

                // 添加到弹窗
                dialogBody.appendChild(container);
                console.warn('==== [DEBUG-19] 图表容器创建完成，再次检查 ====');
                const createdContainer = dialogBody.querySelector('#groupRRIChart');
                console.warn(`创建后是否找到图表容器: ${!!createdContainer}`);

                return !!createdContainer;
            } catch (error) {
                console.error('==== [ERROR] 创建图表容器失败 ====', error);
                return false;
            }
        },

        async fetchServerGeneratedCharts() {
            try {
                console.warn('==== [DEBUG-13] 开始获取图表数据 ====');

                // 检查并清理DOM中的重复容器
                console.warn('==== [DEBUG-13.1] 检查DOM元素 ====');
                const allContainers = document.querySelectorAll('.server-chart-container');
                console.warn(`找到 ${allContainers.length} 个图表容器`);

                // 如果存在多个容器，保留Vue渲染的容器，删除其他容器
                if (allContainers.length > 1) {
                    console.warn('==== [DEBUG-13.2] 清理重复容器 ====');
                    const vueContainer = document.querySelector('[data-v-9a2b367d].server-chart-container');

                    // 如果找到了Vue渲染的容器，删除所有其他容器
                    if (vueContainer) {
                        const nonVueContainers = document.querySelectorAll('.server-chart-container:not([data-v-9a2b367d])');
                        console.warn(`找到 ${nonVueContainers.length} 个非Vue容器`);
                        nonVueContainers.forEach(container => {
                            if (container.parentNode) {
                                console.warn('移除非Vue容器');
                                container.parentNode.removeChild(container);
                            }
                        });
                    }
                }

                // 使用现有搜索条件
                const query = this.$refs.baseTable ? this.$refs.baseTable.searchForm || {} : {};
                // 添加图表相关参数
                const chartParams = {
                    ...query,
                    maxPoints: 5000,  // 每组最大数据点数
                    samplingRate: 1,    // 采样率，1表示不采样
                    useCache: this.useCache  // 是否使用缓存
                };

                this.$message.info('正在获取数据，请稍候...');

                // 使用专用的图表API获取已处理的数据
                console.warn('==== [DEBUG-14] 调用API获取数据 ====');
                const response = await crriApi.getChart(chartParams);

                console.warn('==== [DEBUG-15] 获取到图表数据 ====', response ? '成功' : '失败');

                if (response && response.data && Array.isArray(response.data) && response.data.length > 0) {
                    console.warn(`==== [DEBUG-16] 数据处理开始，分组数: ${response.data.length} ====`);
                    // 直接使用后端处理好的图表数据
                    this.serverChartGroups = response.data;
                    console.warn(`获取到${this.serverChartGroups.length}个分组图表数据`);

                    // 显示数据采样信息
                    const totalOriginalPoints = this.serverChartGroups.reduce((sum, group) =>
                        sum + (group.originalPoints || 0), 0);
                    const totalActualPoints = this.serverChartGroups.reduce((sum, group) =>
                        sum + (group.validPoints || 0), 0);
                    console.warn(`==== [DEBUG-17] 处理前共${totalOriginalPoints}个数据点，采样后共${totalActualPoints}个数据点 ====`);

                    if (totalOriginalPoints > totalActualPoints) {
                        this.$message.info(`为提高性能，已对大量数据进行采样：${totalOriginalPoints} → ${totalActualPoints}个数据点`);
                    }

                    this.currentGroupIndex = 0;
                    this.currentServerChart = this.serverChartGroups[0];

                    // 确保图表容器存在
                    console.warn('==== [DEBUG-18] 准备初始化图表 ====');
                    this.$nextTick(() => {
                        // 等待DOM更新，多次尝试初始化图表
                        let attempts = 0;
                        const maxAttempts = 3;

                        const tryInitChart = () => {
                            attempts++;
                            console.warn(`==== [DEBUG-19] 尝试初始化图表 (尝试 ${attempts}/${maxAttempts}) ====`);

                            const chartDom = document.getElementById('groupRRIChart');
                            console.warn(`图表容器存在: ${!!chartDom}`);

                            if (!chartDom && attempts < maxAttempts) {
                                // 尝试创建容器
                                console.warn(`==== [DEBUG-20] 图表容器不存在，尝试创建 (尝试 ${attempts}) ====`);
                                const created = this.createChartContainer();

                                if (created) {
                                    // 创建成功，直接初始化
                                    console.warn('==== [DEBUG-21] 容器创建成功，初始化图表 ====');
                                    this.initAndRenderChart();
                                } else {
                                    // 创建失败，延迟重试
                                    console.warn(`==== [DEBUG-22] 容器创建失败，${500 * attempts}毫秒后重试 ====`);
                                    setTimeout(tryInitChart, 500 * attempts);
                                }
                            } else if (chartDom) {
                                // 容器存在，初始化图表
                                console.warn('==== [DEBUG-23] 容器已存在，初始化图表 ====');
                                this.initAndRenderChart();
                            } else {
                                // 多次尝试仍然失败，创建应急替代方案
                                console.warn('==== [DEBUG-24] 多次尝试失败，创建应急图表容器 ====');
                                this.createEmergencyChartContainer();
                            }
                        };

                        // 开始尝试
                        setTimeout(tryInitChart, 300);
                    });
                } else {
                    console.warn('==== [DEBUG-25] 获取数据失败或数据为空 ====');
                    this.$modal.msgWarning('未获取到有效的RRI数据');
                }
            } catch (error) {
                console.warn('==== [DEBUG-26] 获取数据出错 ====', error);
                this.$modal.msgError('获取数据失败: ' + (error.message || '未知错误'));
            } finally {
                this.groupChartLoading = false;
            }
        },

        initAndRenderChart(customContainerId) {
            console.warn('==== [DEBUG-26] 开始初始化图表 ====');
            // 使用自定义容器ID或默认ID
            const containerId = customContainerId || 'groupRRIChart';
            console.warn(`==== [DEBUG-26.1] 使用图表容器ID: ${containerId} ====`);

            const chartDom = document.getElementById(containerId);
            if (!chartDom) {
                console.warn(`==== [DEBUG-27] 图表容器(${containerId})不存在，无法初始化图表 ====`);
                return;
            }

            // 如果已存在图表实例，先销毁
            if (this.groupChartInstance) {
                console.warn('==== [DEBUG-28] 销毁旧图表实例 ====');
                this.groupChartInstance.dispose();
                this.groupChartInstance = null;
            }

            try {
                console.warn('==== [DEBUG-29] 创建图表实例 ====');
                this.groupChartInstance = echarts.init(chartDom);

                // 设置基础配置
                const option = {
                    title: {
                        text: 'RRI数据趋势图',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            if (!params || !params[0] || !params[0].data) {
                                return '无数据';
                            }

                            try {
                                const data = params[0].data;
                                const time = new Date(data[0]).toLocaleString();
                                const rri = data[1] !== undefined ? data[1] : '无';
                                const sqi = data[2] !== undefined ? data[2] : '无';
                                return `时间：${time}<br/>RRI：${rri}ms<br/>信号质量：${sqi}`;
                            } catch (e) {
                                console.error('tooltip格式化错误:', e);
                                return '数据格式错误';
                            }
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '8%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'time',
                        name: '时间',
                        nameLocation: 'middle',
                        nameGap: 30
                    },
                    yAxis: {
                        type: 'value',
                        name: 'RRI(ms)',
                        nameLocation: 'middle',
                        nameGap: 30,
                        min: 1, // 设置固定最小值，避免自动计算可能导致的断言错误
                        max: 3000, // 设置固定最大值
                        minInterval: 1, // 设置最小间隔，避免精度问题
                        scale: true // 允许缩放调整，但保留最小最大值限制
                    },
                    dataZoom: [
                        {
                            type: 'slider',
                            show: true,
                            xAxisIndex: [0],
                            start: 0,
                            end: 100,
                            bottom: 10
                        },
                        {
                            type: 'inside',
                            xAxisIndex: [0],
                            start: 0,
                            end: 100
                        }
                    ],
                    series: [{
                        name: 'RRI数据',
                        type: 'line',
                        symbol: 'circle',
                        symbolSize: 4,
                        sampling: 'average',
                        itemStyle: {
                            color: '#5470c6'
                        },
                        data: [],
                        // 添加进度渲染选项，优化大数据渲染性能
                        progressive: 500,
                        progressiveThreshold: 5000
                    }]
                };

                this.groupChartInstance.setOption(option);
                console.warn('==== [DEBUG-30] 图表实例创建成功，准备渲染数据 ====');

                // 渲染图表数据
                if (this.currentServerChart && this.currentServerChart.data) {
                    console.warn(`==== [DEBUG-31] 开始渲染图表数据，数据点数量: ${this.currentServerChart.data.length} ====`);
                    this.renderServerChart(this.currentServerChart.data);
                }
            } catch (error) {
                console.warn('==== [DEBUG-32] 初始化图表失败 ====', error);
                this.$modal.msgError('初始化图表失败: ' + (error.message || '未知错误'));
            }
        },

        renderServerChart(data) {
            console.warn('==== [DEBUG-33] 渲染图表数据 ====');
            if (!this.groupChartInstance) {
                console.warn('==== [DEBUG-34] 图表实例不存在 ====');
                return;
            }

            const defaultRRIValue = 800;

            try {
                // 验证数据
                if (!data || !Array.isArray(data)) {
                    console.warn('==== [DEBUG-35] 图表数据无效 ====');
                    this.groupChartInstance.setOption({
                        series: [{
                            data: []
                        }]
                    });
                    return;
                }

                // 日志数据量信息
                console.warn(`==== [DEBUG-36] 图表数据点数: ${data.length} ====`);

                // 如果数据为空，显示空图表
                if (data.length === 0) {
                    console.warn('==== [DEBUG-37] 数据为空 ====');
                    this.groupChartInstance.setOption({
                        series: [{
                            data: []
                        }]
                    });
                    return;
                }

                // 检查并过滤数据中的无效值
                let chartData = [];
                let hasInvalidData = false;

                // 如果后端返回的数据格式需要转换，在这里处理
                if (!Array.isArray(data[0])) {
                    console.warn('==== [DEBUG-38] 转换非数组格式数据 ====');
                    // 每个元素应该是一个对象，需要转成数组
                    data.forEach(item => {
                        if (!item) return; // 跳过null或undefined

                        const timestamp = item.timestamp || item.time || item[0];
                        const rri = item.rri || item.value || item[1];
                        const sqi = item.sqi || item.quality || item[2] || 0;

                        // 检查值是否有效
                        if (timestamp && !isNaN(new Date(timestamp).getTime()) &&
                            rri !== undefined && rri !== null && !isNaN(rri) && isFinite(rri)) {
                            chartData.push([timestamp, rri, sqi]);
                        } else {
                            hasInvalidData = true;
                        }
                    });
                } else {
                    console.warn('==== [DEBUG-39] 处理数组格式数据 ====');
                    // 数据已经是数组格式，验证格式并过滤无效值
                    chartData = data.filter(item => {
                        if (!item || item.length < 2) {
                            hasInvalidData = true;
                            return false;
                        }

                        const timestamp = item[0];
                        const rri = item[1];

                        // 验证时间戳和RRI值
                        if (timestamp && !isNaN(new Date(timestamp).getTime()) &&
                            rri !== undefined && rri !== null && !isNaN(rri) && isFinite(rri)) {
                            return true;
                        } else {
                            hasInvalidData = true;
                            return false;
                        }
                    });
                }

                if (hasInvalidData) {
                    console.warn('==== [DEBUG-40] 过滤了部分无效数据 ====');
                }

                if (chartData.length === 0) {
                    console.warn('==== [DEBUG-41] 过滤后数据为空 ====');
                    this.groupChartInstance.setOption({
                        series: [{
                            data: []
                        }]
                    });
                    return;
                }

                console.warn(`==== [DEBUG-42] 有效数据点数: ${chartData.length} ====`);

                // 检查数据量，如果太大启用渐进渲染
                const enableProgressive = chartData.length > 5000;

                // 更新图表数据
                console.warn('==== [DEBUG-43] 更新图表数据 ====');

                // 设置Y轴范围，避免ECharts自动计算可能导致的错误
                let minRRI = Number.MAX_VALUE;
                let maxRRI = Number.MIN_VALUE;

                // 计算RRI值的范围
                chartData.forEach(item => {
                    const rri = item[1];
                    if (rri < minRRI) minRRI = rri;
                    if (rri > maxRRI) maxRRI = rri;
                });

                // 确保有合理的Y轴范围
                if (minRRI === maxRRI) {
                    // 如果所有值都一样，设置一个范围
                    minRRI = minRRI * 0.9;
                    maxRRI = maxRRI * 1.1;
                }

                // 安全范围保障
                minRRI = Math.max(1, minRRI * 0.9); // 避免接近0或负值
                maxRRI = Math.min(3000, maxRRI * 1.1); // 设置一个上限以防异常值

                console.warn(`==== [DEBUG-44] 数据范围: ${minRRI} - ${maxRRI} ====`);

                this.groupChartInstance.setOption({
                    yAxis: {
                        min: minRRI,
                        max: maxRRI
                    },
                    series: [{
                        data: chartData,
                        // 大数据量时启用渐进渲染
                        progressive: enableProgressive ? 1000 : 0,
                        progressiveThreshold: enableProgressive ? 3000 : 0,
                        // 如果数据量大，不显示点标记以提高性能
                        symbol: chartData.length > 10000 ? 'none' : 'circle',
                        symbolSize: chartData.length > 10000 ? 0 : 4,
                        markLine: {
                            silent: true,
                            lineStyle: {
                                color: '#333'
                            },
                            data: [{
                                yAxis: defaultRRIValue,
                                name: '替换默认值'
                            }]
                        }
                    }]
                });

                console.warn('==== [DEBUG-45] 图表数据更新完成 ====');
            } catch (error) {
                console.warn('==== [DEBUG-46] 更新图表数据失败 ====', error);

                // 出现错误时设置一个空图表
                try {
                    this.groupChartInstance.setOption({
                        series: [{
                            data: []
                        }]
                    });
                    console.warn('==== [DEBUG-47] 已重置为空图表 ====');
                } catch (e) {
                    console.error('==== [ERROR] 无法重置图表 ====', e);
                }
            }
        },

        viewRRIChart(row) {
            console.log('========== 打开RRI图表对话框 ==========')
            console.log('当前行数据:', row)

            // 修复数据字段
            row = this.fixDataField(row)

            this.currentRow = row
            this.currentUser = row.userId || '未知用户'
            console.log('当前用户:', this.currentUser)

            this.chartVisible = true
            this.chartLoading = true

            this.$nextTick(() => {
                console.log('对话框渲染完成，准备初始化图表')
                const chartDom = document.getElementById('rriChart')
                console.log('图表DOM元素是否存在:', !!chartDom)

                if (chartDom) {
                    this.initChartPopup(chartDom)
                    console.log('图表初始化完成，准备加载数据')
                    this.loadChartData(row)
                } else {
                    console.error('未找到图表DOM元素')
                    this.chartLoading = false
                    this.$modal.msgError('图表初始化失败：未找到图表容器')
                }
            })
        },
        initChartPopup(container) {
            console.log('========== 初始化图表弹窗 ==========')

            // 如果已存在图表实例，先销毁
            if (this.chartInstance) {
                console.log('已存在图表实例，先销毁')
                this.chartInstance.dispose()
            }

            try {
                // 初始化图表
                console.log('创建新图表实例')
                this.chartInstance = echarts.init(container)
                console.log('图表实例创建成功')

                // 设置基础配置
                const option = {
                    title: {
                        text: 'RRI数据趋势图',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            if (!params || !params[0] || !params[0].data) {
                                return '无数据'
                            }

                            try {
                                const data = params[0].data
                                const time = new Date(data[0]).toLocaleString()
                                const rri = data[1] !== undefined ? data[1] : '无'
                                const sqi = data[2] !== undefined ? data[2] : '无'
                                return `时间：${time}<br/>RRI：${rri}ms<br/>信号质量：${sqi}`
                            } catch (e) {
                                console.error('tooltip格式化错误:', e)
                                return '数据格式错误'
                            }
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'time',
                        name: '时间',
                        nameLocation: 'middle',
                        nameGap: 30
                    },
                    yAxis: {
                        type: 'value',
                        name: 'RRI(ms)',
                        nameLocation: 'middle',
                        nameGap: 30,
                        min: 1, // 设置固定最小值，避免自动计算可能导致的断言错误
                        max: 3000, // 设置固定最大值
                        minInterval: 1, // 设置最小间隔，避免精度问题
                        scale: true // 允许缩放调整，但保留最小最大值限制
                    },
                    dataZoom: [
                        {
                            type: 'slider',
                            show: true,
                            xAxisIndex: [0],
                            start: 0,
                            end: 100
                        },
                        {
                            type: 'inside',
                            xAxisIndex: [0],
                            start: 0,
                            end: 100
                        }
                    ],
                    series: [
                        {
                            name: 'RRI数据',
                            type: 'line',
                            symbol: 'circle',
                            symbolSize: 5,
                            sampling: 'average',
                            itemStyle: {
                                color: '#5470c6'
                            },
                            data: []
                        }
                    ]
                }

                console.log('设置图表配置')
                this.chartInstance.setOption(option)
                console.log('图表配置设置完成')
            } catch (error) {
                console.error('初始化图表失败:', error)
                console.error('错误详情:', error.stack)
                this.$modal.msgError('初始化图表失败: ' + (error.message || '未知错误'))
            }
        },
        fixDataField(row) {
            console.log('========== 检查并修复数据字段 ==========')

            // 检查rriData字段是否存在
            if (row.hasOwnProperty('rriData') && row.rriData) {
                console.log('rriData字段存在且有值')
                return row
            }

            console.warn('rriData字段不存在或为空，尝试查找替代字段')

            // 1. 检查常见字段替代
            const possibleFields = ['rri_data', 'rridata', 'RRIData', 'rri', 'data']
            for (const field of possibleFields) {
                if (row.hasOwnProperty(field) && row[field]) {
                    console.log(`找到可能的替代字段: ${field}，值类型:`, typeof row[field])
                    row.rriData = row[field]
                    this.dataFieldFixed = true
                    return row
                }
            }

            // 2. 检查所有字段，寻找可能包含数据的JSON字段
            console.log('未找到预设替代字段，检查所有字段')
            const allFields = Object.keys(row)
            console.log('所有字段:', allFields)

            for (const field of allFields) {
                const value = row[field]
                if (typeof value === 'string' && value.includes('[') && value.includes(']')) {
                    try {
                        const parsed = JSON.parse(value)
                        if (Array.isArray(parsed) && parsed.length > 0) {
                            console.log(`找到可能包含RRI数据的JSON字段: ${field}`)
                            row.rriData = parsed
                            this.dataFieldFixed = true
                            return row
                        }
                    } catch (e) {
                        // 不是有效的JSON，继续检查
                    }
                } else if (Array.isArray(value) && value.length > 0) {
                    console.log(`找到数组类型字段: ${field}，长度: ${value.length}`)
                    row.rriData = value
                    this.dataFieldFixed = true
                    return row
                }
            }

            console.error('未找到任何可能的RRI数据字段')
            return row
        },
        switchServerChart(index) {
            if (index >= 0 && index < this.serverChartGroups.length) {
                this.currentServerChart = this.serverChartGroups[index];

                // 确保图表对象包含必要的字段
                if (!this.currentServerChart.startTime && this.currentServerChart.startDateTime) {
                    this.currentServerChart.startTime = this.currentServerChart.startDateTime;
                }
                if (!this.currentServerChart.endTime && this.currentServerChart.endDateTime) {
                    this.currentServerChart.endTime = this.currentServerChart.endDateTime;
                }
                if (!this.currentServerChart.validPoints && this.currentServerChart.dataCount) {
                    this.currentServerChart.validPoints = this.currentServerChart.dataCount;
                }

                // 根据选择的分组更新图表
                this.$nextTick(() => {
                    this.renderServerChart(this.currentServerChart.data);
                });
            }
        },
        // 清除缓存并重新加载数据
        clearCache() {
            this.useCache = false;
            this.$message.info('已禁用缓存，将获取最新数据');

            if (this.groupChartVisible) {
                // 如果图表已显示，则重新加载
                this.groupChartLoading = true;
                this.fetchServerGeneratedCharts().then(() => {
                    this.useCache = true; // 加载后重新启用缓存
                    this.$message.success('已刷新数据并重新启用缓存');
                });
            }
        },
        // 创建应急图表容器
        createEmergencyChartContainer() {
            console.warn('==== [DEBUG-27] 创建应急图表容器 ====');

            try {
                // 先检查是否有Vue渲染的容器
                const vueContainer = document.querySelector('[data-v-9a2b367d].server-chart-container');
                if (vueContainer) {
                    console.warn('==== [DEBUG-27.1] 已找到Vue渲染的图表容器，使用Vue容器 ====');
                    return true;
                }

                // 检查是否已有应急图表容器
                let existingEmergencyModal = document.querySelector('.emergency-chart-modal');
                if (existingEmergencyModal) {
                    console.warn('==== [DEBUG-27.2] 清理旧的应急容器 ====');
                    document.body.removeChild(existingEmergencyModal);
                }

                // 清理所有非Vue渲染的.server-chart-container
                const extraContainers = document.querySelectorAll('.server-chart-container:not([data-v-9a2b367d])');
                if (extraContainers.length > 0) {
                    console.warn(`==== [DEBUG-27.3] 删除${extraContainers.length}个多余容器 ====`);
                    extraContainers.forEach(container => {
                        if (container.parentNode) {
                            container.parentNode.removeChild(container);
                        }
                    });
                }

                // 创建一个模态弹窗
                const modalContainer = document.createElement('div');
                modalContainer.className = 'emergency-chart-modal';
                modalContainer.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:9999;display:flex;align-items:center;justify-content:center;';

                // 创建弹窗内容
                const modalContent = document.createElement('div');
                modalContent.className = 'emergency-chart-content';
                modalContent.style.cssText = 'width:90%;height:80%;background:#fff;border-radius:4px;box-shadow:0 0 10px rgba(0,0,0,0.3);padding:20px;display:flex;flex-direction:column;';

                // 创建标题栏
                const titleBar = document.createElement('div');
                titleBar.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;border-bottom:1px solid #eee;padding-bottom:10px;';

                const title = document.createElement('h2');
                title.textContent = 'RRI数据分组图表';
                title.style.cssText = 'margin:0;font-size:18px;';

                const closeBtn = document.createElement('button');
                closeBtn.textContent = '关闭';
                closeBtn.style.cssText = 'border:none;background:#f56c6c;color:#fff;padding:5px 15px;border-radius:3px;cursor:pointer;';
                closeBtn.onclick = () => {
                    document.body.removeChild(modalContainer);
                    this.groupChartVisible = false;
                };

                titleBar.appendChild(title);
                titleBar.appendChild(closeBtn);

                // 创建图表容器，使用不同的ID避免冲突
                const chartContainer = document.createElement('div');
                chartContainer.id = 'emergencyGroupRRIChart';
                chartContainer.style.cssText = 'width:100%;height:450px;flex-grow:1;';

                // 创建图表信息区域
                const infoContainer = document.createElement('div');
                infoContainer.className = 'chart-info';
                infoContainer.innerHTML = `
                    <div style="display:flex;flex-wrap:wrap;justify-content:space-between;">
                        <div class="info-item" style="width:48%;margin-bottom:10px;">
                            <span style="font-weight:bold;">时间范围：</span>
                            <span style="color:#409EFF;">加载中...</span>
                        </div>
                        <div class="info-item" style="width:48%;margin-bottom:10px;">
                            <span style="font-weight:bold;">有效数据点：</span>
                            <span style="color:#409EFF;">加载中...</span>
                        </div>
                        <div class="info-item" style="width:48%;margin-bottom:10px;">
                            <span style="font-weight:bold;">平均值：</span>
                            <span style="color:#409EFF;">加载中...</span>
                        </div>
                        <div class="info-item" style="width:48%;margin-bottom:10px;">
                            <span style="font-weight:bold;">数据范围：</span>
                            <span style="color:#409EFF;">加载中...</span>
                        </div>
                    </div>
                `;
                infoContainer.style.cssText = 'margin-top:15px;padding:10px;background:#f8f8f8;border-radius:4px;';

                // 组装DOM
                modalContent.appendChild(titleBar);
                modalContent.appendChild(chartContainer);
                modalContent.appendChild(infoContainer);
                modalContainer.appendChild(modalContent);
                document.body.appendChild(modalContainer);

                console.warn('==== [DEBUG-28] 应急图表容器创建完成 ====');

                // 修改初始化逻辑以适应新的容器ID
                this.$nextTick(() => {
                    console.warn('==== [DEBUG-29] 应急图表初始化 ====');
                    // 调整initAndRenderChart方法以使用应急容器ID
                    const chartDom = document.getElementById('emergencyGroupRRIChart');
                    if (chartDom) {
                        if (this.groupChartInstance) {
                            this.groupChartInstance.dispose();
                        }
                        this.groupChartInstance = echarts.init(chartDom);
                        // 配置和渲染图表
                        this.initAndRenderChart('emergencyGroupRRIChart');
                    }
                });

                return true;
            } catch (error) {
                console.error('==== [ERROR] 创建应急图表容器失败 ====', error);
                return false;
            }
        },
        loadChartData(row) {
            console.log('========== 加载图表数据 ==========')
            this.chartLoading = true

            try {
                // 检查数据
                if (!row || !row.rriData) {
                    console.error('数据无效，无法加载图表')
                    this.chartData = []
                    this.validPoints = 0
                    this.avgRRI = 0
                    this.minRRI = 0
                    this.maxRRI = 0
                    this.chartLoading = false

                    if (this.chartInstance) {
                        this.chartInstance.setOption({
                            series: [{
                                data: []
                            }]
                        })
                    }
                    return
                }

                // 解析数据
                let rriData = row.rriData
                if (typeof rriData === 'string') {
                    try {
                        rriData = JSON.parse(rriData)
                    } catch (error) {
                        console.error('解析RRI数据失败:', error)
                        this.$modal.msgError('RRI数据格式错误')
                        this.chartLoading = false
                        return
                    }
                }

                // 确保数据是数组
                if (!Array.isArray(rriData)) {
                    console.error('RRI数据不是数组')
                    this.$modal.msgError('RRI数据格式不正确')
                    this.chartLoading = false
                    return
                }

                // 处理数据
                console.log(`原始数据长度: ${rriData.length}`)
                const processedData = this.processChartData(rriData)
                const validData = processedData.filter(item => item && item.length >= 2)

                // 计算统计信息
                this.chartData = validData
                this.validPoints = validData.length

                // 处理空数据情况
                if (validData.length === 0) {
                    console.log('没有有效的RRI数据')
                    this.avgRRI = 0
                    this.minRRI = 0
                    this.maxRRI = 0
                    this.chartLoading = false
                    return
                }

                // 计算统计量
                const rriValues = validData.map(item => item[1])
                this.minRRI = Math.min(...rriValues)
                this.maxRRI = Math.max(...rriValues)
                this.avgRRI = Math.round(rriValues.reduce((sum, val) => sum + val, 0) / rriValues.length)

                // 更新图表
                if (this.chartInstance) {
                    // 重要：设置Y轴范围，避免断言错误
                    const minY = Math.max(1, this.minRRI * 0.9)  // 避免0或负值
                    const maxY = Math.min(3000, this.maxRRI * 1.1) // 上限

                    this.chartInstance.setOption({
                        yAxis: {
                            min: minY,
                            max: maxY
                        },
                        series: [{
                            data: validData
                        }]
                    })

                    console.log('图表数据更新完成')
                } else {
                    console.error('图表实例不存在')
                }
            } catch (error) {
                console.error('处理RRI数据出错:', error)
                console.error('错误详情:', error.stack)
                this.$modal.msgError('处理RRI数据出错: ' + (error.message || '未知错误'))

                // 错误时显示空图表
                if (this.chartInstance) {
                    this.chartInstance.setOption({
                        series: [{
                            data: []
                        }]
                    })
                }
            } finally {
                this.chartLoading = false
            }
        },
        processChartData(rriData) {
            console.log('========== 处理图表数据 ==========');
            try {
                // 检查数据是否为空
                if (!rriData || !Array.isArray(rriData) || rriData.length === 0) {
                    console.warn('RRI数据为空或格式错误');
                    return [];
                }

                // 检查第一个元素的格式，确定数据结构
                const firstItem = rriData[0];
                let processedData = [];

                // 如果数据已经是二维数组格式 [[timestamp, rri, sqi], ...]
                if (Array.isArray(firstItem)) {
                    console.log('处理二维数组格式数据');

                    // 过滤掉无效的数据项
                    processedData = rriData.filter(item => {
                        // 检查数组长度
                        if (!item || item.length < 2) return false;

                        // 确保时间戳和RRI值有效
                        const timestamp = item[0];
                        const rri = item[1];

                        return timestamp &&
                            !isNaN(new Date(timestamp).getTime()) &&
                            rri !== undefined &&
                            rri !== null &&
                            !isNaN(rri) &&
                            isFinite(rri);
                    });
                }
                // 如果是对象数组格式 [{timestamp/time, rri/value, sqi/quality}, ...]
                else if (typeof firstItem === 'object' && firstItem !== null) {
                    console.log('处理对象数组格式数据');

                    processedData = rriData.map(item => {
                        if (!item) return null;

                        // 提取时间戳、RRI值和质量指数
                        const timestamp = item.timestamp || item.time;
                        const rri = item.rri || item.value;
                        const sqi = item.sqi || item.quality || 0;

                        // 验证时间戳和RRI值
                        if (timestamp &&
                            !isNaN(new Date(timestamp).getTime()) &&
                            rri !== undefined &&
                            rri !== null &&
                            !isNaN(rri) &&
                            isFinite(rri)) {
                            return [timestamp, rri, sqi];
                        }

                        return null;
                    }).filter(item => item !== null);
                }
                // 如果是简单的值数组，尝试结合时间戳构建数据
                else {
                    console.log('处理简单值数组格式数据');

                    // 生成时间序列（假设等间隔采样，1秒1个点）
                    const startTime = new Date();
                    startTime.setMinutes(startTime.getMinutes() - rriData.length / 60); // 向前推

                    processedData = rriData.map((value, index) => {
                        // 跳过无效值
                        if (value === undefined || value === null || isNaN(value) || !isFinite(value)) {
                            return null;
                        }

                        // 生成时间戳，每个点加1秒
                        const timestamp = new Date(startTime.getTime() + index * 1000);
                        return [timestamp.toISOString(), Number(value), 0];
                    }).filter(item => item !== null);
                }

                console.log(`原始数据点数: ${rriData.length}, 有效数据点数: ${processedData.length}`);

                // 如果有效数据太少，给出警告
                if (processedData.length < rriData.length * 0.5) {
                    console.warn(`数据质量较低，有效数据比例: ${(processedData.length / rriData.length * 100).toFixed(1)}%`);
                }

                // 返回处理后的数据
                return processedData;
            } catch (error) {
                console.error('处理图表数据出错:', error);
                return [];
            }
        }
    },
    mounted() {
        console.log('====== ContinuousRRI组件挂载 ======');
        console.log('this.$api:', this.$api);
        console.log('this.$api.medical:', this.$api.medical);
        console.log('this.$api.medical.crri:', this.$api.medical.crri);
        if (this.$api.medical.crri) {
            console.log('list类型:', typeof this.$api.medical.crri.list);
            console.log('getDetail类型:', typeof this.$api.medical.crri.getDetail);
        }

        // 添加图表容器到详情对话框
        this.$watch('currentRow', (newVal) => {
            if (newVal) {
                // 等待详情对话框渲染完成
                this.$nextTick(() => {
                    // 查找详情对话框，并添加图表
                    const dialogForm = document.querySelector('.el-dialog__body .el-form');
                    if (dialogForm) {
                        // 创建图表容器
                        const chartContainer = document.createElement('div');
                        chartContainer.style.marginTop = '20px';
                        chartContainer.innerHTML = `
                            <h3 style="margin-top: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;">RRI数据图表</h3>
                            <div id="detailRRIChart" style="width: 100%; height: 350px; margin-top: 15px;"></div>
                            <div class="chart-info" style="margin-top: 15px; padding: 10px; background: #f8f8f8; border-radius: 4px;">
                                <div style="display: flex; justify-content: space-around;">
                                    <div class="info-item">
                                        <span class="label" style="font-weight: bold;">有效数据点：</span>
                                        <span class="value" style="color: #409EFF;">${this.validPoints}个</span>
                                    </div>
                                    <div class="info-item">
                                        <span class="label" style="font-weight: bold;">平均值：</span>
                                        <span class="value" style="color: #409EFF;">${this.avgRRI}ms</span>
                                    </div>
                                    <div class="info-item">
                                        <span class="label" style="font-weight: bold;">数据范围：</span>
                                        <span class="value" style="color: #409EFF;">${this.minRRI}-${this.maxRRI}ms</span>
                                    </div>
                                </div>
                            </div>
                        `;

                        // 将图表容器添加到对话框中
                        const parentElement = dialogForm.parentElement;
                        parentElement.appendChild(chartContainer);

                        // 渲染图表
                        this.$nextTick(() => {
                            this.initDetailChart();
                            this.loadChartData(newVal);
                        });
                    }
                });
            }
        });
    }
}
</script>

<style scoped>
.chart-info {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f8f8;
    border-radius: 4px;
}

.info-item {
    display: flex;
    align-items: center;
}

.info-item .label {
    font-weight: bold;
    margin-right: 5px;
}

.info-item .value {
    color: #409EFF;
    font-size: 16px;
}

.no-data {
    margin: 30px 0;
}
</style>