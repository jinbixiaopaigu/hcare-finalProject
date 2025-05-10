from flask import Blueprint
from owl_system.controllers.medical.AtrialFibrillationController import (
    list_atrial_fibrillation, 
    get_atrial_fibrillation_detail
)
from owl_system.controllers.medical.BloodOxygenController import (
    list_blood_oxygen,
    get_blood_oxygen_detail,
    add_blood_oxygen,
    update_blood_oxygen,
    delete_blood_oxygen
)

def register_medical_module(app):
    """注册医疗模块"""
    print("开始注册医疗模块...")  # 调试日志
    
    try:
        # 房颤检测路由(仅注册已导入的方法)
        af_bp = Blueprint('af', __name__, url_prefix='/medical/af')
        af_bp.route('/list', methods=['GET'])(list_atrial_fibrillation)
        af_bp.route('/<string:id>', methods=['GET'])(get_atrial_fibrillation_detail)
        
        # 血氧饱和度路由(完整注册)
        bo_bp = Blueprint('bo', __name__, url_prefix='/medical/bo')
        bo_bp.route('/list', methods=['GET'])(list_blood_oxygen)
        bo_bp.route('/<string:id>', methods=['GET'])(get_blood_oxygen_detail)
        bo_bp.route('', methods=['POST'])(add_blood_oxygen)
        bo_bp.route('', methods=['PUT'])(update_blood_oxygen)
        bo_bp.route('/<string:id>', methods=['DELETE'])(delete_blood_oxygen)
        
        app.register_blueprint(af_bp)
        app.register_blueprint(bo_bp)
        
        print("医疗模块注册成功!")  # 调试日志
        print("注册的路由:")
        print(f"  /medical/af/list")
        print(f"  /medical/af/<id>")
        print(f"  /medical/af (POST)")
        print(f"  /medical/af (PUT)")
        print(f"  /medical/af/<id> (DELETE)")
        print(f"  /medical/bo/list")
        print(f"  /medical/bo/<id>")
        print(f"  /medical/bo (POST)")
        print(f"  /medical/bo (PUT)")
        print(f"  /medical/bo/<id> (DELETE)")
        
    except Exception as e:
        print(f"医疗模块注册失败: {str(e)}")  # 错误日志