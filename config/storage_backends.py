from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootStorage(S3Boto3Storage):
    location = 'myblog-static'
    default_acl = 'public-read'


class MediaRootStorage(S3Boto3Storage):
    location = 'myblog-media'
    default_acl = 'public-read'
