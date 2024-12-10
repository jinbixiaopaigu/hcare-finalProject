# -*- coding: utf-8 -*-
# @Author  : shaw-lee

import base64
import random
import string, uuid
from captcha.image import ImageCaptcha
from io import BytesIO

from owl_common.base.entity import AjaxResponse
from owl_common.constant import Constants
from owl_common.descriptor.serializer import ViewSerializer
from owl_admin.ext import redis_cache
from ... import reg


@reg.api.route("/captchaImage")
@ViewSerializer()
def index_captcha_image():
    """
    生成验证码图片
    :return:
    """
    ImageCaptcha.character_rotate = (-15, 15)
    ImageCaptcha.character_warp_dx = (0.1, 0.1)
    ImageCaptcha.character_warp_dy = (0.1, 0.1)
    ImageCaptcha.word_offset_dx = 0.2
    ImageCaptcha.word_space_probability = 0
    image = ImageCaptcha(width=230, height=76, font_sizes=[60])
    
    code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    uuid_str = uuid.uuid4().hex
    verifyKey = Constants.CAPTCHA_CODE_KEY + uuid_str
    redis_cache.set(verifyKey, code, ex=Constants.CAPTCHA_EXPIRATION*60)
    
    byte_buffer = BytesIO()
    try:
        image.write(code, byte_buffer)
    except Exception as e:
        return AjaxResponse.from_error(str(e))
    byte_image = byte_buffer.getvalue()
    ajax_response = AjaxResponse.from_success()
    ajax_response.uuid = uuid_str
    ajax_response.img = str(base64.b64encode(byte_image),encoding="utf-8")
    return ajax_response
