from flask import Blueprint
from owl_admin.ext import decorators
from owl_system.modules.medical.controller.ContinuousRRIController import (
    list_continuous_rri,
    get_continuous_rri_detail,
    add_continuous_rri,
    update_continuous_rri,
    delete_continuous_rri,
    sync_continuous_rri,
    generate_rri_chart
)

login_required = decorators.login_required
permission_required = decorators.permission_required

# 创建医疗模块蓝图
bp = Blueprint('medical', __name__, url_prefix='/medical')

# 连续RRI数据管理
@bp.route('/crri/list', methods=['GET'])
@login_required
@permission_required('medical:continuousRRI:list')
def get_continuous_rri_list():
    return list_continuous_rri()

@bp.route('/crri/<id>', methods=['GET'])
@login_required
@permission_required('medical:continuousRRI:query')
def get_continuous_rri_info(id):
    return get_continuous_rri_detail(id)

@bp.route('/crri', methods=['POST'])
@login_required
@permission_required('medical:continuousRRI:add')
def add_continuous_rri_data():
    return add_continuous_rri()

@bp.route('/crri', methods=['PUT'])
@login_required
@permission_required('medical:continuousRRI:edit')
def update_continuous_rri_data():
    return update_continuous_rri()

@bp.route('/crri/<id>', methods=['DELETE'])
@login_required
@permission_required('medical:continuousRRI:remove')
def delete_continuous_rri_data(id):
    return delete_continuous_rri(id)

@bp.route('/crri/sync', methods=['POST'])
@login_required
@permission_required('medical:continuousRRI:sync')
def sync_continuous_rri_data():
    return sync_continuous_rri()

@bp.route('/crri/chart', methods=['GET'])
@login_required
@permission_required('medical:continuousRRI:query')
def get_continuous_rri_chart():
    return generate_rri_chart() 