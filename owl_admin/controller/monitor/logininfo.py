# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from typing import List
from pydantic import BeforeValidator
from typing_extensions import Annotated

from owl_common.base.transformer import ids_to_list
from owl_common.base.model import AjaxResponse, TableResponse
from owl_common.descriptor.serializer import BaseSerializer, JsonSerializer
from owl_common.descriptor.validator import QueryValidator, PathValidator, VoValidatorContext
from owl_common.domain.enum import BusinessType
from owl_system.domain.entity import SysLogininfor
from owl_system.service.sys_logininfo import SysLogininforService
from owl_framework.descriptor.log import Log
from owl_framework.descriptor.permission import HasPerm, PreAuthorize
from ... import reg


@reg.api.route('/monitor/logininfor/list',methods=['GET'])
@QueryValidator(
    is_page=True, 
    include={"login_time", "createTime", "infoId", "userName", "ipaddr", "status"}
)
@PreAuthorize(HasPerm("monitor:logininfor:list"))
@JsonSerializer()
def monitor_logininfo_list(dto:SysLogininfor):
    '''
        查询登录日志列表
    '''
    from flask import request, g
    from datetime import datetime
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
        
        from urllib.parse import unquote
        
        # 获取原始时间参数
        begin_time_str = all_args.get('beginTime')
        end_time_str = all_args.get('endTime')
        
        # 验证时间格式
        def validate_time_format(time_str):
            if not time_str:
                return None
            try:
                # URL解码并清理字符串
                decoded_str = unquote(time_str).replace('%20', ' ').strip()
                # 解析为datetime对象
                return datetime.strptime(decoded_str, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                print(f"时间参数解析错误: {str(e)}", file=sys.stderr)
                raise ValueError(
                    f"时间格式错误: '{time_str}'，请使用YYYY-MM-DD HH:MM:SS格式。"
                    f"示例: 2025-01-01 00:00:00"
                )
        
        try:
            begin_time = validate_time_format(begin_time_str)
            end_time = validate_time_format(end_time_str)
            print(f"处理后的时间参数: beginTime={begin_time}, endTime={end_time}", file=sys.stderr)
        except ValueError as e:
            print(f"时间参数验证失败: {str(e)}", file=sys.stderr)
            raise
        
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
                    extra_model.begin_time = begin_time
                    print(f"设置ExtraModel.begin_time: {begin_time}", file=sys.stderr)
                
                if end_time:
                    extra_model.end_time = end_time
                    print(f"设置ExtraModel.end_time: {end_time}", file=sys.stderr)
                
                print(f"创建的ExtraModel: {extra_model}", file=sys.stderr)
                g.criterian_meta._extra = extra_model
            except Exception as e:
                print(f"处理时间参数失败: {e}\n{traceback.format_exc()}", file=sys.stderr)
                raise
        
        # 打印最终查询条件
        print(f"最终查询条件: {dto}", file=sys.stderr)
        print(f"g.criterian_meta: {g.criterian_meta.__dict__ if hasattr(g, 'criterian_meta') else None}", file=sys.stderr)
        
        # 确保时间范围参数应用到查询条件
        if hasattr(g, 'criterian_meta') and hasattr(g.criterian_meta, '_extra'):
            extra = g.criterian_meta._extra
            if hasattr(extra, 'begin_time') and hasattr(extra, 'end_time'):
                # 使用正确的字段名设置时间范围
                dto.login_time = f"{extra.begin_time}~{extra.end_time}"
            print(f"应用时间范围后的查询条件: {dto}", file=sys.stderr)
        
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