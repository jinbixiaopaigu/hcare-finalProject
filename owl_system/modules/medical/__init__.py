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
    delete_continuous_body_temperature,
    sync_continuous_body_temperature
)
from .controller.ContinuousHeartRateController import (
    list_continuous_heart_rate,
    get_continuous_heart_rate_detail,
    add_continuous_heart_rate,
    update_continuous_heart_rate,
    delete_continuous_heart_rate,
    sync_continuous_heart_rate
)
from .controller.ContinuousRRIController import (
    list_continuous_rri,
    get_continuous_rri_detail,
    add_continuous_rri,
    update_continuous_rri,
    delete_continuous_rri,
    sync_continuous_rri,
    generate_rri_chart
)
from .controller.SingleWorkoutProcessDetailController import (
    list_workout_detail,
    get_workout_detail,
    add_workout_detail,
    update_workout_detail,
    delete_workout_detail
)

# 导入同步控制器
from owl_admin.controller.medical.atrialFibrillation import sync_atrial_fibrillation
from owl_admin.controller.medical.bloodOxygen import sync_blood_oxygen
from owl_admin.controller.medical.continuousBloodOxygen import sync_continuous_blood_oxygen
from owl_admin.controller.medical.singleWorkoutDetail import sync

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
        # 添加同步路由
        bo_bp.route('/sync', methods=['POST', 'OPTIONS'], endpoint='bo_sync')(sync_blood_oxygen)
        
        # 连续血氧饱和度路由(使用唯一端点名称)
        cbo_bp = Blueprint('medical_cbo', __name__, url_prefix='/medical/cbo')
        cbo_bp.route('/list', methods=['GET', 'POST'], endpoint='cbo_list')(list_continuous_blood_oxygen)
        cbo_bp.route('/<string:id>', methods=['GET'], endpoint='cbo_detail')(get_continuous_blood_oxygen_detail)
        cbo_bp.route('', methods=['POST'], endpoint='cbo_add')(add_continuous_blood_oxygen)
        cbo_bp.route('', methods=['PUT'], endpoint='cbo_update')(update_continuous_blood_oxygen)
        cbo_bp.route('/<string:id>', methods=['DELETE'], endpoint='cbo_delete')(delete_continuous_blood_oxygen)
        # 添加同步路由
        cbo_bp.route('/sync', methods=['POST', 'OPTIONS'], endpoint='cbo_sync')(sync_continuous_blood_oxygen)

        cbt_bp = Blueprint('medical_cbt', __name__, url_prefix='/medical/cbt')
        cbt_bp.route('/list', methods=['GET', 'POST'], endpoint='cbt_list')(list_continuous_body_temperature)
        cbt_bp.route('/<string:id>', methods=['GET'], endpoint='cbt_detail')(get_continuous_body_temperature_detail)
        cbt_bp.route('', methods=['POST'], endpoint='cbt_add')(add_continuous_body_temperature)
        cbt_bp.route('', methods=['PUT'], endpoint='cbt_update')(update_continuous_body_temperature)
        cbt_bp.route('/<string:id>', methods=['DELETE'], endpoint='cbt_delete')(delete_continuous_body_temperature)
        # 添加同步路由
        cbt_bp.route('/sync', methods=['POST', 'OPTIONS'], endpoint='cbt_sync')(sync_continuous_body_temperature)

        # 连续心率路由
        chr_bp = Blueprint('medical_chr', __name__, url_prefix='/medical/chr')
        chr_bp.route('/list', methods=['GET', 'POST'], endpoint='chr_list')(list_continuous_heart_rate)
        chr_bp.route('/<string:id>', methods=['GET'], endpoint='chr_detail')(get_continuous_heart_rate_detail)
        chr_bp.route('', methods=['POST'], endpoint='chr_add')(add_continuous_heart_rate)
        chr_bp.route('', methods=['PUT'], endpoint='chr_update')(update_continuous_heart_rate)
        chr_bp.route('/<string:id>', methods=['DELETE'], endpoint='chr_delete')(delete_continuous_heart_rate)
        # 添加同步路由
        chr_bp.route('/sync', methods=['POST', 'OPTIONS'], endpoint='chr_sync')(sync_continuous_heart_rate)

        # 连续RRI数据路由
        crri_bp = Blueprint('medical_crri', __name__, url_prefix='/medical/crri')
        crri_bp.route('/list', methods=['GET'], endpoint='crri_list')(list_continuous_rri)
        crri_bp.route('/<string:id>', methods=['GET'], endpoint='crri_detail')(get_continuous_rri_detail)
        crri_bp.route('', methods=['POST'], endpoint='crri_add')(add_continuous_rri)
        crri_bp.route('', methods=['PUT'], endpoint='crri_update')(update_continuous_rri)
        crri_bp.route('/<string:id>', methods=['DELETE'], endpoint='crri_delete')(delete_continuous_rri)
        crri_bp.route('/sync', methods=['POST'], endpoint='crri_sync')(sync_continuous_rri)
        crri_bp.route('/chart', methods=['GET'], endpoint='crri_chart')(generate_rri_chart)
        
        # 6分钟行走测试数据路由
        swd_bp = Blueprint('medical_swd', __name__, url_prefix='/medical/swd')
        swd_bp.route('/list', methods=['GET'], endpoint='swd_list')(list_workout_detail)
        swd_bp.route('/<string:id>', methods=['GET'], endpoint='swd_detail')(get_workout_detail)
        swd_bp.route('', methods=['POST'], endpoint='swd_add')(add_workout_detail)
        swd_bp.route('', methods=['PUT'], endpoint='swd_update')(update_workout_detail)
        swd_bp.route('/<string:id>', methods=['DELETE'], endpoint='swd_delete')(delete_workout_detail)
        swd_bp.route('/sync', methods=['POST', 'OPTIONS'], endpoint='swd_sync')(sync)

        # 注册蓝图
        try:
            app.register_blueprint(af_bp)
            app.register_blueprint(bo_bp)
            app.register_blueprint(cbo_bp)
            app.register_blueprint(cbt_bp)
            app.register_blueprint(chr_bp)
            app.register_blueprint(crri_bp)  # 注册连续RRI数据蓝图
            app.register_blueprint(swd_bp)   # 注册6分钟行走测试数据蓝图
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
        print(f"  /medical/bo/sync") # 添加同步路由日志
        print(f"  /medical/bo (POST)")
        print(f"  /medical/bo (PUT)")
        print(f"  /medical/bo/<id> (DELETE)")
        print(f"  /medical/cbo/list")
        print(f"  /medical/cbo/<id>")
        print(f"  /medical/cbo/sync") # 添加连续血氧同步路由日志
        print(f"  /medical/cbo (POST)")
        print(f"  /medical/cbo (PUT)")
        print(f"  /medical/cbo/<id> (DELETE)")
        print(f"  /medical/cbt/list")
        print(f"  /medical/cbt/<id>")
        print(f"  /medical/cbt/sync")  # 添加持续体温同步路由日志
        print(f"  /medical/cbt (POST)")
        print(f"  /medical/cbt (PUT)")
        print(f"  /medical/cbt/<id> (DELETE)")
        print(f"  /medical/chr/list")
        print(f"  /medical/chr/<id>")
        print(f"  /medical/chr/sync")
        print(f"  /medical/chr (POST)")
        print(f"  /medical/chr (PUT)")
        print(f"  /medical/chr/<id> (DELETE)")
        print(f"  /medical/crri/list")
        print(f"  /medical/crri/<id>")
        print(f"  /medical/crri/sync")
        print(f"  /medical/crri/chart")
        print(f"  /medical/crri (POST)")
        print(f"  /medical/crri (PUT)")
        print(f"  /medical/crri/<id> (DELETE)")
        print(f"  /medical/swd/list")  # 添加6分钟行走测试路由日志
        print(f"  /medical/swd/<id>")
        print(f"  /medical/swd/sync")
        print(f"  /medical/swd (POST)")
        print(f"  /medical/swd (PUT)")
        print(f"  /medical/swd/<id> (DELETE)")
        
    except Exception as e:
        print(f"医疗模块注册失败: {str(e)}")  # 错误日志