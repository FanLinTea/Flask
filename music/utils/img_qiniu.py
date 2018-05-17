# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag, urlsafe_base64_encode,put_data
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
def imp_up(localfile):
    access_key = 'QF8H5MqRZb6RrtEYK99pp-ExPPzhSUhMYpbXGGDa'
    secret_key = 'cr6qagD6xm-pF3lhdaa5oVifHkCj0kRRpJSg1OGK'
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'test'
    #上传到七牛后保存的文件名
    # key = 'my-python-logo.png';
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)
    #要上传文件的本地路径

    ret, info = put_data(token, None, localfile)
    if info.status_code == 200:
        return ret["key"]
    else:
        raise Exception('上传失败')
# print info