from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static-assets'


class MediaStorage(S3Boto3Storage):
    location = 'media-files'
