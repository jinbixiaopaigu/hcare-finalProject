


from dataclasses import dataclass, field
from typing import List, Literal

from pydantic import Field


def ExcelField(
    name:str,
    cell_type:Literal['numeric', 'string', 'image'] = "string",
    width:int=16,
    height:int=14,
    default:str='',
    converter:str='',
    prompt:str='',
    combo:List=[],
    date_format:str='',
    is_export:bool=True,
    is_statistics:bool=False,
    header_background_color:str='#F2F2F2',
    header_color:str='#000000',
    background_color:str='#FFFFFF',
    color:str='#000000',
    align:str='left',
    handler=None,
    args:List=[],
    action:Literal['import', 'export', 'both']='both'
):
    excel_access = ExcelAccess(
        name=name,
        cell_type=cell_type,
        width=width,
        height=height,
        default=default,
        converter=converter,     
        prompt=prompt,
        date_format=date_format,
        combo=combo,
        is_export=is_export,
        is_statistics=is_statistics,
        header_background_color=header_background_color,
        header_color=header_color,
        background_color=background_color,
        color=color,
        align=align,
        handler=handler,
        args=args,
        action=action
    )
    Field(excel_access=excel_access)

def ExcelFields(*access:"ExcelAccess"):
    Field(excel_access=access)    


@dataclass(frozen=True)
class ExcelAccess:
    
    sort: int = 0
    
    name: str = ''
    
    date_format: str = ''
    
    dict_type: str = ''
    
    converter: str = ''
    
    separators: str = ','
    
    scale: bool = False
    
    roundmode: str = ''
    
    height: int = 14
    
    width: int = 16
    
    suffix: str = ''
    
    default: str = ''
    
    prompt: str = ''
    
    combo: List = field(default_factory=list)
    
    attr: str = ''
    
    is_export: bool = True
    
    is_statistics : bool = False
    
    cell_type: Literal['numeric', 'string', 'image'] = 'string'
    
    header_background_color: str = '#F2F2F2'
    
    header_color: str = '#000000'
    
    background_color: str = '#FFFFFF'
    
    color: str = '#000000'
    
    align: str = 'left'
    
    handler: str = ''
    
    args: List = field(default_factory=list)
    
    action: Literal['import', 'export', 'both'] = 'both'
    
    
    