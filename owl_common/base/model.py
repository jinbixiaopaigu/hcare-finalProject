# -*- coding: utf-8 -*-
# @Author  : shaw-lee

from datetime import datetime
from io import BytesIO
from threading import Lock
# from types import None
from typing import Any, Dict, Generator, Iterator, List, Literal, Optional, Set, Tuple, Union

from flask import g
from typing_extensions import Annotated
from dataclasses import dataclass, field, replace
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from sqlalchemy import Row
from flask_sqlalchemy.model import Model
from pydantic.alias_generators import to_camel,to_pascal
from pydantic.aliases import AliasGenerator
from pydantic.fields import FieldInfo
from pydantic import AliasChoices, AliasPath, BaseModel, BeforeValidator, \
    ConfigDict, Field, ValidationInfo, computed_field, field_validator, model_validator
    
from owl_common.base.schema_excel import ExcelAccess
from owl_common.base.transformer import to_datetime
from owl_common.constant import HttpStatus
from owl_common.utils.base import DateUtil


strict_base_config = ConfigDict(
    from_attributes = True,
    alias_generator = to_camel,  
    frozen = False,
    extra = "forbid",
    strict = True,
    populate_by_name = True,
    json_encoders = {
        datetime: lambda v: v.strftime(DateUtil.YYYY_MM_DD_HH_MM_SS)
    },
)

general_response_serial_config = ConfigDict(
    from_attributes = True,
    alias_generator = to_camel,  
    extra = "allow",
    strict = True,
    populate_by_name = True,
    frozen = False,
    json_encoders = {
        datetime: lambda v: v.strftime(DateUtil.YYYY_MM_DD_HH_MM_SS)
    },
)


@dataclass
class ExtraOpt:
    
    name:str = field(init=False)
    
    info:FieldInfo = field(init=False)


@dataclass
class BetOpt(ExtraOpt):
    
    min:str = None
    
    max:str = None
    
    active:Literal["min","max","default"] = "default"

    def replace(self, **kwargs):
        return replace(self, **kwargs)


@dataclass(frozen=True)
class VoAccess:
    
    body: bool = True
    
    query: Union[ExtraOpt,bool] = False
    
    sort: bool = False
    

@dataclass
class VoValidatorContext:
    
    is_page: bool = False
    
    is_sort: bool = False
    
    exclude_data_alias: bool = False
    
    include_sort_alias: Set = field(default_factory=set)
    
    include_fields: Set = field(default_factory=set)
    
    exclude_fields: Set = field(default_factory=set)
    

@dataclass
class DbValidatorContext: 
    
    col_entity_list: List[Any]


@dataclass
class VoSerializerContext:
        
    exclude_fields: Set = field(default_factory=set)

    include_fields: Set = field(default_factory=set)

    by_alias: bool = True

    exclude_none: bool = True

    exclude_unset: bool = True

    exclude_default: bool = False
    
    is_excel: bool = False
    
    def as_kwargs(self):
        return {
            "by_alias": self.by_alias,
            "exclude": self.exclude_fields,
            "include": self.include_fields,
            "exclude_none": self.exclude_none,
            "exclude_unset": self.exclude_unset,
            "exclude_defaults": self.exclude_default
        }
    

@dataclass
class CriterianMeta:
    
    _scope: List = field(default_factory=list)
    
    _page: "PageModel" = field(default=None)
    
    _sort: "OrderModel" = field(default=None)
    
    _extra: "ExtraModel" = field(default=None)
    
    @property
    def scope(self):
        return self._scope
    
    @scope.setter
    def scope(self, value):
        self._scope = value
    
    @property
    def page(self):
        return self._page
    
    @page.setter
    def page(self, value):
        self._page = value
    
    @property
    def sort(self):
        return self._sort
    
    @sort.setter
    def sort(self, value):
        self._sort = value
    
    @property
    def extra(self):
        return self._extra
    
    @extra.setter
    def extra(self, value):
        self._extra = value

    
class BaseEntity(BaseModel):
    
    model_config = strict_base_config.copy()
    
    @model_validator(mode="before")
    def model_before_validation(cls, data:Any, info:ValidationInfo) -> Dict:
        '''
        数据校验前的处理
        '''
        new_values = {}
        if isinstance(info.context,DbValidatorContext):
            db_columns_alias = info.context.col_entity_list
            if db_columns_alias and db_columns_alias._alia_prefix:
                if isinstance(data, Row):
                    for k in data._mapping:
                        v = data._mapping[k]
                        if db_columns_alias.check_prefix(k):
                            key = db_columns_alias.to_field(k)
                            new_values[key] = v
                        else:
                            continue
            else:
                if isinstance(data, Row):
                    new_values = data._mapping
        elif isinstance(info.context,VoValidatorContext):
            pass
        else:
            if isinstance(data, Row):
                new_values = data._mapping
        return new_values if new_values else data
    
    
    @classmethod
    def generate_excel_schema(cls) -> Generator[Tuple[str,ExcelAccess],None,None]:
        '''
        生成excel的schema
        '''
        for k,info in cls.model_fields.items():
            if info.json_schema_extra is None:continue
            excel_access = info.json_schema_extra.get("excel_access",False)
            if excel_access:
                if isinstance(excel_access,(list,tuple,)):
                    for access in excel_access:
                        yield "{}.{}".format(k,access.attr),access
                else:
                    yield k,excel_access
    
    @classmethod
    def rebuild_excel_schema(cls,row:Dict[str,str]) -> Dict[str,str]:
        '''
        重新修改excel的schema，将别名修改为实际字段名
        '''
        new_row = {}
        for k,access in cls.generate_excel_schema():
            val = row.get(access.name)
            if "." in k:
                k1,k2 = k.split(".")
                new_row.setdefault(k1,{})[k2] = val
            else:
                new_row[k] = val
        return new_row
    
    def generate_excel_data(self) -> Generator[Tuple[str,ExcelAccess],None,None]:
        '''
        生成excel数据
        '''
        data = self.model_dump()
        for k,access in self.generate_excel_schema():
            if "." in k:
                k1,k2 = k.split(".")
                sub_data = data.get(k1,{})
                if sub_data:
                    val = sub_data.get(k2,None)
                else:
                    val = None
            else:
                val = data.get(k)
            access.val = val
            yield k,access
    
    def create_by_user(self, name: str ) -> None:
        self.create_by = name
        self.create_time = datetime.now()
    
    def update_by_user(self, name: str) -> None:
        self.update_by = name
        self.update_time = datetime.now()
        

class AuditEntity(BaseEntity):
    
    # 创建者
    create_by: Annotated[Union[str, int, None], Field(default=None, vo=VoAccess(body=False, query=False))]
    
    # 创建时间
    create_time: Annotated[Union[datetime, None], BeforeValidator(to_datetime()), Field(default=None, vo=VoAccess(body=False, query=False))]
    
    # 更新者
    update_by: Annotated[
        Union[str, int, None],
        Field(default=None, vo=VoAccess(body=False, query=False))
    ]

    # 更新时间
    update_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, vo=VoAccess(body=False, query=False))
    ]

    # 备注
    remark: Optional[str] = None
    

class AjaxResponse(BaseEntity):
    
    model_config = general_response_serial_config.copy()
    
    # 数据状态码
    code: Annotated[int, Field(default=HttpStatus.SUCCESS)]
    
    # 提示信息
    msg: Annotated[str, Field(default="")]
    
    # 数据
    data: Annotated[Any, Field(default=None)] 
    
    __pydantic_extra__: Dict[str, Any] = Field(init=False)
    
    @classmethod
    def from_success(cls, msg='操作成功', data=""):
        return cls(code=HttpStatus.SUCCESS, msg=msg, data=data)
    
    @classmethod
    def from_error(cls, msg='操作失败', data=""):
        return cls(code=HttpStatus.ERROR, msg=msg, data=data)


class TableResponse(BaseEntity):
    
    model_config = general_response_serial_config.copy()
    
    # 数据状态码
    code: Annotated[int, Field(default=HttpStatus.SUCCESS)]
    
    # 提示信息
    msg: Annotated[str, Field(default='查询成功')]
    
    # 数据
    rows: Annotated[
            List[Any],  # 建议补充泛型类型
            BeforeValidator(
                lambda x: list(x) if isinstance(x, (Iterator, map)) else x
            )
            ]
    
    __pydantic_extra__: Dict[str, Any] = Field(init=False)
    
    @computed_field
    @property
    def total(self) -> int:
        page:PageModel = g.criterian_meta.page
        if page and page.total:
            return page.total
        return len(self.rows)


class TreeEntity(AuditEntity):
    
    # 父菜单名称
    parent_name: Annotated[str, Field(default=None)]
    
    # 父菜单ID
    parent_id: Annotated[int, Field(default=None)]
    
    # 显示顺序
    order_num: Annotated[int, Field(default=None)]
    
    # 祖级列表
    ancestors: Annotated[str, Field(default=None)]

    # 子部门
    children: Annotated[List["TreeEntity"], Field(default=None)]


class MultiFile(ImmutableMultiDict):
    def one(self) -> FileStorage:
        return next(self.values())

    @classmethod
    def from_obj(cls, obj: ImmutableMultiDict) -> 'MultiFile':
        return cls(**obj.to_dict())


class VoModel(BaseModel):
    
    model_config = ConfigDict(
        from_attributes = False,
        alias_generator = AliasGenerator(
            alias=to_camel,
            validation_alias=to_camel,
            serialization_alias=to_pascal,
        ),  
        frozen = False,
        extra = "forbid",
        strict = True,
        populate_by_name = False,
    )

    @model_validator(mode="before")
    def model_before_validation(cls, data:Any, info:ValidationInfo) -> Dict:
        """
        处理data中的别名

        Args:
            data (Any): 数据
            info (ValidationInfo): 验证信息

        Returns:
            Dict: 处理后的数据
        """
        new_data = {}
        for k,finfo in cls.model_fields.items():
            alias_set = cls.get_validation_alias(k,finfo)
            for alias in alias_set:
                if alias in data:
                    if info.context and info.context.exclude_data_alias:
                        new_data[alias] = data.pop(alias, None)
                    else:
                        new_data[alias] = data.get(alias, None)
        return new_data
        
    
    @classmethod
    def get_serialization_alias(cls, name:str, info:FieldInfo) -> Set[str]:
        """
        获取字段的序列化别名  

        Args:
            name (str): 字段名称
            info (FieldInfo): 字段信息

        Raises:
            Exception: AliasPath不支持

        Returns:
            Set[str]: 序列化别名集合
        """
        alias_set = set()
        alias = cls.get_alias_from_config(name,False)
        if alias:
            alias_set.add(alias)
        if info.serialization_alias:
            alias_set.add(info.serialization_alias)
        return alias_set
    
    @classmethod
    def get_validation_alias(cls, name:str, info:FieldInfo) -> Set[str]:
        """
        获取字段的校验别名  

        Args:
            name (str): 字段名称
            info (FieldInfo): 字段信息

        Raises:
            Exception: AliasPath不支持

        Returns:
            Set[str]: 别名集合
        """
        alias_set = set()
        alias = cls.get_alias_from_config(name)
        if alias:
            alias_set = alias_set | alias
        if info.validation_alias:
            if isinstance(info.validation_alias, str):
                alias_set.add(info.validation_alias)
            elif isinstance(info.validation_alias, AliasPath):
                raise Exception(f"模型{cls.__name__}的字段不支持AliasPath")
            elif isinstance(info.validation_alias, AliasChoices):
                alias_set = alias_set | \
                    set(info.validation_alias.choices)
        if "populate_by_name" in cls.model_config \
            and cls.model_config["populate_by_name"]:
            alias_set.add(name)
        return alias_set
    
    @classmethod
    def get_alias_from_config(cls,name:str,validation=True)-> Optional[Set[str]]:
        """
        从配置中获取别名
        
        Args:
            name (str): 字段名称
            validation (bool, optional): 是否为验证字段. Defaults to True.
        
        Returns:
            Optional[Set[str]]: 别名
        """
        alias_set = set()
        if "generate_alias" in cls.model_config and \
            cls.model_config["generate_alias"]:
            g_alias,v_alias,s_alias = cls.model_config["generate_alias"].\
            generate_aliases(name)
            if validation:
                if g_alias:
                    alias_set.add(g_alias)
                if v_alias:
                    alias_set.add(v_alias)
            else:
                if s_alias:
                    alias_set.add(s_alias)
            return alias_set


class PageModel(VoModel):
    
    model_config = ConfigDict(
        from_attributes = False,
        alias_generator = AliasGenerator(
            alias=to_camel,
            validation_alias=to_camel,
            serialization_alias=to_pascal,
        ),  
        frozen = False,
        extra = "forbid",
        strict = True,
        populate_by_name = False,
    )
    
    page_num: Annotated[
        int, 
        BeforeValidator(int), 
        Field(1, ge=1,frozen=True)
    ] 
    
    page_size: Annotated[
        int, 
        BeforeValidator(int), 
        Field(10, ge=1, le=100, frozen=True)
    ] 
    
    total: Annotated[int, Field(default=None)]
    
    stmt: Annotated[Any, Field(default=None)]
    
        
class OrderModel(VoModel):
    
    order_by_column: Annotated[Optional[List[str]],Field(default=None)]
    
    is_asc: Annotated[Literal["asc", "desc"],Field(default="asc")]
    
    @field_validator("order_by_column",mode="before")
    def order_by_column_before_validation(cls, value:str, info:ValidationInfo) -> List[str]:
        value = value.split(",")
        if info.context and isinstance(info.context,VoValidatorContext):
            for val in value:
                if val not in info.context.include_sort_alias:
                    raise ValueError(f"排序字段{val},在禁止的模型字段范围内")
        return value
    

class ExtraModel(VoModel):
    
    begin_time: Annotated[
        Optional[datetime], 
        BeforeValidator(to_datetime()),
        Field(default=None)
    ]
    
    end_time: Annotated[
        Optional[datetime], 
        BeforeValidator(to_datetime()),
        Field(default=None)
    ]
            

class ForbiddenExtraModel(VoModel):
    
    def criterians(self,po:Model)-> List[Any]:
        """
        构建查询条件
        
        Args:
            po (Model): 数据库模型
        
        Returns:
            List[Any]: 查询条件
        """
        criterions = []
        for k,info in self.model_fields.items():
            val = getattr(self,k,None)
            json_extra = info.json_schema_extra
            if json_extra and "vo_opt" in json_extra:
                vo_opt:ExtraOpt = json_extra["vo_opt"]
                column = getattr(po,vo_opt.name,None)
                if column:
                    if isinstance(vo_opt, BetOpt):
                        if vo_opt.active == "min":
                            criterion = column >= val
                        elif vo_opt.active == "max":
                            criterion = column <= val
                        else:
                            criterion = column == val
                        criterions.append(criterion)
                    else:
                        criterions.append(column == val)
        return criterions

    
class AllowedExtraModel(ForbiddenExtraModel):
    
    model_config = ConfigDict(
        from_attributes = False,
        alias_generator = AliasGenerator(
            alias=to_camel,
            validation_alias=to_camel,
            serialization_alias=to_pascal,
        ),  
        frozen = True,
        extra = "allow",
        strict = True,
        populate_by_name = False,
    )

