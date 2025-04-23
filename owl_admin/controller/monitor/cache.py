# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from flask import jsonify
from owl_common.descriptor.serializer import JsonSerializer
from owl_framework.domain.entity import RedisCache
from owl_framework.descriptor.permission import HasPerm, PreAuthorize
from owl_admin.ext import redis_cache
from ... import reg
import traceback


@reg.api.route('/monitor/cache',methods=['GET'])
@PreAuthorize(HasPerm("monitor:cache:list"))
@JsonSerializer()
def monitor_cache():
    '''
        获取缓存信息
    '''
    try:
        cache = RedisCache.from_connection(redis_cache)
        # 安全获取Redis信息
        cache_info = {}
        if hasattr(cache, 'info'):
            if isinstance(cache.info, dict):
                cache_info = cache.info
            elif callable(cache.info):
                cache_info = cache.info()
        
        # 转换为可序列化的字典格式
        cache_data = {
            'status': 'online',
            'info': str(cache_info) if cache_info else 'Redis info not available'
        }
        return jsonify({
            'code': 200,
            'msg': '操作成功',
            'data': cache_data
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'code': 500,
            'msg': f'获取缓存信息失败: {str(e)}',
            'data': None
        }), 500


@reg.api.route('/monitor/cache/keys/<cacheName>', methods=['GET'])
@PreAuthorize(HasPerm("monitor:cache:list"))
@JsonSerializer()
def get_cache_keys(cacheName):
    '''
        获取指定缓存的键列表
    '''
    try:
        cache = RedisCache.from_connection(redis_cache)
        if not hasattr(cache, 'keys'):
            return jsonify({
                'code': 500,
                'msg': 'Redis缓存操作不支持keys方法',
                'data': None
            }), 500
            
        # 处理特殊缓存名称
        if cacheName == "dbSize":
            # 获取数据库大小信息
            try:
                db_info = cache.info('keyspace')
                if isinstance(db_info, bytes):
                    db_info = db_info.decode('utf-8')
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': str(db_info)
                })
            except Exception as e:
                traceback.print_exc()
                return jsonify({
                    'code': 500,
                    'msg': f'获取数据库信息失败: {str(e)}',
                    'data': None
                }), 500
        elif cacheName == "commandStats":
            # 特殊处理命令统计
            try:
                stats = cache.info('commandstats')
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': stats
                })
            except Exception as e:
                traceback.print_exc()
                return jsonify({
                    'code': 500,
                    'msg': f'获取命令统计失败: {str(e)}',
                    'data': None
                }), 500
        else:
            # 通用键获取逻辑
            try:
                if hasattr(cache, 'keys'):
                    if callable(cache.keys):
                        keys = cache.keys(f"*{cacheName}*") if cacheName != "*" else cache.keys()
                    else:
                        keys = []
                else:
                    keys = []
                
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': [str(key) for key in keys] if keys else []
                })
            except Exception as e:
                traceback.print_exc()
                return jsonify({
                    'code': 500,
                    'msg': f'获取缓存键失败: {str(e)}',
                    'data': None
                }), 500
            
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'code': 500,
            'msg': f'获取缓存键失败: {str(e)}',
            'data': None
        }), 500