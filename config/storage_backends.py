from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootStorage(S3Boto3Storage):
    location = 'static'


class MediaRootStorage(S3Boto3Storage):
    location = 'myblog-media'
