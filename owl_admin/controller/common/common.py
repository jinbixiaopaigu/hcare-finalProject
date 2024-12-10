# -*- coding: utf-8 -*-
# @Author  : shaw-lee

import os
import time
from flask import request, send_from_directory
from pydantic import Field
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

from owl_common.config import OWLConfig
from owl_common.constant import Constants
from owl_common.descriptor.serializer import ViewSerializer
from owl_common.descriptor.validate import FileValidator, QueryValidator
from owl_common.base.entity import AjaxResponse, MultiFile
from owl_common.utils import FileUploadUtil, FileUtil, StringUtil
from ... import reg


@reg.api.route('/common/download')
@QueryValidator()
@ViewSerializer()
def common_download(
    file_name:Annotated[str,Field(min_length=1,max_length=100)],
    delete:Annotated[bool,Field(annotations=bool,default=False)],
):
    file_path = OWLConfig.download_path + file_name
    download_name = time.time() * 1000 + file_name[file_name.index("_") + 1:]
    try:
        response = send_from_directory(
            directory=OWLConfig.download_path,
            path=file_name,
            as_attachment=True,
            download_name=download_name,
        )
        if delete:
            FileUtil.delete_file(file_path)
    except NotFound as e:
        return AjaxResponse.from_error("文件不存在")
    except Exception as e:
        return AjaxResponse.from_error("下载失败")
    return response


@reg.api.route('/common/upload')
@FileValidator()
@ViewSerializer()
def common_upload(file:MultiFile):
    file:FileStorage = file.one()
    file_name = FileUploadUtil.upload(file,OWLConfig.upload_path)
    url = request.host_url[:-1] + file_name
    new_file_name = FileUploadUtil.get_filename(file_name)
    original_filename = file.filename
    ajax_response = AjaxResponse.from_success()
    setattr(ajax_response,"url",url)
    setattr(ajax_response,"file_name",file_name)
    setattr(ajax_response,"new_file_name",new_file_name)
    setattr(ajax_response,"original_filename",original_filename)
    return ajax_response


@reg.api.route('/common/uploads')
@FileValidator()
@ViewSerializer()
def common_uploads(files:MultiFile):
    file_names = []
    urls = []
    new_file_names = []
    original_filenames = []
    for _,file in files.items():
        file_name = FileUploadUtil.upload(file,OWLConfig.upload_path)
        file_names.append(file_name)
        url = request.host_url[:-1] + file_name
        urls.append(url)
        new_file_name = FileUploadUtil.get_filename(file_name)
        new_file_names.append(new_file_name)
        original_filename = file.filename
        original_filenames.append(original_filename)
    ajax_response = AjaxResponse.from_success()
    setattr(ajax_response,"urls",urls.join(","))
    setattr(ajax_response,"file_names",file_names.join(","))
    setattr(ajax_response,"new_file_names",new_file_names.join(","))
    setattr(ajax_response,"original_filenames",original_filenames.join(","))
    return ajax_response


@reg.api.route('/common/download/resource')
@QueryValidator()
@ViewSerializer()
def common_download_resource(
    resource:Annotated[str,Field(annotation=str,min_length=1,max_length=100)]
):
    download_path = OWLConfig.download_path + StringUtil.substring_after(resource,Constants.RESOURCE_PREFIX)
    download_name = os.path.basename(download_path)
    try:
        response = send_from_directory(
            directory=OWLConfig.download_path,
            path=download_path,
            as_attachment=True,
            download_name=download_name,
            )
    except NotFound as e:
        return AjaxResponse.from_error("文件不存在")
    except Exception as e:
        return AjaxResponse.from_error("下载失败")
    return response
