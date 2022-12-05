import logging

from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.conf.cloud_service_conf import *

__all__ = ['S3Connector']
_LOGGER = logging.getLogger(__name__)


class S3Connector(AWSConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3_client = self.set_connect(kwargs.get('secret_data'), kwargs.get('region_name', DEFAULT_REGION), service="s3")

    def get_bucket_versioning(self, bucket_name):
        try:
            return self.s3_client.get_bucket_versioning(Bucket=bucket_name)
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Bucket Versioning] {e}')
            return None

    def get_bucket_versioning(self, bucket_name):
        try:
            return self.s3_client.get_bucket_versioning(Bucket=bucket_name)
        except Exception as e:
            return {}

    def get_bucket_encryption(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_encryption(Bucket=bucket_name)
            return response.get('ServerSideEncryptionConfiguration', {})
        except Exception as e:
            return {}

    def get_bucket_policy_status(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_policy_status(Bucket=bucket_name)
            return response.get('PolicyStatus', {})
        except Exception as e:
            return {}
