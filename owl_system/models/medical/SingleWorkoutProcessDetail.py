from datetime import datetime
from owl_system.models import db

class SingleWorkoutProcessDetail(db.Model):
    """6分钟行走测试数据表"""
    __tablename__ = 'single_workout_process_detail'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    record_group_id = db.Column(db.String(36))
    upload_time = db.Column(db.DateTime, default=datetime.now)
    data_time = db.Column(db.DateTime, nullable=False)
    activity_name = db.Column(db.String(255))
    activity_type = db.Column(db.String(255))
    activity_intensity = db.Column(db.String(255))
    activity_duration = db.Column(db.String(255))
    activity_duration_unit = db.Column(db.String(32))
    activity_distance = db.Column(db.Float)
    activity_distance_unit = db.Column(db.String(32))
    activity_calories = db.Column(db.Float)
    activity_calories_unit = db.Column(db.String(32))
    activity_heart_rate_avg = db.Column(db.Float)
    activity_heart_rate_avg_unit = db.Column(db.String(32))
    activity_heart_rate_max = db.Column(db.Float)
    activity_heart_rate_max_unit = db.Column(db.String(32))
    activity_heart_rate_min = db.Column(db.Float)
    activity_heart_rate_min_unit = db.Column(db.String(32))
    activity_step_count = db.Column(db.Integer)
    activity_step_count_unit = db.Column(db.String(32))
    activity_speed_avg = db.Column(db.Float)
    activity_speed_avg_unit = db.Column(db.String(32))
    activity_speed_max = db.Column(db.Float)
    activity_speed_max_unit = db.Column(db.String(32))
    activity_speed_min = db.Column(db.Float)
    activity_speed_min_unit = db.Column(db.String(32))
    external_id = db.Column(db.String(255))
    metadata_version = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'record_group_id': self.record_group_id,
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
            'data_time': self.data_time.strftime('%Y-%m-%d %H:%M:%S') if self.data_time else None,
            'step_count': self.activity_step_count,
            'distance': self.activity_distance,
            'distance_unit': self.activity_distance_unit,
            'heart_rate': self.activity_heart_rate_avg,
            'speed': self.activity_speed_avg,
            'speed_unit': self.activity_speed_avg_unit,
            'step_frequency': None,
            'calories': self.activity_calories,
            'workout_type': self.activity_type,
            'workout_status': self.activity_intensity,
            'activity_name': self.activity_name,
            'activity_type': self.activity_type,
            'activity_intensity': self.activity_intensity,
            'activity_duration': self.activity_duration,
            'activity_duration_unit': self.activity_duration_unit,
            'activity_distance': self.activity_distance,
            'activity_distance_unit': self.activity_distance_unit,
            'activity_calories': self.activity_calories,
            'activity_calories_unit': self.activity_calories_unit,
            'activity_heart_rate_avg': self.activity_heart_rate_avg,
            'activity_heart_rate_avg_unit': self.activity_heart_rate_avg_unit,
            'activity_step_count': self.activity_step_count,
            'activity_step_count_unit': self.activity_step_count_unit,
            'activity_speed_avg': self.activity_speed_avg,
            'activity_speed_avg_unit': self.activity_speed_avg_unit,
            'external_id': self.external_id,
            'metadata_version': self.metadata_version
        } 