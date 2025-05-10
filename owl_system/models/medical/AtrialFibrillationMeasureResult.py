from datetime import datetime
from owl_system.models import db

class AtrialFibrillationMeasureResult(db.Model):
    """房颤检测结果表"""
    __tablename__ = 'atrial_fibrillation_measure_result'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    group_id = db.Column(db.String(36))
    upload_time = db.Column(db.DateTime, default=datetime.now)
    data_time = db.Column(db.DateTime)
    af_result = db.Column(db.String(50))
    risk_level = db.Column(db.String(20))
    external_id = db.Column(db.String(100))
    metadata_version = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
            'data_time': self.data_time.strftime('%Y-%m-%d %H:%M:%S') if self.data_time else None,
            'af_result': self.af_result,
            'risk_level': self.risk_level,
            'external_id': self.external_id,
            'metadata_version': self.metadata_version
        }