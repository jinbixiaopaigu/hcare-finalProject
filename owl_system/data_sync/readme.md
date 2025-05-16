# 华为Research数据同步模块

该模块用于将华为Research平台的研究数据同步到MySQL数据库中。

## 功能特点

- 支持多表同步，可配置不同的表映射关系
- 支持增量同步，避免重复同步数据
- 支持自动字段映射，可处理不同命名风格
- 支持定时任务，定期自动同步数据
- 提供命令行工具，方便手动操作

## 配置说明

### 配置文件

配置文件为项目根目录下的 `config.ini`，包含以下几个部分：

```ini
[credentials]
access_key = your_access_key
secret_key = your_secret_key

[database]
host = localhost
port = 3306
user = root
password = your_password
db = hcare-final

[sync]
batch_size = 1000
sync_interval = 30  ; 同步间隔（分钟）
```

### 表映射配置

表映射配置在 `config.py` 中的 `SyncConfig.init_table_mappings` 方法中定义，可以根据需要添加更多表的映射关系。

例如：

```python
self.tables['atrial_fibrillation_measure_result'] = TableMapping(
    research_table_id='t_mnhqsfbc_atrialfibrillationmeasureresult_system',
    mysql_table_name='atrial_fibrillation_measure_result',
    field_mappings={
        "id": "id",
        "healthid": "user_id",
        "recordgroupid": "group_id",  
        "uploadtime": "upload_time",
        "recordtime": "data_time",
        "atrialfibrillationdetectresult": "af_result",
        "atrialfibrillationrisklevel": "risk_level",
        "externalid": "external_id",
        "metadataversion": "metadata_version"
    }
)
```

## 使用方法

### 命令行工具

模块提供了命令行工具，可以通过以下命令使用：

```bash
# 查看命令帮助
python -m owl_system.data_sync --help

# 列出所有可同步的表
python -m owl_system.data_sync list

# 比较表结构
python -m owl_system.data_sync compare atrial_fibrillation_measure_result

# 同步指定表
python -m owl_system.data_sync sync atrial_fibrillation_measure_result

# 同步所有表
python -m owl_system.data_sync sync-all

# 启动定时同步任务
python -m owl_system.data_sync scheduler
```

### 作为库使用

也可以在其他代码中导入并使用该模块：

```python
from owl_system.data_sync import SyncConfig, DataSynchronizer

# 初始化同步器
synchronizer = DataSynchronizer()

# 同步单个表
inserted, updated = synchronizer.synchronize_table('atrial_fibrillation_measure_result')
print(f"同步完成：插入 {inserted} 条记录，更新 {updated} 条记录")

# 同步所有表
results = synchronizer.synchronize_all()
```

### 定时任务

可以使用系统定时任务框架自动执行同步：

```python
from owl_apscheduler.task.research_sync_task import research_data_sync_task

# 立即执行同步任务
research_data_sync_task()
```

## 开发指南

### 添加新表

如果需要添加新的表进行同步，需要按照以下步骤操作：

1. 在 `config.py` 的 `init_table_mappings` 方法中添加新表的映射关系
2. 确认 MySQL 数据库中已创建对应的表结构
3. 使用命令行工具比较表结构，确保字段映射正确

例如：

```python
self.tables['continuousheartrate'] = TableMapping(
    research_table_id='t_mnhqsfbc_continuousheartrate_system',
    mysql_table_name='continuousheartrate',
    field_mappings={
        "id": "id",
        "healthid": "user_id",
        "recordgroupid": "record_group_id",
        "uploadtime": "upload_time",
        "recordtime": "data_time",
        # 添加其他字段映射...
    }
)
```

### 调试建议

1. 首先使用 `compare` 命令查看表结构和字段映射情况
2. 然后使用 `sync` 命令同步单个表，观察日志输出
3. 解决问题后，再使用 `sync-all` 或定时任务同步所有表

## 常见问题

### 1. 无法连接到华为Research

- 检查 `config.ini` 中的 `access_key` 和 `secret_key` 是否正确
- 检查网络连接是否正常

### 2. 无法连接到MySQL数据库

- 检查 `config.ini` 中的数据库配置是否正确
- 确认MySQL服务是否启动
- 检查用户权限是否足够

### 3. 字段映射错误

- 使用 `compare` 命令检查字段映射
- 修改 `config.py` 中的 `field_mappings` 配置 