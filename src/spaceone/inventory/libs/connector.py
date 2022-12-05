import logging
from boto3.session import Session
from spaceone.core import utils
from spaceone.core.connector import BaseConnector
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


class AWSConnector(BaseConnector):
    def __init__(self, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data
        """

        super().__init__(transaction=None, connector_conf=None)
        self.session = None

    def set_connect(self, secret_data, region_name, service="ec2"):
        self.session = self.get_session(secret_data, region_name)
        client = self.session.client(service, region_name=region_name)
        return client

    def set_client(self, service, region_name):
        return self.session.client(service, region_name)

    def get_aws_account(self, secret_data):
        session = self.get_session(secret_data, DEFAULT_REGION)
        sts_client = session.client('sts')
        response = sts_client.get_caller_identity()
        return response.get('Account')

    def get_all_regions(self, secret_data):
        session = self.get_session(secret_data, DEFAULT_REGION)
        ec2_client = session.client('ec2')
        return list(map(lambda region_info: region_info.get('RegionName'),
                        ec2_client.describe_regions().get('Regions')))

    def verify(self, secret_data, region_name):
        self.set_connect(secret_data, region_name)
        return "ACTIVE"

    @staticmethod
    def get_session(secret_data, region_name):
        params = {
            'aws_access_key_id': secret_data['aws_access_key_id'],
            'aws_secret_access_key': secret_data['aws_secret_access_key'],
            'region_name': region_name
        }

        session = Session(**params)

        # ASSUME ROLE
        if role_arn := secret_data.get('role_arn'):
            sts = session.client('sts')

            _assume_role_request = {
                'RoleArn': role_arn,
                'RoleSessionName': utils.generate_id('AssumeRoleSession'),
            }

            if external_id := secret_data.get('external_id'):
                _assume_role_request.update({'ExternalId': external_id})

            assume_role_object = sts.assume_role(**_assume_role_request)
            credentials = assume_role_object['Credentials']

            assume_role_params = {
                'aws_access_key_id': credentials['AccessKeyId'],
                'aws_secret_access_key': credentials['SecretAccessKey'],
                'region_name': region_name,
                'aws_session_token': credentials['SessionToken']
            }
            session = Session(**assume_role_params)

        return session
