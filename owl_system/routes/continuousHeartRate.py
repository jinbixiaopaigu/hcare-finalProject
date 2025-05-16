from flask import Blueprint
from owl_system.modules.medical.controller.ContinuousHeartRateController import (
    list_continuous_heart_rate,
    get_continuous_heart_rate_detail,
    add_continuous_heart_rate,
    update_continuous_heart_rate,
    delete_continuous_heart_rate,
    sync_continuous_heart_rate
)
from owl_system.utils.log import log_debug

def register_routes(app):
    """注册连续心率路由"""
    # 创建蓝图
    chr_bp = Blueprint('medical_chr', __name__, url_prefix='/medical/chr')
    
    # 注册路由
    chr_bp.route('/list', methods=['GET', 'POST'], endpoint='chr_list')(list_continuous_heart_rate)
    chr_bp.route('/<string:id>', methods=['GET'], endpoint='chr_detail')(get_continuous_heart_rate_detail)
    chr_bp.route('', methods=['POST'], endpoint='chr_add')(add_continuous_heart_rate)
    chr_bp.route('', methods=['PUT'], endpoint='chr_update')(update_continuous_heart_rate)
    chr_bp.route('/<string:id>', methods=['DELETE'], endpoint='chr_delete')(delete_continuous_heart_rate)
    chr_bp.route('/sync', methods=['POST', 'OPTIONS'], endpoint='chr_sync')(sync_continuous_heart_rate)
    
    # 注册蓝图
    app.register_blueprint(chr_bp)
    log_debug('连续心率路由注册成功') 