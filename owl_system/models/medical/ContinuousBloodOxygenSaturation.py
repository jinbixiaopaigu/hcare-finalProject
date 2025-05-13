from datetime import datetime
from owl_system.models import db

class ContinuousBloodOxygenSaturation(db.Model):
    """连续血氧饱和度数据表"""
    __tablename__ = 'continuous_blood_oxygen_saturation'
    
    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    record_group_id = db.Column(db.String(255))
    upload_time = db.Column(db.DateTime)
    data_time = db.Column(db.DateTime)
    spo2_value = db.Column(db.Float)
    spo2_unit = db.Column(db.String(50))
    measurement_start_time = db.Column(db.DateTime)
    measurement_end_time = db.Column(db.DateTime)
    measurement_time = db.Column(db.DateTime)
    statistical_method = db.Column(db.String(255))
    user_notes = db.Column(db.Text)
    spo2_group_values = db.Column(db.Text)
    measurement_type = db.Column(db.String(255))
    external_id = db.Column(db.String(255))
    metadata_version = db.Column(db.Integer)
    spo2_min_value = db.Column(db.Float)
    spo2_min_unit = db.Column(db.String(50))
    spo2_min_time = db.Column(db.DateTime)
    spo2_max_value = db.Column(db.Float)
    spo2_max_unit = db.Column(db.String(50))
    spo2_max_time = db.Column(db.DateTime)
    spo2_avg_value = db.Column(db.Float)
    spo2_avg_unit = db.Column(db.String(50))
    spo2_measurement_count = db.Column(db.Integer)
    spo2_measurement_duration = db.Column(db.Integer)
    spo2_measurement_duration_unit = db.Column(db.String(50))
    spo2_measurement_status = db.Column(db.String(255))
    spo2_measurement_status_reason = db.Column(db.Text)

    def to_dict(self):
        try:
            return {
                'id': self.id,
                'user_id': self.user_id,
                'spo2_value': float(self.spo2_value) if self.spo2_value is not None else None,
                'spo2_unit': str(self.spo2_unit) if self.spo2_unit is not None else None,
                'data_time': self.data_time.strftime('%Y-%m-%d %H:%M:%S') if self.data_time else None,
                'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
                'record_group_id': str(self.record_group_id) if self.record_group_id else None
            }
        except Exception as e:
            import logging
            logging.error(f"to_dict转换失败: {str(e)}")
            return {
                'id': str(self.id) if self.id else None,
                'user_id': str(self.user_id) if self.user_id else None,
                'error': f"数据转换异常: {str(e)}"
            }