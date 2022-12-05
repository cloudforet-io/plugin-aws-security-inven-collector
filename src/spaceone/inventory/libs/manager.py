import json
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.libs.schema.resource import ErrorResourceResponse


_LOGGER = logging.getLogger(__name__)


class AWSManager(BaseManager):
    cloud_service_types = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: AWSConnector = self.locator.get_connector('AWSConnector', secret_data=secret_data)
        region_name = kwargs.get('region_name', DEFAULT_REGION)
        connector.verify(secret_data, region_name)

    def collect_cloud_service_type(self, params):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        total_resources = []

        try:
            total_resources.extend(self.collect_cloud_service_type(params))
            resources, error_resources = self.collect_cloud_service(params)

            total_resources.extend(resources)
            total_resources.extend(error_resources)

        except Exception as e:
            error_resource_response = self.generate_error_response(e, self.cloud_service_types[0].resource.group, self.cloud_service_types[0].resource.name)
            total_resources.append(error_resource_response)
            _LOGGER.error(f'[collect] {e}', exc_info=True)

        return total_resources

    @staticmethod
    def get_aws_account(secret_data):
        connector = AWSConnector()
        return connector.get_aws_account(secret_data)

    @staticmethod
    def get_all_regions(secret_data):
        connector = AWSConnector()
        return connector.get_all_regions(secret_data)

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({'message': json.dumps(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type}})
        else:
            error_resource_response = ErrorResourceResponse({'message': str(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type}})
        return error_resource_response

    @staticmethod
    def generate_resource_error_response(e, cloud_service_group, cloud_service_type, resource_id):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({'message': json.dumps(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type,
                                                                          'resource_id': resource_id}})
        else:
            error_resource_response = ErrorResourceResponse({'message': str(e),
                                                             'resource': {'cloud_service_group': cloud_service_group,
                                                                          'cloud_service_type': cloud_service_type,
                                                                          'resource_id': resource_id}})
        return error_resource_response
