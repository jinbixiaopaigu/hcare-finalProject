import logging
import sys
from owl_system.data_sync.synchronizer import DataSynchronizer

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('test_bo_sync')

def main():
    """测试血氧饱和度同步功能"""
    logger.info("开始测试血氧饱和度同步...")
    
    # 初始化同步器
    synchronizer = DataSynchronizer()
    
    try:
        # 同步血氧饱和度表
        table_key = 'blood_oxygen_saturation'
        inserted, updated = synchronizer.synchronize_table(table_key)
        
        logger.info(f"同步完成: 新增 {inserted} 条记录，更新 {updated} 条记录")
    except Exception as e:
        logger.error(f"同步测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭连接
        synchronizer.close()

if __name__ == "__main__":
    main() 