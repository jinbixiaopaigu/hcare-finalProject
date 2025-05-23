<template>
  <div class="app-container">
    <el-row :gutter="10">
      <el-col :span="8">
        <el-card style="height: calc(100vh - 125px)">
          <template #header>
            <Collection style="width: 1em; height: 1em; vertical-align: middle;" /> <span
              style="vertical-align: middle;">缓存列表</span>
            <el-button style="float: right; padding: 3px 0" link type="primary" icon="Refresh"
              @click="refreshCacheNames()"></el-button>
          </template>
          <el-table v-loading="loading" :data="cacheNames" :height="tableHeight" highlight-current-row
            @row-click="getCacheKeys" style="width: 100%">
            <el-table-column label="序号" width="60" type="index"></el-table-column>

            <el-table-column label="缓存名称" align="center" prop="cacheName" :show-overflow-tooltip="true"
              :formatter="nameFormatter"></el-table-column>

            <el-table-column label="备注" align="center" prop="remark" :show-overflow-tooltip="true" />
            <el-table-column label="操作" width="60" align="center" class-name="small-padding fixed-width">
              <template #default="scope">
                <el-button link type="primary" icon="Delete" @click="handleClearCacheName(scope.row)"></el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card style="height: calc(100vh - 125px)">
          <template #header>
            <Key style="width: 1em; height: 1em; vertical-align: middle;" /> <span
              style="vertical-align: middle;">键名列表</span>
            <el-button style="float: right; padding: 3px 0" link type="primary" icon="Refresh"
              @click="refreshCacheKeys()"></el-button>
          </template>
          <el-table v-loading="subLoading" :data="cacheKeys" :height="tableHeight" highlight-current-row
            @row-click="handleCacheValue" style="width: 100%">
            <el-table-column label="序号" width="60" type="index"></el-table-column>
            <el-table-column label="缓存键名" align="center" :show-overflow-tooltip="true" :formatter="keyFormatter">
            </el-table-column>
            <el-table-column label="操作" width="60" align="center" class-name="small-padding fixed-width">
              <template #default="scope">
                <el-button link type="primary" icon="Delete" @click="handleClearCacheKey(scope.row)"></el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card :bordered="false" style="height: calc(100vh - 125px)">
          <template #header>
            <Document style="width: 1em; height: 1em; vertical-align: middle;" /> <span
              style="vertical-align: middle;">缓存内容</span>
            <el-button style="float: right; padding: 3px 0" link type="primary" icon="Refresh"
              @click="handleClearCacheAll()">清理全部</el-button>
          </template>
          <el-form :model="cacheForm">
            <el-row :gutter="32">
              <el-col :offset="1" :span="22">
                <el-form-item label="缓存名称:" prop="cacheName">
                  <el-input v-model="cacheForm.cacheName" :readOnly="true" />
                </el-form-item>
              </el-col>
              <el-col :offset="1" :span="22">
                <el-form-item label="缓存键名:" prop="cacheKey">
                  <el-input v-model="cacheForm.cacheKey" :readOnly="true" />
                </el-form-item>
              </el-col>
              <el-col :offset="1" :span="22">
                <el-form-item label="缓存内容:" prop="cacheValue">
                  <el-input v-model="cacheForm.cacheValue" type="textarea" :rows="8" :readOnly="true" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="CacheList">
import { listCacheName, listCacheKey, getCacheValue, clearCacheName, clearCacheKey, clearCacheAll } from "@/api/monitor/cache";
import { computed } from 'vue';

const { proxy } = getCurrentInstance();
const isDevelopment = computed(() => import.meta.env.MODE === 'development');

const cacheNames = ref([]);
const cacheKeys = ref([]);
const cacheForm = ref({});
const loading = ref(true);
const subLoading = ref(false);
const nowCacheName = ref("");
const tableHeight = ref(window.innerHeight - 200);

/** 查询缓存名称列表 */
function getCacheNames() {
  loading.value = true;
  listCacheName().then(response => {
    const data = response?.data || {};

    // 转换数据结构为表格需要的格式
    cacheNames.value = [
      {
        cacheName: 'info',
        remark: 'Redis服务器信息'
      },
      {
        cacheName: 'dbSize',
        remark: `数据库大小: ${data.dbSize || 0}`
      },
      {
        cacheName: 'commandStats',
        remark: 'Redis命令统计信息'
      }
    ];

    // 如果数据为空，显示提示
    if (cacheNames.value.length === 0) {
      proxy.$modal.msgWarning("没有找到缓存数据");
    }
  }).catch(error => {
    proxy.$modal.msgError("获取缓存列表失败");
    console.error("获取缓存列表失败:", error);
    cacheNames.value = [];
  }).finally(() => {
    loading.value = false;
  });
}

/** 获取缓存备注 */
function getCacheRemark(name) {
  const remarks = {
    'info': '系统信息缓存',
    'dbSize': '数据库大小缓存',
    'commandStats': '命令统计缓存'
  };
  return remarks[name] || '系统缓存';
}

/** 刷新缓存名称列表 */
function refreshCacheNames() {
  getCacheNames();
  proxy.$modal.msgSuccess("刷新缓存列表成功");
}

/** 清理指定名称缓存 */
function handleClearCacheName(row) {
  clearCacheName(row.cacheName).then(response => {
    proxy.$modal.msgSuccess("清理缓存名称[" + row.cacheName + "]成功");
    getCacheKeys();
  });
}

/** 查询缓存键名列表 */
function getCacheKeys(row) {
  const cacheName = row !== undefined ? row.cacheName : nowCacheName.value;
  if (cacheName === "") {
    return;
  }
  subLoading.value = true;
  listCacheKey(cacheName).then(response => {
    // 处理不同类型的返回数据
    let keys = [];
    if (Array.isArray(response.data)) {
      keys = response.data;
    } else if (response.data && typeof response.data === 'object') {
      keys = Object.keys(response.data);
    }

    // 创建新的数组避免响应式问题
    const newCacheKeys = keys.map(item => {
      // 处理不同类型的键名数据
      const key = item?.cacheKey || item;
      const formattedItem = {
        cacheKey: key,
        keyValue: item?.keyValue || '',
        keyType: typeof key,
        original: item
      };
      // console.log('格式化后的键名项:', formattedItem);
      return formattedItem;
    });

    // 简化数据结构，保留cacheKey和keyValue字段
    const simplifiedKeys = newCacheKeys.map(item => ({
      cacheKey: item.cacheKey,
      keyValue: item.keyValue
    }));

    // 整体替换数组确保响应式更新
    cacheKeys.value = simplifiedKeys;
    // console.log('简化后的键名列表数据:', JSON.parse(JSON.stringify(cacheKeys.value)));

    nowCacheName.value = cacheName;
  }).catch(error => {
    proxy.$modal.msgError("获取键名列表失败");
    console.error("获取键名列表失败:", error);
    cacheKeys.value = [];
  }).finally(() => {
    subLoading.value = false;
  });
}

/** 刷新缓存键名列表 */
function refreshCacheKeys() {
  getCacheKeys();
  proxy.$modal.msgSuccess("刷新键名列表成功");
}

/** 清理指定键名缓存 */
function handleClearCacheKey(cacheKey) {
  clearCacheKey(cacheKey).then(response => {
    proxy.$modal.msgSuccess("清理缓存键名[" + cacheKey + "]成功");
    getCacheKeys();
  });
}

/** 列表前缀去除 */
function nameFormatter(row) {
  return row.cacheName.replace(":", "");
}

/** 键名格式化处理 */
function keyFormatter(row, column, cellValue, index) {
  // 从正确参数位置获取键名
  const key = row?.cacheKey || cellValue;
  if (!key) return '';

  // 确保处理字符串
  const keyStr = String(key);
  const cacheName = nowCacheName.value;

  // 1. 先去除缓存名称前缀
  let formattedKey = keyStr.replace(new RegExp(`^${cacheName}`), '');

  // 2. 处理键名中的键值部分（分隔符可能是":"或"="）
  const keyParts = formattedKey.split(/[:=]/);
  if (keyParts.length > 1) {
    formattedKey = keyParts[0].trim();
  }

  return formattedKey;
}

/** 查询缓存内容详细 */
function handleCacheValue(row) {
  subLoading.value = true;
  console.group('获取缓存内容');
  console.log('缓存名称:', nowCacheName.value);
  console.log('缓存键名:', row);

  // 优先使用keyValue作为缓存键，确保简单键名
  const cacheKey = row?.keyValue || row?.cacheKey || '';
  if (!cacheKey) {
    proxy.$modal.msgError("无效的缓存键名");
    subLoading.value = false;
    console.groupEnd();
    return;
  }

  // 只传递简单键名，去除特殊字符
  const simpleKey = String(cacheKey).replace(/[^\w]/g, '');
  if (!simpleKey) {
    proxy.$modal.msgError("无效的缓存键名格式");
    subLoading.value = false;
    console.groupEnd();
    return;
  }

  getCacheValue(nowCacheName.value, simpleKey).then(response => {
    console.log('API响应:', response);

    // 处理不同类型的缓存值
    let cacheValue = response.data?.cacheValue || response.data;

    // 如果是对象或数组，转换为格式化JSON字符串
    if (cacheValue && typeof cacheValue === 'object') {
      try {
        cacheValue = JSON.stringify(cacheValue, null, 2);
      } catch (e) {
        console.warn('JSON序列化失败:', e);
      }
    }

    // 更新表单数据
    cacheForm.value = {
      cacheName: nowCacheName.value,
      cacheKey: cacheKey,
      cacheValue: cacheValue
    };

    console.log('处理后内容数据:', cacheForm.value);
    proxy.$modal.msgSuccess("获取缓存内容成功");
  }).catch(error => {
    console.error('获取缓存内容失败:', error);
    proxy.$modal.msgError(`获取缓存内容失败: ${error.message || '未知错误'}`);

    // 清空表单显示错误状态
    cacheForm.value = {
      cacheName: nowCacheName.value,
      cacheKey: cacheKey,
      cacheValue: '获取缓存内容失败'
    };
  }).finally(() => {
    subLoading.value = false;
    console.groupEnd();
  });
}

/** 清理全部缓存 */
function handleClearCacheAll() {
  clearCacheAll().then(response => {
    proxy.$modal.msgSuccess("清理全部缓存成功");
  });
}

getCacheNames();
</script>