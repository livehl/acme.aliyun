# -*- coding: utf-8 -*-
import argparse
import os

from alibabacloud_cas20200407.client import Client as cas20200407Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cas20200407 import models as cas_20200407_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


# from alibabacloud_credentials.client import Client as CredClient


def main(akid, secret, name, cert, key):
    client = cas20200407Client(open_api_models.Config(
        endpoint="cas.aliyuncs.com", access_key_id=akid, access_key_secret=secret))
    with open(cert, encoding="utf-8") as c:
        cert_str = c.read()
    with open(key, encoding="utf-8") as k:
        key_str = k.read()
    upload_user_certificate_request = cas_20200407_models.UploadUserCertificateRequest(
        name=name, cert=cert_str, key=key_str
    )
    runtime = util_models.RuntimeOptions()
    # print(upload_user_certificate_request)
    try:
        # 复制代码运行请自行打印 API 的返回值
        ret = client.upload_user_certificate_with_options(upload_user_certificate_request, runtime)
        print(ret)
    except Exception as error:
        # 如有需要，请打印 error
        error_str = UtilClient.assert_as_string(error.message)
        print(error_str)
        if "名称重复" in error_str:
            list_user_certificate_order_request = cas_20200407_models.ListUserCertificateOrderRequest(
                order_type='UPLOAD'
            )
            print("已经存在同名证书，删除重建")
            try:
                # 复制代码运行请自行打印 API 的返回值
                ret = client.list_user_certificate_order_with_options(list_user_certificate_order_request, runtime)
                for i in ret.body.certificate_order_list:
                    if i.name == name:
                        delete_user_certificate_request = cas_20200407_models.DeleteUserCertificateRequest(
                            cert_id=i.certificate_id
                        )
                        ret = client.delete_user_certificate_with_options(delete_user_certificate_request, runtime)
                        # print(ret)
                        break
                main(akid, secret, name, cert, key)
            except Exception as error:
                # 如有需要，请打印 error
                UtilClient.assert_as_string(error.message)
    print("ok")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', type=str, required=True, help="access_key_id")
    parser.add_argument('-s', '--secret', type=str, required=True, help="access_key_secret")
    parser.add_argument('-n', '--name', type=str, required=True, help="域名")
    parser.add_argument('-c', '--cert', type=str, default="/data/cert.pem",
                        help="证书文件，默认/data/cert.pem")
    parser.add_argument('-k', '--key', type=str, default="/data/key.pem",
                        help="证书Key，默认为/data/key.pem")
    args = parser.parse_args()
    main(args.id, args.secret, args.name, args.cert, args.key)
