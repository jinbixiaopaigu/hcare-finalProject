from datetime import datetime
from owl_admin.ext import db

class ContinuousHeartRate(db.Model):
    """
    连续心率数据模型
    """
    __tablename__ = 'continuousheartrate'

    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255))
    record_group_id = db.Column(db.String(255))
    upload_time = db.Column(db.DateTime)
    data_time = db.Column(db.DateTime)
    heart_rate_value = db.Column(db.Float)
    heart_rate_unit = db.Column(db.String(50))
    measurement_start_time = db.Column(db.DateTime)
    measurement_end_time = db.Column(db.DateTime)
    measurement_time = db.Column(db.DateTime)
    statistical_method = db.Column(db.String(255))
    user_notes = db.Column(db.Text)
    heart_rate_group_values = db.Column(db.Text)
    measurement_type = db.Column(db.String(255))
    external_id = db.Column(db.String(255))
    metadata_version = db.Column(db.Integer)
    heart_rate_min_value = db.Column(db.Float)
    heart_rate_min_unit = db.Column(db.String(50))
    heart_rate_min_time = db.Column(db.DateTime)
    heart_rate_max_value = db.Column(db.Float)
    heart_rate_max_unit = db.Column(db.String(50))
    heart_rate_max_time = db.Column(db.DateTime)
    heart_rate_avg_value = db.Column(db.Float)
    heart_rate_avg_unit = db.Column(db.String(50))
    heart_rate_measurement_count = db.Column(db.Integer)
    heart_rate_measurement_duration = db.Column(db.Integer)
    heart_rate_measurement_duration_unit = db.Column(db.String(50))
    heart_rate_measurement_status = db.Column(db.String(255))
    heart_rate_measurement_status_reason = db.Column(db.Text)

    def __repr__(self):
        return f'<ContinuousHeartRate {self.id}>'

    def to_dict(self):
        """转换为字典"""
        try:
            return {
                'id': self.id,
                'userId': self.user_id,
                'recordGroupId': self.record_group_id,
                'uploadTime': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
                'dataTime': self.data_time.strftime('%Y-%m-%d %H:%M:%S') if self.data_time else None,
                'heartRateValue': self.heart_rate_value,
                'heartRateUnit': self.heart_rate_unit,
                'measurementStartTime': self.measurement_start_time.strftime('%Y-%m-%d %H:%M:%S') if self.measurement_start_time else None,
                'measurementEndTime': self.measurement_end_time.strftime('%Y-%m-%d %H:%M:%S') if self.measurement_end_time else None,
                'measurementTime': self.measurement_time.strftime('%Y-%m-%d %H:%M:%S') if self.measurement_time else None,
                'statisticalMethod': self.statistical_method,
                'userNotes': self.user_notes,
                'heartRateGroupValues': self.heart_rate_group_values,
                'measurementType': self.measurement_type,
                'externalId': self.external_id,
                'metadataVersion': self.metadata_version,
                'heartRateMinValue': self.heart_rate_min_value,
                'heartRateMinUnit': self.heart_rate_min_unit,
                'heartRateMinTime': self.heart_rate_min_time.strftime('%Y-%m-%d %H:%M:%S') if self.heart_rate_min_time else None,
                'heartRateMaxValue': self.heart_rate_max_value,
                'heartRateMaxUnit': self.heart_rate_max_unit,
                'heartRateMaxTime': self.heart_rate_max_time.strftime('%Y-%m-%d %H:%M:%S') if self.heart_rate_max_time else None,
                'heartRateAvgValue': self.heart_rate_avg_value,
                'heartRateAvgUnit': self.heart_rate_avg_unit,
                'heartRateMeasurementCount': self.heart_rate_measurement_count,
                'heartRateMeasurementDuration': self.heart_rate_measurement_duration,
                'heartRateMeasurementDurationUnit': self.heart_rate_measurement_duration_unit,
                'heartRateMeasurementStatus': self.heart_rate_measurement_status,
                'heartRateMeasurementStatusReason': self.heart_rate_measurement_status_reason
            }
        except Exception as e:
            import logging
            logging.error(f"to_dict转换失败: {str(e)}")
            return {
                'id': str(self.id) if self.id else None,
                'userId': str(self.user_id) if self.user_id else None,
                'error': f"数据转换异常: {str(e)}"
            }

    @classmethod
    def get_by_user_id(cls, user_id):
        """根据用户ID获取记录"""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_time_range(cls, start_time, end_time):
        """根据时间范围获取记录"""
        return cls.query.filter(cls.data_time.between(start_time, end_time)).all() 