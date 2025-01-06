# -*- coding: utf-8 -*-
# @Author  : shaw-lee

# todo: 完善异常类

from werkzeug.exceptions import HTTPException,InternalServerError

class CaptchaException(HTTPException):
    pass


class CaptchaExpireException(HTTPException):
    pass


class UserException(HTTPException):
    pass


class UserPasswordNotMatchException(HTTPException):
    pass


class UserNotFound(HTTPException):
    pass


class UserExistsError(HTTPException):
    pass


class ServiceException(InternalServerError):
    
    code = 500
    description = 'Service Error'


class BusinessException(InternalServerError):
    
    code = 500
    description = 'Business Error'
    

class MapperException(HTTPException):
    
    pass


class MapperDataNotFound(MapperException):
    
    pass