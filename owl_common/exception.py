# -*- coding: utf-8 -*-
# @Author  : shaw-lee

# todo: 完善异常类

from werkzeug.exceptions import HTTPException


class CreatedException(HTTPException):
    
    code = 201
    description = 'Request Create Status'

    
class AcceptedException(HTTPException):
    
    code = 202
    description = 'Request Accept Status'


class NoContentException(HTTPException):
    
    code = 204
    description = 'Request No Content Status'


class ServiceException(AcceptedException):
    
    description = 'Service Accept Status'
    
