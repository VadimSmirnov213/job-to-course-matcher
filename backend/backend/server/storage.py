#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
from config import aws_access_key_id, aws_secret_access_key
class Storage:
    def __init__(self):
        self.session = boto3.session.Session().client(service_name='s3',
                                      endpoint_url='https://storage.yandexcloud.net',
                                      region_name='ru-central1',
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)


storage = Storage()
session = storage.session