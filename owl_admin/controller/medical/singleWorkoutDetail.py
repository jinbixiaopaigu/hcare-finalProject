from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from owl_system.modules.medical.controller.SingleWorkoutProcessDetailController import (
    list_workout_detail,
    get_workout_detail,
    add_workout_detail,
    update_workout_detail,
    delete_workout_detail
)
from owl_system.data_sync.sync_service import sync_data_by_model_name

bp = Blueprint('singleWorkoutDetail', __name__, url_prefix='/medical/swd')

@bp.route('/list', methods=['GET'])
@jwt_required()
def get_list():
    """获取6分钟行走测试数据列表"""
    return list_workout_detail()

@bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_detail(id):
    """获取6分钟行走测试数据详情"""
    return get_workout_detail(id)

@bp.route('', methods=['POST'])
@jwt_required()
def add():
    """新增6分钟行走测试数据"""
    return add_workout_detail()

@bp.route('', methods=['PUT'])
@jwt_required()
def update():
    """更新6分钟行走测试数据"""
    return update_workout_detail()

@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """删除6分钟行走测试数据"""
    return delete_workout_detail(id)

@bp.route('/sync', methods=['POST'])
@jwt_required()
def sync():
    """同步6分钟行走测试数据"""
    result = sync_data_by_model_name("SingleWorkoutProcessDetail")
    return result 