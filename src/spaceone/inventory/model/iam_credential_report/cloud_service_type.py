import os
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
IAM Credential
"""
cst_iam_cred = CloudServiceTypeResource()
cst_iam_cred.name = 'UserSecurity'
cst_iam_cred.group = 'Compliance'
cst_iam_cred.provider = 'aws'
cst_iam_cred.labels = ['Security']
cst_iam_cred.is_major = True
cst_iam_cred.is_primary = True
cst_iam_cred.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Identity-and-Access-Management_IAM.svg',
    'spaceone:display_name': 'UserSecurity'
}

cst_iam_cred._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ARN', 'data.arn'),
        DateTimeDyField.data_source('User Created', 'data.user_creation_time'),
        EnumDyField.data_source('Status', 'data.status', default_badge={
            'indigo.500': ['PASS'],
            'coral.600': ['FAILED']
        }),
        TextDyField.data_source('Password Enabled', 'data.password_enabled'),
        TextDyField.data_source('MFA Active', 'data.mfa_active'),
        TextDyField.data_source('Access Key 1 Active', 'data.access_key_1_active'),
        TextDyField.data_source('Access Key 2 Active', 'data.access_key_2_active'),
        DateTimeDyField.data_source('Password Last Used', 'data.password_last_used', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Password Last Changed', 'data.password_last_changed', options={
            'is_optional': True
        }),
        TextDyField.data_source('Password Next Rotation', 'data.password_next_rotation', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Key 1 Active', 'data.access_key_1_active', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Access Key 1 Rotated', 'data.access_key_1_last_rotated', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Access Key 1 Used Date', 'data.access_key_1_last_used_date', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Key 1 Last Used Region', 'data.access_key_1_last_used_region', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Key 1 Last Used Service', 'data.access_key_1_last_used_service', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Key 2 Active', 'data.access_key_2_active', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Access Key 2 Rotated', 'data.access_key_2_last_rotated', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Access Key 2 Used Date', 'data.access_key_2_last_used_date', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Key 2 Last Used Region', 'data.access_key_2_last_used_region', options={
            'is_optional': True
        }),
        TextDyField.data_source('Access Key 2 Last Used Service', 'data.access_key_2_last_used_service', options={
            'is_optional': True
        }),
        TextDyField.data_source('Cert 1 Active', 'data.cert_1_active', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Cert 1 Last Rotated', 'data.cert_1_last_rotated', options={
            'is_optional': True
        }),
        TextDyField.data_source('Cert 2 Active', 'data.cert_2_active', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Cert 2 Last Rotated', 'data.cert_2_last_rotated', options={
            'is_optional': True
        }),
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='User Created', key='data.user_creation_time', data_type='datetime'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_iam_cred})
]
