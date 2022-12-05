import os
from spaceone.inventory.libs.utils import get_data_from_yaml
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
failed_count_conf = os.path.join(current_dir, 'widget/failed_count.yaml')

cst_trail = CloudServiceTypeResource()
cst_trail.name = 'EventLogging'
cst_trail.group = 'Compliance'
cst_trail.provider = 'aws'
cst_trail.labels = ['Security']
cst_trail.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudtrail.svg',
    'spaceone:display_name': 'EventLogging'
}

cst_trail._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        EnumDyField.data_source('Status', 'data.status', default_badge={
            'indigo.500': ['PASS'],
            'coral.500': ['FAILED']
        }),
        TextDyField.data_source('Home Region', 'data.home_region'),
        TextDyField.data_source('Multi-Region Trail', 'data.is_multi_region_trail'),
        TextDyField.data_source('S3 Bucket', 'data.s3_bucket_name'),
        TextDyField.data_source('Log file Validation Enabled', 'data.log_file_validation_enabled'),
        TextDyField.data_source('S3 Bucket Public', 'data.s3_bucket_public'),
        TextDyField.data_source('S3 Bucket MFA Delete Enabled', 'data.s3_bucket_mfa_delete'),
        TextDyField.data_source('S3 Bucket Encryption', 'data.s3_bucket_encryption'),
        TextDyField.data_source('KMS Key ID', 'data.kms_key_id'),
        # For Dynamic Table
        TextDyField.data_source('Log file Prefix', 'data.s3_key_prefix', options={
            'is_optional': True
        }),
        TextDyField.data_source('Trail ARN', 'data.trail_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('CloudWatch Logs Log group', 'data.cloud_watch_logs_log_group_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('SNS Topic name', 'data.sns_topic_name', options={
            'is_optional': True
        }),
        TextDyField.data_source('SNS Topic ARN', 'data.sns_topic_arn', options={
            'is_optional': True
        }),
        TextDyField.data_source('Include Global Service Events', 'data.include_global_service_events', options={
            'is_optional': True
        }),
        TextDyField.data_source('AWS Account ID', 'account', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ARN', key='data.trail_arn'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Home Region', key='data.home_region'),
        SearchField.set(name='Multi-Region Trail', key='data.is_multi_region_trail', data_type='boolean'),
        SearchField.set(name='S3 Bucket', key='data.s3_bucket_name'),
        SearchField.set(name='Log file Validation Enabled', key='data.log_file_validation_enabled',
                        data_type='boolean'),
        SearchField.set(name='S3 Bucket Public', key='data.s3_bucket_public', data_type='boolean'),
        SearchField.set(name='S3 Bucket MFA Delete Enabled', key='data.s3_bucket_mfa_delete', data_type='boolean'),
        SearchField.set(name='S3 Bucket Encryption', key='data.s3_bucket_encryption', data_type='boolean'),
        SearchField.set(name='AWS Account ID', key='account')
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(failed_count_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_trail})
]
