# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from flask import jsonify, request
import logging
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


from urllib.parse import unquote

@reg.api.route('/monitor/cache/getValue', methods=['GET'])
@PreAuthorize(HasPerm("monitor:cache:list"))
@JsonSerializer()
def get_cache_value():
    '''
        获取指定缓存的值
    '''
    try:
        # 记录请求参数
        logger.info(f"请求参数: {request.args}")
        
        # 参数验证
        cache_name = request.args.get('cache_name')
        cache_key = request.args.get('cache_key')
        
        if not cache_name or not cache_key:
            error_msg = f"缺少必要参数 cache_name: {cache_name}, cache_key: {cache_key}"
            logger.error(error_msg)
            return jsonify({
                'code': 400,
                'msg': error_msg,
                'data': None
            }), 400
            
        # Redis连接检查
        try:
            redis_cache.ping()
        except Exception as e:
            error_msg = f"Redis连接失败: {str(e)}"
            logger.error(error_msg)
            return jsonify({
                'code': 500,
                'msg': error_msg,
                'data': None
            }), 500
            
        # 处理请求
        decoded_key = unquote(cache_key).strip()
        logger.info(f"处理请求 - 缓存名: {cache_name}, 键: {decoded_key}")
        
        # 验证参数
        if not cache_name:
            logger.error("缺少缓存名称参数")
            return jsonify({
                'code': 400,
                'msg': '缺少缓存名称参数',
                'data': None
            }), 400
            
        if not decoded_key:
            logger.error("缺少缓存键参数")
            return jsonify({
                'code': 400,
                'msg': '缺少缓存键参数',
                'data': None
            }), 400
            
        # 处理特殊缓存名称
        if cache_name == "info":
            logger.info("处理Redis info命令请求")
        
        # 处理特殊缓存名称
        if cache_name == "info":
            # 获取Redis服务器信息
            try:
                info_data = redis_cache.info()
                if isinstance(info_data, bytes):
                    value = info_data.decode('utf-8')
                elif isinstance(info_data, dict):
                    value = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                            v.decode('utf-8') if isinstance(v, bytes) else v
                            for k, v in info_data.items()}
                else:
                    value = str(info_data)
                
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': value
                })
            except Exception as e:
                logger.error(f"获取Redis信息失败: {str(e)}", exc_info=True)
                return jsonify({
                    'code': 500,
                    'msg': f'获取Redis信息失败: {str(e)}',
                    'data': None
                }), 500
        else:
            # 获取普通缓存值
            try:
                value = redis_cache.get(cache_key)
                if value is None:
                    return jsonify({
                        'code': 404,
                        'msg': '缓存键不存在',
                        'data': None
                    }), 404
                
                # 处理不同类型返回值
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                
                return jsonify({
                    'code': 200,
                    'msg': '操作成功',
                    'data': value
                })
            except Exception as e:
                logger.error(f"获取缓存值失败: {str(e)}", exc_info=True)
                return jsonify({
                    'code': 500,
                    'msg': f'获取缓存值失败: {str(e)}',
                    'data': None
                }), 500
                
    except Exception as e:
        logger.error(f"获取缓存值失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': 500,
            'msg': f'获取缓存值失败: {str(e)}',
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