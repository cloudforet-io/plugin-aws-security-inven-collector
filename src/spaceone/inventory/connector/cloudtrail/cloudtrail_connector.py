import logging

from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.conf.cloud_service_conf import *

__all__ = ['CloudTrailConnector']
_LOGGER = logging.getLogger(__name__)


class CloudTrailConnector(AWSConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cloudtrail_client = self.set_connect(kwargs.get('secret_data'), DEFAULT_REGION, service="cloudtrail")

    def describe_trails(self):
        response = self.cloudtrail_client.describe_trails()
        return response.get('trailList', [])

    def get_event_selectors(self, trail_name):
        response = self.cloudtrail_client.get_event_selectors(TrailName=trail_name)
        return response.get('EventSelectors', [])

    def get_insight_selectors(self, trail_name):
        response = self.cloudtrail_client.get_insight_selectors(TrailName=trail_name)
        return response.get('InsightSelectors', [])

    def list_tags(self, trail_arns):
        response = self.cloudtrail_client.list_tags(ResourceIdList=trail_arns)
        return response.get('ResourceTagList', [])
