# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from flask import jsonify
import logging
from owl_common.descriptor.serializer import JsonSerializer
from owl_framework.descriptor.permission import HasPerm, PreAuthorize
from owl_admin.ext import redis_cache
from ... import reg
import traceback

logger = logging.getLogger(__name__)


@reg.api.route('/monitor/cache',methods=['GET'])
@PreAuthorize(HasPerm("monitor:cache:list"))
@JsonSerializer()
def monitor_cache():
    '''
        获取缓存信息
    '''
    try:
        logger.info("正在获取Redis缓存信息...")
        
        # 获取基本Redis信息
        try:
            info = redis_cache.info()
            logger.info(f"获取到的Redis信息: {info}")
            
            # 处理不同类型返回值
            if isinstance(info, bytes):
                info = info.decode('utf-8')
            elif isinstance(info, dict):
                info = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                        v.decode('utf-8') if isinstance(v, bytes) else v
                        for k, v in info.items()}
            
            cache_data = {
                'status': 'online',
                'info': info
            }
            return jsonify({
                'code': 200,
                'msg': '操作成功',
                'data': cache_data
            })
            
        except Exception as e:
            logger.error(f"获取Redis信息失败: {str(e)}", exc_info=True)
            return jsonify({
                'code': 500,
                'msg': f'获取Redis信息失败: {str(e)}',
                'data': None
            }), 500
            
    except Exception as e:
        logger.error(f"获取缓存信息失败: {str(e)}", exc_info=True)
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
        logger.info(f"开始获取缓存键: {cacheName}")
        logger.info(f"Redis连接状态: {redis_cache is not None}")
        
        # 处理特殊缓存名称
        if cacheName == "dbSize":
            # 获取数据库大小信息
            try:
                logger.info("正在获取数据库大小信息...")
                db_info = redis_cache.info('keyspace')
                logger.info(f"原始db_info类型: {type(db_info)}, 内容: {db_info}")
                
                # 处理不同类型返回值
                if isinstance(db_info, bytes):
                    db_info = db_info.decode('utf-8')
                elif isinstance(db_info, dict):
                    db_info = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                              v.decode('utf-8') if isinstance(v, bytes) else v
                              for k, v in db_info.items()}
                
                logger.info(f"处理后的db_info: {db_info}")
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': db_info
                })
            except Exception as e:
                logger.error(f"获取数据库信息失败: {str(e)}", exc_info=True)
                return jsonify({
                    'code': 500,
                    'msg': f'获取数据库信息失败: {str(e)}',
                    'data': None
                }), 500
        elif cacheName == "commandStats":
            # 获取命令统计信息
            try:
                logger.info("正在获取命令统计信息...")
                cmd_info = redis_cache.info('commandstats')
                logger.info(f"原始cmd_info类型: {type(cmd_info)}, 内容: {cmd_info}")
                
                # 处理不同类型返回值
                if isinstance(cmd_info, bytes):
                    cmd_info = cmd_info.decode('utf-8')
                elif isinstance(cmd_info, dict):
                    cmd_info = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                               v.decode('utf-8') if isinstance(v, bytes) else v
                               for k, v in cmd_info.items()}
                
                logger.info(f"处理后的cmd_info: {cmd_info}")
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': cmd_info
                })
            except Exception as e:
                logger.error(f"获取命令统计信息失败: {str(e)}", exc_info=True)
                return jsonify({
                    'code': 500,
                    'msg': f'获取命令统计信息失败: {str(e)}',
                    'data': None
                }), 500
                
        elif cacheName == "info":
            # 获取Redis服务器信息
            try:
                logger.info("正在获取Redis服务器信息...")
                
                # 检查Redis连接
                logger.info(f"Redis连接状态: {redis_cache.ping()}")
                
                # 获取原始info数据
                info_data = redis_cache.info()
                logger.info(f"原始info_data类型: {type(info_data)}, 内容: {info_data}")
                
                # 处理空数据情况
                if not info_data:
                    logger.warning("Redis info命令返回空数据！")
                    return jsonify({
                        'code': 200,
                        'msg': '操作成功',
                        'data': []
                    })
                
                # 转换数据格式为可显示的字符串
                processed_data = []
                if isinstance(info_data, bytes):
                    processed_data = [{'cacheKey': f"info: {info_data.decode('utf-8')}"}]
                elif isinstance(info_data, dict):
                    processed_data = [
                        {'cacheKey': f"{k}: {str(v)}"}
                        for k, v in info_data.items()
                    ]
                
                logger.info(f"转换后的数据条目数: {len(processed_data)}")
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': processed_data
                })
            except Exception as e:
                logger.error(f"获取Redis服务器信息失败: {str(e)}", exc_info=True)
                return jsonify({
                    'code': 500,
                    'msg': f'获取Redis服务器信息失败: {str(e)}',
                    'data': None
                }), 500
                logger.info(f"原始cmd_info类型: {type(cmd_info)}, 内容: {cmd_info}")
                
                # 处理不同类型返回值
                if isinstance(cmd_info, bytes):
                    cmd_info = cmd_info.decode('utf-8')
                elif isinstance(cmd_info, dict):
                    cmd_info = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                               v.decode('utf-8') if isinstance(v, bytes) else v
                               for k, v in cmd_info.items()}
                
                logger.info(f"处理后的cmd_info: {cmd_info}")
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': cmd_info
                })
            except Exception as e:
                logger.error(f"获取命令统计信息失败: {str(e)}", exc_info=True)
                return jsonify({
                    'code': 500,
                    'msg': f'获取命令统计信息失败: {str(e)}',
                    'data': None
                }), 500
        else:
            # 获取普通键列表
            try:
                logger.info(f"正在获取键列表: {cacheName}")
                keys = redis_cache.keys(f"*{cacheName}*") if cacheName != "*" else redis_cache.keys()
                logger.info(f"获取到的原始键数量: {len(keys) if keys else 0}")
                
                # 处理键列表
                if keys:
                    keys = [k.decode('utf-8') if isinstance(k, bytes) else str(k) for k in keys]
                
                logger.info(f"处理后的键列表(前10个): {keys[:10]}{'...' if len(keys)>10 else ''}")
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': keys or []
                })
            except Exception as e:
                logger.error(f"获取键列表失败: {str(e)}", exc_info=True)
                return jsonify({
                    'code': 500,
                    'msg': f'获取键列表失败: {str(e)}',
                    'data': None
                }), 500
            
    except Exception as e:
        logger.error(f"获取缓存键失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': 500,
            'msg': f'获取缓存键失败: {str(e)}',
            'data': None
        }), 500