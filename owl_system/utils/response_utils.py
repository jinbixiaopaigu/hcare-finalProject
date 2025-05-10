from flask import jsonify

def success(data=None, message="操作成功", code=200):
    """成功响应"""
    return jsonify({
        "code": code,
        "msg": message,
        "data": data
    })

def error(message="操作失败", code=500, data=None):
    """错误响应"""
    return jsonify({
        "code": code,
        "msg": message,
        "data": data
    }), code