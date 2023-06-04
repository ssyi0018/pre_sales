# md5加密
import hashlib
from django.conf import settings


def md5(data_sting):
    # 用django里自带的盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_sting.encode('utf-8'))
    return obj.hexdigest()
