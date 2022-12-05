from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cloudtrail.data import Trail
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


# TAB - BASE
meta_base = ItemDynamicLayout.set_fields('Trails', fields=[
    TextDyField.data_source('Trail Name', 'data.name'),
    TextDyField.data_source('Trail ARN', 'data.trail_arn'),
    TextDyField.data_source('Home Region', 'data.home_region'),
    EnumDyField.data_source('Multi-Region Trail', 'data.is_multi_region_trail', default_badge={
        'indigo.500': ['true'], 'coral.500': ['false']
    }),
    EnumDyField.data_source('Log file Validation Enabled', 'data.log_file_validation_enabled', default_badge={
        'indigo.500': ['true'], 'coral.500': ['false']
    }),
    TextDyField.data_source('KMS Key ID', 'data.kms_key_id'),
    TextDyField.data_source('S3 Bucket', 'data.s3_bucket_name'),
    TextDyField.data_source('S3 Key Prefix', 'data.s3_key_prefix'),
    EnumDyField.data_source('S3 Bucket Public', 'data.s3_bucket_public', default_badge={
        'indigo.500': ['true'], 'coral.500': ['false']
    }),
    EnumDyField.data_source('S3 Bucket MFA Delete Enabled', 'data.s3_bucket_mfa_delete', default_badge={
        'indigo.500': ['true'], 'coral.500': ['false']
    }),
    EnumDyField.data_source('S3 Bucket Encryption', 'data.s3_bucket_encryption', default_badge={
        'indigo.500': ['true'], 'coral.500': ['false']
    }),
    TextDyField.data_source('SNS Topic', 'data.sns_topic_name'),
    TextDyField.data_source('SNS Topic ARN', 'data.sns_topic_arn'),
    TextDyField.data_source('CloudWatch Logs Log group', 'data.cloud_watch_logs_log_group_arn'),
    TextDyField.data_source('CloudWatch Logs Role ARN', 'data.cloud_watch_logs_role_arn'),
    TextDyField.data_source('Include Global Service Events', 'data.include_global_service_events', options={
        'is_optional': True
    })
])

compliance_rules_meta = TableDynamicLayout.set_fields('Rules', 'data.rules', fields=[
    TextDyField.data_source('Rule Name', 'name'),
    EnumDyField.data_source('Status', 'status', default_badge={
        'indigo.500': ['PASS'], 'coral.500': ['FAILED']
    }),
    TextDyField.data_source('Fail Reason', 'fail_reason')
])

metadata = CloudServiceMeta.set_layouts([meta_base, compliance_rules_meta])


class CloudTrailResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compliance')


class TrailResource(CloudTrailResource):
    cloud_service_type = StringType(default='EventLogging')
    data = ModelType(Trail)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class TrailResponse(CloudServiceResponse):
    resource = PolyModelType(TrailResource)
