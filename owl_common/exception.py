# -*- coding: utf-8 -*-
# @Author  : shaw-lee

# todo: 完善异常类

class CaptchaException(Exception):
    pass


class CaptchaExpireException(Exception):
    pass


class UserException(Exception):
    pass


class UserPasswordNotMatchException(Exception):
    pass


class UserNotFound(Exception):
    pass


class UserExistsError(Exception):
    pass


class ServiceException(Exception):
    
    pass


class MapperException(Exception):
    
    pass


class MapperDataNotFound(MapperException):
    
    pass