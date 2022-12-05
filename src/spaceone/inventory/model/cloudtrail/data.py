import logging
from schematics import Model
from schematics.types import ModelType, StringType, ListType, BooleanType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


'''
TRAIL
'''
class Trail(AWSCloudService):
    name = StringType(deserialize_from="Name", serialize_when_none=False)
    s3_bucket_name = StringType(deserialize_from="S3BucketName", serialize_when_none=False)
    s3_key_prefix = StringType(deserialize_from="S3KeyPrefix", serialize_when_none=False)
    sns_topic_name = StringType(deserialize_from="SnsTopicName", serialize_when_none=False)
    sns_topic_arn = StringType(deserialize_from="SnsTopicARN", serialize_when_none=False)
    include_global_service_events = BooleanType(deserialize_from="IncludeGlobalServiceEvents", serialize_when_none=False)
    is_multi_region_trail = BooleanType(deserialize_from="IsMultiRegionTrail", serialize_when_none=False)
    home_region = StringType(deserialize_from="HomeRegion", serialize_when_none=False)
    trail_arn = StringType(deserialize_from="TrailARN", serialize_when_none=False)
    log_file_validation_enabled = BooleanType(deserialize_from="LogFileValidationEnabled", serialize_when_none=False)
    cloud_watch_logs_log_group_arn = StringType(deserialize_from="CloudWatchLogsLogGroupArn", serialize_when_none=False)
    cloud_watch_logs_role_arn = StringType(deserialize_from="CloudWatchLogsRoleArn", serialize_when_none=False)
    kms_key_id = StringType(deserialize_from="KmsKeyId", serialize_when_none=False)
    has_custom_event_selectors = BooleanType(deserialize_from="HasCustomEventSelectors", serialize_when_none=False)
    has_insight_selectors = BooleanType(deserialize_from="HasInsightSelectors", serialize_when_none=False)
    is_organization_trail = BooleanType(deserialize_from="IsOrganizationTrail", serialize_when_none=False)
    s3_bucket_mfa_delete = BooleanType(default=False)
    s3_bucket_encryption = BooleanType(default=False)
    s3_bucket_public = BooleanType(default=False)

    def reference(self):
        return {
            "resource_id": self.trail_arn,
            "external_link": f"https://console.aws.amazon.com/cloudtrail/home?region={self.home_region}#/configuration/{self.trail_arn.replace('/', '@')}"
        }
