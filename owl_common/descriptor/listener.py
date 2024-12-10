# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from functools import wraps
from typing import Any
from blinker import Signal
from flask import Flask


class AppSignalListener(object):
    '''
    Application信号监听器
    '''
        
    def __init__(self, app:Flask, signal:Signal):
        self._app = app
        self._signal = signal
    
    def __call__(self, func) -> Any:
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._app.app_context():
                return func(*args, **kwargs)
            
        self._signal.connect_via(self._app)(wrapper)
        
        return wrapper


class ModuleSignalListener(object):
    '''
    模块信号监听器
    '''
    
    def __init__(self, module, signal:Signal):
        self._module = module
        self._signal = signal
    
    def __call__(self, func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
            
        self._signal.connect_via(self._module)(wrapper)
        
        return wrapper