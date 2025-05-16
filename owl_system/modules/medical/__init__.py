from flask import Blueprint
from .controller.AtrialFibrillationController import (
    list_atrial_fibrillation, 
    get_atrial_fibrillation_detail
)
from .controller.BloodOxygenController import (
    list_blood_oxygen,
    get_blood_oxygen_detail,
    add_blood_oxygen,
    update_blood_oxygen,
    delete_blood_oxygen
)
from .controller.ContinuousBloodOxygenController import (
    list_continuous_blood_oxygen,
    get_continuous_blood_oxygen_detail,
    add_continuous_blood_oxygen,
    update_continuous_blood_oxygen,
    delete_continuous_blood_oxygen
)
from .controller.ContinuousBodyTemperatureController import (
    list_continuous_body_temperature,
    get_continuous_body_temperature_detail,
    add_continuous_body_temperature,
    update_continuous_body_temperature,
    delete_continuous_body_temperature
)

# 导入同步控制器
from owl_admin.controller.medical.atrialFibrillation import sync_atrial_fibrillation

def register_medical_module(app):
    """注册医疗模块"""
    print("开始注册医疗模块...")  # 调试日志
    
    try:
        # 房颤检测路由(使用唯一端点名称)
        af_bp = Blueprint('medical_af', __name__, url_prefix='/medical/af')
        af_bp.route('/list', methods=['GET'], endpoint='af_list')(list_atrial_fibrillation)
        af_bp.route('/<string:id>', methods=['GET'], endpoint='af_detail')(get_atrial_fibrillation_detail)
        # 添加同步路由
        af_bp.route('/sync', methods=['POST', 'OPTIONS'], endpoint='af_sync')(sync_atrial_fibrillation)
        
        # 血氧饱和度路由(使用唯一端点名称)
        bo_bp = Blueprint('medical_bo', __name__, url_prefix='/medical/bo')
        bo_bp.route('/list', methods=['GET'], endpoint='bo_list')(list_blood_oxygen)
        bo_bp.route('/<string:id>', methods=['GET'], endpoint='bo_detail')(get_blood_oxygen_detail)
        bo_bp.route('', methods=['POST'], endpoint='bo_add')(add_blood_oxygen)
        bo_bp.route('', methods=['PUT'], endpoint='bo_update')(update_blood_oxygen)
        bo_bp.route('/<string:id>', methods=['DELETE'], endpoint='bo_delete')(delete_blood_oxygen)
        
        # 连续血氧饱和度路由(使用唯一端点名称)
        cbo_bp = Blueprint('medical_cbo', __name__, url_prefix='/medical/cbo')
        cbo_bp.route('/list', methods=['GET', 'POST'], endpoint='cbo_list')(list_continuous_blood_oxygen)
        cbo_bp.route('/<string:id>', methods=['GET'], endpoint='cbo_detail')(get_continuous_blood_oxygen_detail)
        cbo_bp.route('', methods=['POST'], endpoint='cbo_add')(add_continuous_blood_oxygen)
        cbo_bp.route('', methods=['PUT'], endpoint='cbo_update')(update_continuous_blood_oxygen)
        cbo_bp.route('/<string:id>', methods=['DELETE'], endpoint='cbo_delete')(delete_continuous_blood_oxygen)

        cbt_bp = Blueprint('medical_cbt', __name__, url_prefix='/medical/cbt')
        cbt_bp.route('/list', methods=['GET', 'POST'], endpoint='cbt_list')(list_continuous_body_temperature)
        cbt_bp.route('/<string:id>', methods=['GET'], endpoint='cbt_detail')(get_continuous_body_temperature_detail)
        cbt_bp.route('', methods=['POST'], endpoint='cbt_add')(add_continuous_body_temperature)
        cbt_bp.route('', methods=['PUT'], endpoint='cbt_update')(update_continuous_body_temperature)
        cbt_bp.route('/<string:id>', methods=['DELETE'], endpoint='cbt_delete')(delete_continuous_body_temperature)
        # # 创建蓝图
        # af_bp = Blueprint('atrial_fibrillation', __name__, url_prefix='/medical/atrialFibrillation')
        # bo_bp = Blueprint('blood_oxygen', __name__, url_prefix='/medical/bloodOxygen')
        # cbo_bp = Blueprint('continuous_blood_oxygen', __name__, url_prefix='/medical/continuousBloodOxygen')
        # cbt_bp = Blueprint('continuous_body_temperature', __name__, url_prefix='/medical/continuousBodyTemperature')

        # # 注册路由
        # af_bp.add_url_rule('/list', view_func=list_atrial_fibrillation, methods=['GET'])
        # af_bp.add_url_rule('/<int:id>', view_func=get_atrial_fibrillation_detail, methods=['GET'])
        # af_bp.add_url_rule('', view_func=add_atrial_fibrillation, methods=['POST'])
        # af_bp.add_url_rule('', view_func=update_atrial_fibrillation, methods=['PUT'])
        # af_bp.add_url_rule('/<int:id>', view_func=delete_atrial_fibrillation, methods=['DELETE'])

        # bo_bp.add_url_rule('/list', view_func=list_blood_oxygen, methods=['GET'])
        # bo_bp.add_url_rule('/<int:id>', view_func=get_blood_oxygen_detail, methods=['GET'])
        # bo_bp.add_url_rule('', view_func=add_blood_oxygen, methods=['POST'])
        # bo_bp.add_url_rule('', view_func=update_blood_oxygen, methods=['PUT'])
        # bo_bp.add_url_rule('/<int:id>', view_func=delete_blood_oxygen, methods=['DELETE'])

        # cbo_bp.add_url_rule('/list', view_func=list_continuous_blood_oxygen, methods=['GET'])
        # cbo_bp.add_url_rule('/<int:id>', view_func=get_continuous_blood_oxygen_detail, methods=['GET'])
        # cbo_bp.add_url_rule('', view_func=add_continuous_blood_oxygen, methods=['POST'])
        # cbo_bp.add_url_rule('', view_func=update_continuous_blood_oxygen, methods=['PUT'])
        # cbo_bp.add_url_rule('/<int:id>', view_func=delete_continuous_blood_oxygen, methods=['DELETE'])

        # cbt_bp.add_url_rule('/list', view_func=list_continuous_body_temperature, methods=['GET'])
        # cbt_bp.add_url_rule('/<int:id>', view_func=get_continuous_body_temperature_detail, methods=['GET'])
        # cbt_bp.add_url_rule('', view_func=add_continuous_body_temperature, methods=['POST'])
        # cbt_bp.add_url_rule('', view_func=update_continuous_body_temperature, methods=['PUT'])
        # cbt_bp.add_url_rule('/<int:id>', view_func=delete_continuous_body_temperature, methods=['DELETE'])

        # 注册蓝图
        try:
            app.register_blueprint(af_bp)
            app.register_blueprint(bo_bp)
            app.register_blueprint(cbo_bp)
            app.register_blueprint(cbt_bp)
            print("医疗模块蓝图注册成功")
        except Exception as e:
            print(f"医疗模块蓝图注册失败: {str(e)}")
            raise
        
        print("医疗模块注册成功!")  # 调试日志
        print("注册的路由:")
        print(f"  /medical/af/list")
        print(f"  /medical/af/<id>")
        print(f"  /medical/af/sync") # 添加同步路由日志
        print(f"  /medical/af (POST)")
        print(f"  /medical/af (PUT)")
        print(f"  /medical/af/<id> (DELETE)")
        print(f"  /medical/bo/list")
        print(f"  /medical/bo/<id>")
        print(f"  /medical/bo (POST)")
        print(f"  /medical/bo (PUT)")
        print(f"  /medical/bo/<id> (DELETE)")
        print(f"  /medical/cbo/list")
        print(f"  /medical/cbo/<id>")
        print(f"  /medical/cbo (POST)")
        print(f"  /medical/cbo (PUT)")
        print(f"  /medical/cbo/<id> (DELETE)")
        
    except Exception as e:
        print(f"医疗模块注册失败: {str(e)}")  # 错误日志