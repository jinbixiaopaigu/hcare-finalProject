from datetime import datetime
from owl_system.models import db

class ContinuousBodyTemperature(db.Model):
    """
    持续体温数据模型
    """
    __tablename__ = 'continuous_body_temperature'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    user_id = db.Column(db.String(64), nullable=False, comment='用户ID')
    record_group_id = db.Column(db.String(64), comment='记录分组ID')
    upload_time = db.Column(db.DateTime, comment='上传时间')
    data_time = db.Column(db.DateTime, nullable=False, comment='数据时间')
    measurement_part = db.Column(db.String(50), nullable=False, comment='测量部位')
    body_temperature = db.Column(db.Float, nullable=False, comment='体温')
    body_temperature_unit = db.Column(db.String(10), default='℃', comment='体温单位')
    skin_temperature = db.Column(db.Float, comment='皮肤温度')
    skin_temperature_unit = db.Column(db.String(10), default='℃', comment='皮肤温度单位')
    board_temperature = db.Column(db.Float, comment='主板温度')
    board_temperature_unit = db.Column(db.String(10), default='℃', comment='主板温度单位')
    ambient_temperature = db.Column(db.Float, comment='环境温度')
    ambient_temperature_unit = db.Column(db.String(10), default='℃', comment='环境温度单位')
    confidence = db.Column(db.Float, comment='置信度')
    external_id = db.Column(db.String(64), comment='外部ID')
    metadata_version = db.Column(db.String(20), comment='元数据版本')

    def __repr__(self):
        return f'<ContinuousBodyTemperature {self.id}>'

    @classmethod
    def get_by_user_id(cls, user_id):
        """根据用户ID获取记录"""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_time_range(cls, start_time, end_time):
        """根据时间范围获取记录"""
        return cls.query.filter(cls.data_time.between(start_time, end_time)).all()