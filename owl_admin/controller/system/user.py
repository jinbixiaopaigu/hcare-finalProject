# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from typing import List
from pydantic import BeforeValidator, Field
from typing_extensions import Annotated
from flask_login import login_required

from owl_common.base.transformer import ids_to_list
from owl_common.base.model import AjaxResponse, TableResponse
from owl_common.constant import UserConstants
from owl_common.utils import security_util as SecurityUtil
from owl_common.utils.base import ExcelUtil
from owl_common.domain.entity import SysUser, SysRole
from owl_common.domain.enum import BusinessType
from owl_common.descriptor.serializer import BaseSerializer, JsonSerializer
from owl_common.descriptor.validator import FormUrlencodedValidator, FormValidator, QueryValidator, BodyValidator, PathValidator
from owl_system.service.sys_role import SysRoleService
from owl_system.service import SysUserService
from owl_framework.descriptor.permission import HasPerm, PreAuthorize
from owl_framework.descriptor.log import Log
from ... import reg


@reg.api.route("/system/user/list", methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm("system:user:list"))
@JsonSerializer()
def system_user_list(dto:SysUser):
    '''
        获取用户列表
    '''
    rows = SysUserService.select_user_list(dto)
    table_response = TableResponse(rows=rows)
    return table_response


@reg.api.route("/system/user/<int:id>", methods=["GET"])
@PathValidator()
@PreAuthorize(HasPerm("system:user:query"))
@JsonSerializer()
def system_get_user(id:int):
    '''
        获取用户详情
    '''
    user = SysUserService.select_user_by_id(id)
    ajax_response = AjaxResponse.from_success(data=user)
    return ajax_response


@reg.api.route("/system/user", methods=["POST"])
@BodyValidator()
@PreAuthorize(HasPerm("system:user:add"))
@Log(title="用户管理",business_type=BusinessType.INSERT)
@JsonSerializer()
def system_create_user(dto:SysUser):
    '''
        新增用户
    '''
    if SysUserService.check_user_name_unique(dto) \
        == UserConstants.NOT_UNIQUE:
        return AjaxResponse.from_error(
            f"新增用户'{dto.user_name}'失败，登录账号已存在"
        )
    elif dto.phonenumber \
        and SysUserService.check_phone_unique(dto) \
        == UserConstants.NOT_UNIQUE:
        return AjaxResponse.from_error(
            f"新增用户'{dto.phonenumber}'失败，手机号码已存在"
        )
    elif dto.email \
        and SysUserService.check_email_unique(dto) \
        == UserConstants.NOT_UNIQUE:
        return AjaxResponse.from_error(
            f"新增用户'{dto.email}'失败，邮箱已存在"
        )
    dto.create_by_user(SecurityUtil.get_user_id())
    flag = SysUserService.insert_user(dto)
    ajax_response = AjaxResponse.from_success() if flag else AjaxResponse.from_error()
    return ajax_response


@reg.api.route("/system/user", methods=["PUT"])
@BodyValidator()
@PreAuthorize(HasPerm("system:user:edit"))
@Log(title="用户管理",business_type=BusinessType.UPDATE)
@JsonSerializer()
def system_update_user(dto:SysUser):
    '''
        修改用户
    '''
    SysUserService.check_user_allowed(dto)
    SysUserService.check_user_data_scope(dto.user_id)
    if dto.phonenumber \
        and SysUserService.check_phone_unique(dto.phonenumber) \
        == UserConstants.NOT_UNIQUE:
        return AjaxResponse.from_error(
            f"新增用户'{dto.phonenumber}'失败，手机号码已存在"
        )
    elif dto.email \
        and SysUserService.check_email_unique(dto.email) \
        == UserConstants.NOT_UNIQUE:
        return AjaxResponse.from_error(
            f"新增用户'{dto.email}'失败，邮箱已存在"
        )
    dto.update_by_user(SecurityUtil.get_user_id())
    flag = SysUserService.update_user(dto)
    ajax_response = AjaxResponse.from_success() if flag else AjaxResponse.from_error()
    return ajax_response


@reg.api.route("/system/user/<ids>", methods=["DELETE"])
@PathValidator()
@PreAuthorize(HasPerm("system:user:remove"))
@Log(title="用户管理",business_type=BusinessType.DELETE)
@JsonSerializer()
def system_delete_users(
    ids: Annotated[List[int],BeforeValidator(ids_to_list)]
):
    '''
        删除用户
    '''
    if SecurityUtil.get_user_id() in ids:
        return AjaxResponse.from_error("当前用户不能删除")
    flag = SysUserService.delete_users_by_ids(ids)
    ajax_response = AjaxResponse.from_success() if flag > 0 else AjaxResponse.from_error()
    return ajax_response


@reg.api.route("/system/user/export", methods=["POST"])
@FormUrlencodedValidator()
@PreAuthorize(HasPerm("system:user:export"))
@Log(title="用户管理",business_type=BusinessType.EXPORT)
@BaseSerializer()
def system_user_export(dto:SysUser):
    '''
        导出用户数据
    '''
    rows = SysUserService.select_user_list(dto)
    excel_util = ExcelUtil(SysUser)
    return excel_util.export_response(rows, "用户数据")


@reg.api.route("/system/user/importData", methods=["POST"])
@FormValidator()
@PreAuthorize(HasPerm("system:user:import"))
@Log(title="用户管理",business_type=BusinessType.IMPORT)
@BaseSerializer()
def system_user_importdata(dto:SysUser):
    '''
        导入用户模板
    '''
    print("system_user_importdata:",dto)
    excel_util = ExcelUtil(SysUser)
    excel_util.import_data(dto)
    


@reg.api.route("/system/user/importTemplate", methods=["POST"])
@login_required
@BaseSerializer()
def system_user_importtemplate():
    '''
        导出模板
    '''
    excel_util = ExcelUtil(SysUser)
    return excel_util.import_template_response("用户数据")
    
    
@reg.api.route("/system/user/resetPwd", methods=["PUT"])
@BodyValidator()
@PreAuthorize(HasPerm("system:user:resetPwd"))
@Log(title="用户管理",business_type=BusinessType.UPDATE)
@JsonSerializer()
def system_update_user_resetpwd(dto:SysUser):
    '''
        重置密码
    '''
    SysUserService.check_user_allowed(dto)
    SysUserService.check_user_data_scope(dto.user_id)
    dto.password = SecurityUtil.encrypt_password(dto.password)
    dto.update_by_user(SecurityUtil.get_user_id())
    flag = SysUserService.reset_pwd(dto)
    ajax_response = AjaxResponse.from_success() if flag else AjaxResponse.from_error()
    return ajax_response


@reg.api.route("/system/user/changeStatus", methods=["PUT"])
@BodyValidator()
@PreAuthorize(HasPerm("system:user:edit"))
@Log(title="用户管理",business_type=BusinessType.UPDATE)
@JsonSerializer()
def system_update_user_changestatus(dto:SysUser):
    '''
        修改用户状态
    '''
    SysUserService.check_user_allowed(dto)
    SysUserService.check_user_data_scope(dto.user_id)
    dto.update_by_user(SecurityUtil.get_user_id())
    flag = SysUserService.update_user_status(dto)
    ajax_response = AjaxResponse.from_success() if flag else AjaxResponse.from_error()
    return ajax_response
    
    
@reg.api.route("/system/user/authRole/<int:id>", methods=["GET"])
@PathValidator()
@PreAuthorize(HasPerm("system:user:query"))
@JsonSerializer()
def system_get_user_authrole(id:int):
    '''
        获取用户授权角色
    '''
    sysuser:SysUser = SysUserService.select_user_by_id(id)
    roles:SysRole = SysRoleService.select_role_by_id(id)
    ajax_response = AjaxResponse.from_success() if sysuser else AjaxResponse.from_error()
    setattr(ajax_response,"user",sysuser)
    setattr(ajax_response,"roles",roles)
    return ajax_response
    
    
@reg.api.route("/system/user/authRole", methods=["PUT"])
@BodyValidator()
@PreAuthorize(HasPerm("system:user:edit"))
@Log(title="用户管理",business_type=BusinessType.GRANT)
@JsonSerializer()
def system_update_user_authrole(
    user_id:Annotated[int,Field(gt=0)],
    role_ids:Annotated[List[int],Field(default_factory=List)]
):
    '''
        授权用户角色
    '''
    SysUserService.check_user_data_scope(user_id)
    SysUserService.update_user_roles(user_id,role_ids)
    return AjaxResponse.from_success()
