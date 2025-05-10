from datetime import datetime
from owl_system.models import db

class BloodOxygenSaturation(db.Model):
    """血氧饱和度数据表"""
    __tablename__ = 'blood_oxygen_saturation'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    record_group_id = db.Column(db.String(36))
    upload_time = db.Column(db.DateTime, default=datetime.now)
    data_time = db.Column(db.DateTime, nullable=False)
    spo2_value = db.Column(db.Float, nullable=False)
    spo2_unit = db.Column(db.String(10), default='%')
    measurement_start_time = db.Column(db.DateTime)
    measurement_end_time = db.Column(db.DateTime)
    measurement_time = db.Column(db.Integer)
    statistical_method = db.Column(db.String(50))
    user_notes = db.Column(db.Text)
    spo2_group_values = db.Column(db.Text)
    measurement_type = db.Column(db.String(20))
    external_id = db.Column(db.String(100))
    metadata_version = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'record_group_id': self.record_group_id,
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
            'data_time': self.data_time.strftime('%Y-%m-%d %H:%M:%S') if self.data_time else None,
            'spo2_value': self.spo2_value,
            'spo2_unit': self.spo2_unit,
            'measurement_start_time': self.measurement_start_time.strftime('%Y-%m-%d %H:%M:%S') if self.measurement_start_time else None,
            'measurement_end_time': self.measurement_end_time.strftime('%Y-%m-%d %H:%M:%S') if self.measurement_end_time else None,
            'measurement_time': self.measurement_time,
            'statistical_method': self.statistical_method,
            'user_notes': self.user_notes,
            'spo2_group_values': self.spo2_group_values,
            'measurement_type': self.measurement_type,
            'external_id': self.external_id,
            'metadata_version': self.metadata_version
        }