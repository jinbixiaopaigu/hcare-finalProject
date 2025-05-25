from datetime import datetime
from owl_admin.ext import db

class ECG(db.Model):
    """ECG数据模型"""
    __tablename__ = 'ecg'

    id = db.Column(db.String(36), primary_key=True, comment='主键ID')
    user_id = db.Column(db.String(36), nullable=False, comment='用户ID')
    record_group_id = db.Column(db.String(36), comment='记录分组ID')
    upload_time = db.Column(db.DateTime, nullable=False, comment='上传时间')
    data_time = db.Column(db.DateTime, nullable=False, comment='数据时间')
    ecg_path = db.Column(db.String(255), nullable=False, comment='ECG数据路径')
    external_id = db.Column(db.Integer, nullable=False, comment='外部ID')
    metadata_version = db.Column(db.Integer, nullable=False, comment='元数据版本')

    def __repr__(self):
        return f'<ECG {self.id}>'

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'userId': self.user_id,
            'recordGroupId': self.record_group_id,
            'uploadTime': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
            'dataTime': self.data_time.strftime('%Y-%m-%d %H:%M:%S') if self.data_time else None,
            'ecgPath': self.ecg_path,
            'externalId': self.external_id,
            'metadataVersion': self.metadata_version
        } 