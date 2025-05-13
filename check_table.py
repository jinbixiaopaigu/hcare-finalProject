from owl_admin.app import create_app
from owl_system.models import db
from owl_system.models.medical.ContinuousBloodOxygenSaturation import ContinuousBloodOxygenSaturation

app = create_app()

with app.app_context():
    # 检查表是否存在
    inspector = db.inspect(db.engine)
    if not inspector.has_table(ContinuousBloodOxygenSaturation.__tablename__):
        print(f"表 {ContinuousBloodOxygenSaturation.__tablename__} 不存在")
    else:
        # 获取表结构
        columns = inspector.get_columns(ContinuousBloodOxygenSaturation.__tablename__)
        print(f"表 {ContinuousBloodOxygenSaturation.__tablename__} 的列:")
        for col in columns:
            print(f"- {col['name']}: {col['type']}")