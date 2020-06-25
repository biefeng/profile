# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/15 23:02
# file_name : baidu_obs.py

import base64
import hashlib
import io
import logging
import os

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bos.bos_client import BosClient

_bos_host = "bj.bcebos.com"
_access_key_id = "9a137e5669e04e1ca994adbe435d644c"
_secret_access_key = "9e89feeb688345cda556992a1065a274"

_config = BceClientConfiguration(credentials=BceCredentials(_access_key_id, _secret_access_key), endpoint=_bos_host)

GENIOUS_BUCKET = 'genious'

LOGGER = logging.getLogger(__name__)


class BaiduBos:
    def __init__(self, bucket):
        self._bucket = bucket
        self._bos_client = BosClient(_config)

    def upload_file(self, fn, key, get_url=False, absent=True):
        """
        上传文件，如果文件超过25兆，将采用分块上传
        如果key已存在，则返回key的url
        :param fn:
        :param key:
        :param get_url:是否需要获取key对应的url
        :param absent: True时，如果bos已存在该文件  则不上传
        :return:
        """
        exists = False
        if absent:
            for obj in self._bos_client.list_all_objects(self._bucket):
                if obj.key == key:
                    LOGGER.warning("the key '{0}' has already existed, upload canceled".format(key))
                    exists = True
                    break
        if not exists:
            fs = os.path.getsize(fn)
            with open(fn, mode='rb') as f:
                if fs > 25 * 1024 * 1024:
                    self._multipart_upload(fn, key)
                else:
                    self._bos_client.put_object(self._bucket, key, f, fs, self.md5_file(fn))
        if get_url:
            url = self._bos_client.generate_pre_signed_url(self._bucket, key)
            return url.decode("utf-8")
        return None

    def upload_bytes(self, byte_arr, key, get_url=False, absent=True):
        """
        上传字节
        如果key已存在，则返回key的url
        :param byte_arr:
        :param key:
        :return:
        """
        exists = False
        if absent:
            for obj in self._bos_client.list_all_objects(self._bucket):
                if obj.key == key:
                    LOGGER.warning("the key '{0}' has already existed, upload canceled".format(key))
                    exists = True
                    break
        if not exists:
            self._bos_client.put_object(GENIOUS_BUCKET, key, io.BytesIO(byte_arr), len(byte_arr), self.md5_obj(byte_arr))
        if get_url:
            url = self._bos_client.generate_pre_signed_url(self._bucket, key)
            return url.decode("utf-8")
        return None

    def upload_bytes_is_absent(self, byte_arr, key, get_url=False):
        for obj in self._bos_client.list_all_objects(self._bucket):
            if obj.key == key:
                LOGGER.warning("the key has already existed, upload canceled")
                return
        return self.upload_bytes(byte_arr, key, get_url)

    def _multipart_upload(self, fn, key):
        """
        文件分块上传
        如果key已存在，则返回key的url
        :arg key
        :arg fn
        """
        upload_id = self._bos_client.initiate_multipart_upload(GENIOUS_BUCKET, key).upload_id
        left_size = os.path.getsize(fn)
        # left_size用于设置分块开始位置
        # 设置分块的开始偏移位置
        offset = 0

        part_number = 1
        part_list = []
        index = 0
        while left_size > 0:
            # 设置每块为5MB
            part_size = 5 * 1024 * 1024
            if left_size < part_size:
                part_size = left_size

            response = self._bos_client.upload_part_from_file(
                GENIOUS_BUCKET, key, upload_id, part_number, part_size, fn, offset)
            index += 1
            print(index)
            left_size -= part_size
            offset += part_size
            part_list.append({
                "partNumber": part_number,
                "eTag": response.metadata.etag
            })

            part_number += 1
        location = self._bos_client.complete_multipart_upload(GENIOUS_BUCKET, key, upload_id, part_list)
        print(location.location)
        return location

    def md5_file(self, fn):
        buf_size = 8192
        md5 = hashlib.md5()
        with open(fn, mode='rb') as fp:
            while True:
                bytes_to_read = buf_size
                buf = fp.read(bytes_to_read)
                if not buf:
                    break
                md5.update(buf)
            content_md5 = base64.standard_b64encode(md5.digest())
        return content_md5

    def md5_obj(self, bs):
        md5 = hashlib.md5()
        md5.update(bs)
        return base64.standard_b64encode(md5.digest())

    def list_uploaded_objects(self, prefix=None):
        """
        列出桶中的文件，如果提供了prefix，则最多返回1000条记录
        若无法满足需要，可以使用sdk的api进行获取
        :arg 指定返回key的前缀"""
        keys = []
        if prefix is not None:
            response = self._bos_client.list_objects(self._bucket, prefix=prefix, max_keys=1000)
            for obj in response.contents:
                keys.append(obj.key)
            return keys
        response = self._bos_client.list_all_objects(self._bucket)
        for obj in response.contents:
            keys.append(obj.key)
        return keys

    def file_exists(self, fn):
        """
        :arg 文件名是否存在，服务器上的文件名为key去掉前缀（带slash）后的
        :return 如果文件存在，返回文件url,否则返回None
        """
        keys = self.list_uploaded_objects()
        for key in keys:
            slash_index = key.rfind("/")
            if slash_index > 0:
                file_name = key[slash_index + 1:]
                if file_name == fn:
                    url = self._bos_client.generate_pre_signed_url(bucket_name=GENIOUS_BUCKET, key=key, expiration_in_seconds=-1)
                    return url.decode("utf-8")
        return None

    def key_exists(self, key):
        keys = self.list_uploaded_objects()
        return keys.index(key) >= 0


if __name__ == '__main__':
    bos = BaiduBos(GENIOUS_BUCKET)
    bs = bytes("123", encoding="utf-8")
    print(bos.upload_file_if_absent("D:\\Download\\chromePlugin\\crx\\abkepgjebgiieabjeocpcimggpdjbaca.crx", "test.crx", True))
