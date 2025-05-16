from datetime import datetime
from owl_system.models import db

class ContinuousBodyTemperature(db.Model):
    """
    持续体温数据模型
    """
    __tablename__ = 'continuous_body_temperature'

    id = db.Column(db.String(64), primary_key=True, comment='主键ID')
    user_id = db.Column(db.String(32), nullable=True, comment='用户ID')
    record_group_id = db.Column(db.String(32), comment='记录分组ID')
    upload_time = db.Column(db.DateTime, comment='上传时间')
    data_time = db.Column(db.DateTime, comment='数据时间')
    measurement_part = db.Column(db.String(20), comment='测量部位')
    body_temperature = db.Column(db.DECIMAL(4,1), comment='体温')
    body_temperature_unit = db.Column(db.String(5), comment='体温单位')
    skin_temperature = db.Column(db.DECIMAL(4,1), comment='皮肤温度')
    skin_temperature_unit = db.Column(db.String(5), comment='皮肤温度单位')
    board_temperature = db.Column(db.DECIMAL(4,1), comment='板温度')
    board_temperature_unit = db.Column(db.String(5), comment='板温度单位')
    ambient_temperature = db.Column(db.DECIMAL(4,1), comment='环境温度')
    ambient_temperature_unit = db.Column(db.String(5), comment='环境温度单位')
    confidence = db.Column(db.DECIMAL(3,1), comment='置信度')
    external_id = db.Column(db.String(20), comment='外部ID')
    metadata_version = db.Column(db.Integer, comment='元数据版本')

    def __repr__(self):
        return f'<ContinuousBodyTemperature {self.id}>'

    def to_dict(self):
        """转换为字典"""
        try:
            return {
                'id': self.id,
                'user_id': self.user_id,
                'body_temperature': float(self.body_temperature) if self.body_temperature is not None else None,
                'body_temperature_unit': self.body_temperature_unit,
                'skin_temperature': float(self.skin_temperature) if self.skin_temperature is not None else None,
                'skin_temperature_unit': self.skin_temperature_unit,
                'ambient_temperature': float(self.ambient_temperature) if self.ambient_temperature is not None else None,
                'ambient_temperature_unit': self.ambient_temperature_unit,
                'measurement_part': self.measurement_part,
                'confidence': float(self.confidence) if self.confidence is not None else None,
                'data_time': self.data_time.strftime('%Y-%m-%d %H:%M:%S') if self.data_time else None,
                'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
                'record_group_id': self.record_group_id,
                'external_id': self.external_id,
                'metadata_version': self.metadata_version
            }
        except Exception as e:
            import logging
            logging.error(f"to_dict转换失败: {str(e)}")
            return {
                'id': str(self.id) if self.id else None,
                'user_id': str(self.user_id) if self.user_id else None,
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