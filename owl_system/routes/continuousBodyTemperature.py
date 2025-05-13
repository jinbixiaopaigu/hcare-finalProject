from flask import Blueprint
from owl_system.controllers.BaseController import BaseController
from owl_system.models.medical import ContinuousBodyTemperature
from owl_system.controllers.config.continuousBodyTemperature import CONTINUOUS_BODY_TEMPERATURE_CONFIG
from owl_system.utils.logger import get_logger

logger = get_logger(__name__)

# 创建蓝图
continuous_body_temperature_bp = Blueprint('continuous_body_temperature', __name__, url_prefix='/medical/continuousBodyTemperature')

# 初始化控制器
controller = BaseController(
    model=ContinuousBodyTemperature,
    config=CONTINUOUS_BODY_TEMPERATURE_CONFIG
)

@continuous_body_temperature_bp.route('/list', methods=['GET'])
def list_items():
    logger.debug('Listing continuous body temperature records')
    return controller.list()

@continuous_body_temperature_bp.route('/<int:id>', methods=['GET'])
def get_item(id):
    logger.debug(f'Getting continuous body temperature record with id: {id}')
    return controller.get_detail(id)

@continuous_body_temperature_bp.route('', methods=['POST'])
def add_item():
    logger.debug('Adding new continuous body temperature record')
    return controller.add()

@continuous_body_temperature_bp.route('/<int:id>', methods=['PUT'])
def update_item(id):
    logger.debug(f'Updating continuous body temperature record with id: {id}')
    return controller.update(id)

@continuous_body_temperature_bp.route('/<int:id>', methods=['DELETE'])
def delete_item(id):
    logger.debug(f'Deleting continuous body temperature record with id: {id}')
    return controller.delete(id)

@continuous_body_temperature_bp.route('/batch', methods=['DELETE'])
def batch_delete_items():
    logger.debug('Batch deleting continuous body temperature records')
    # 注意：需要在前端API中实现批量删除逻辑
    return controller.batch_delete()

# 导出路由蓝图
def get_blueprint():
    return continuous_body_temperature_bp