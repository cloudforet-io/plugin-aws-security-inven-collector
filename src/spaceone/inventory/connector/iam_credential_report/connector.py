import logging

from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.conf.cloud_service_conf import *

__all__ = ['IAMCredentialReportConnector']
_LOGGER = logging.getLogger(__name__)


class IAMCredentialReportConnector(AWSConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.iam_client = self.set_connect(kwargs.get('secret_data'), DEFAULT_REGION, service="iam")

    def get_credential_report(self):
        response = self.iam_client.get_credential_report()
        return response.get('Content', {})
