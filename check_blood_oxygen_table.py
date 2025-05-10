from owl_admin.app import create_app
from owl_admin.ext import db

app = create_app()

with app.app_context():
    # 检查表是否存在
    inspector = db.inspect(db.engine)
    if inspector.has_table('blood_oxygen_saturation'):
        # 获取表结构
        columns = inspector.get_columns('blood_oxygen_saturation')
        print('现有表结构:', [col['name'] for col in columns])
        
        # 模型定义的字段
        model_columns = [
            'id', 'user_id', 'record_group_id', 'upload_time', 'data_time',
            'spo2_value', 'spo2_unit', 'measurement_start_time',
            'measurement_end_time', 'measurement_time', 'statistical_method',
            'user_notes', 'spo2_group_values', 'measurement_type',
            'external_id', 'metadata_version'
        ]
        print('模型定义字段:', model_columns)
        
        # 找出缺失字段
        missing = set(model_columns) - {col['name'] for col in columns}
        print('缺失字段:', missing)
        
        # 生成添加字段的SQL
        if missing:
            print('\n修复SQL:')
            print('ALTER TABLE blood_oxygen_saturation')
            for i, field in enumerate(missing):
                suffix = ',' if i < len(missing)-1 else ';'
                if field == 'measurement_start_time':
                    print(f"ADD COLUMN {field} DATETIME{suffix}")
                elif field == 'measurement_end_time':
                    print(f"ADD COLUMN {field} DATETIME{suffix}")
                elif field == 'measurement_time':
                    print(f"ADD COLUMN {field} INT{suffix}")
                elif field == 'statistical_method':
                    print(f"ADD COLUMN {field} VARCHAR(50){suffix}")
                elif field == 'spo2_group_values':
                    print(f"ADD COLUMN {field} TEXT{suffix}")
                else:
                    print(f"ADD COLUMN {field} VARCHAR(255){suffix}")
    else:
        print('blood_oxygen_saturation表不存在，需要创建')