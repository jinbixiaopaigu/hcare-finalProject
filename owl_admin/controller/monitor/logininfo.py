# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from typing import List
from pydantic import BeforeValidator
from typing_extensions import Annotated

from owl_common.base.transformer import ids_to_list
from owl_common.base.model import AjaxResponse, TableResponse
from owl_common.descriptor.serializer import BaseSerializer, JsonSerializer
from owl_common.descriptor.validator import QueryValidator, PathValidator
from owl_common.domain.enum import BusinessType
from owl_system.domain.entity import SysLogininfor
from owl_system.service.sys_logininfo import SysLogininforService
from owl_framework.descriptor.log import Log
from owl_framework.descriptor.permission import HasPerm, PreAuthorize
from ... import reg


@reg.api.route('/monitor/logininfor/list',methods=['GET'])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm("monitor:logininfor:list"))
@JsonSerializer()
def monitor_logininfo_list(dto:SysLogininfor):
    '''
        查询登录日志列表
    '''
    from flask import request, g
    from owl_common.base.transformer import to_datetime
    from owl_common.base.model import ExtraModel, CriterianMeta
    import sys
    import traceback
    import json
    from urllib.parse import unquote
    
    # 使用print直接输出到控制台
    print("\n=== 登录日志查询调试信息 ===", file=sys.stderr)
    print(f"完整请求URL: {request.url}", file=sys.stderr)
    print(f"请求方法: {request.method}", file=sys.stderr)
    print(f"原始请求参数: {request.args}", file=sys.stderr)
    
    try:
        # 获取并解析所有参数
        all_args = request.args.to_dict()
        print(f"所有参数字典: {all_args}", file=sys.stderr)
        
        # 检查是否存在params[beginTime]格式的参数
        begin_time = all_args.get('params[beginTime]')
        end_time = all_args.get('params[endTime]')
        
        if begin_time or end_time:
            print(f"找到params[beginTime]格式的参数: beginTime={begin_time}, endTime={end_time}", file=sys.stderr)
        else:
            # 尝试解析params参数
            params_str = request.args.get('params', '{}')
            try:
                params = json.loads(params_str)
                print(f"解析JSON格式的params参数: {params}", file=sys.stderr)
                begin_time = params.get('beginTime')
                end_time = params.get('endTime')
            except Exception as e:
                print(f"解析params参数失败: {e}", file=sys.stderr)
                params = {}
        
        print(f"最终解析到的时间参数 - beginTime: {begin_time}, endTime: {end_time}", file=sys.stderr)
        
        # 初始化查询条件元数据
        if not hasattr(g, 'criterian_meta'):
            g.criterian_meta = CriterianMeta()
        
        # 处理时间参数
        if begin_time or end_time:
            try:
                # 创建ExtraModel实例
                extra_model = ExtraModel()
                if begin_time:
                    # 解码URL编码的时间字符串
                    begin_time = unquote(begin_time)
                    print(f"解码后的beginTime: {begin_time}", file=sys.stderr)
                    try:
                        # 打印原始时间字符串和解析结果
                        print(f"尝试解析beginTime: {begin_time}", file=sys.stderr)
                        extra_model.start_time = to_datetime()(begin_time)
                        print(f"成功解析beginTime为: {extra_model.start_time}", file=sys.stderr)
                    except Exception as e:
                        print(f"解析beginTime失败: {e}\n{traceback.format_exc()}", file=sys.stderr)
                        return AjaxResponse.from_error(f"开始时间格式错误: {begin_time}，请使用YYYY-MM-DD HH:MM:SS格式")
                
                if end_time:
                    # 解码URL编码的时间字符串
                    end_time = unquote(end_time)
                    print(f"解码后的endTime: {end_time}", file=sys.stderr)
                    try:
                        # 打印原始时间字符串和解析结果
                        print(f"尝试解析endTime: {end_time}", file=sys.stderr)
                        extra_model.end_time = to_datetime()(end_time)
                        print(f"成功解析endTime为: {extra_model.end_time}", file=sys.stderr)
                    except Exception as e:
                        print(f"解析endTime失败: {e}\n{traceback.format_exc()}", file=sys.stderr)
                        return AjaxResponse.from_error(f"结束时间格式错误: {end_time}，请使用YYYY-MM-DD HH:MM:SS格式")
                
                print(f"创建的ExtraModel: {extra_model}", file=sys.stderr)
                g.criterian_meta._extra = extra_model
            except Exception as e:
                print(f"处理时间参数失败: {e}\n{traceback.format_exc()}", file=sys.stderr)
                raise
        
        # 打印最终查询条件
        print(f"最终查询条件: {dto}", file=sys.stderr)
        print(f"g.criterian_meta: {g.criterian_meta.__dict__ if hasattr(g, 'criterian_meta') else None}", file=sys.stderr)
        
        rows = SysLogininforService.select_logininfor_list(dto)
        print(f"查询返回结果数量: {len(rows)}", file=sys.stderr)
        return TableResponse(rows=rows)
    except Exception as e:
        print(f"查询登录日志失败: {e}\n{traceback.format_exc()}", file=sys.stderr)
        raise


@reg.api.route('/monitor/logininfor/export',methods=['POST'])
@PreAuthorize(HasPerm("monitor:logininfor:export"))
@Log(title = "登录日志", business_type = BusinessType.EXPORT)
@BaseSerializer()
def monitor_logininfo_export():
    '''
        导出登录日志
    '''
    # todo
    return AjaxResponse.from_success()


@reg.api.route('/monitor/logininfor/<ids>',methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm("monitor:logininfor:remove"))
@Log(title = "登录日志", business_type = BusinessType.DELETE)
@JsonSerializer()
def monitor_logininfo_delete(
    ids: Annotated[List[int],BeforeValidator(ids_to_list)]
):
    '''
        批量删除登录日志
    '''
    SysLogininforService.delete_logininfor(ids)
    return AjaxResponse.from_success()


@reg.api.route('/monitor/logininfor/clean',methods=['DELETE'])
@PreAuthorize(HasPerm("monitor:logininfor:remove"))
@Log(title = "登录日志", business_type = BusinessType.CLEAN)
@JsonSerializer()
def monitor_logininfo_clean():
    '''
        清空登录日志
    '''
    SysLogininforService.clean_logininfor()
    return AjaxResponse.from_success()