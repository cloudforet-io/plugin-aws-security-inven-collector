import os
from spaceone.inventory.libs.utils import get_data_from_yaml
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yaml')
failed_count_conf = os.path.join(current_dir, 'widget/failed_count.yaml')

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
            'coral.500': ['FAILED']
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
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Password Enabled', key='data.password_enabled'),
        SearchField.set(name='MFA Active', key='data.mfa_active'),
        SearchField.set(name='Password Last Used', key='data.password_last_used', data_type='datetime'),
        SearchField.set(name='Password Last Changed', key='data.password_last_changed', data_type='datetime'),
        SearchField.set(name='Password Next Rotation', key='data.password_next_rotation', data_type='datetime'),
        SearchField.set(name='Access Key 1 Active', key='data.access_key_1_active'),
        SearchField.set(name='Access Key 1 Rotated', key='data.access_key_1_last_rotated', data_type='datetime'),
        SearchField.set(name='Access Key 1 Used Date', key='data.access_key_1_last_used_date', data_type='datetime'),
        SearchField.set(name='Access Key 1 Used Region', key='data.access_key_1_last_used_region',
                        data_type='datetime'),
        SearchField.set(name='Access Key 1 Used Service', key='data.access_key_1_last_used_service',
                        data_type='datetime'),
        SearchField.set(name='Access Key 2 Active', key='data.access_key_2_active'),
        SearchField.set(name='Access Key 2 Rotated', key='data.access_key_2_last_rotated', data_type='datetime'),
        SearchField.set(name='Access Key 2 Used Date', key='data.access_key_2_last_used_date', data_type='datetime'),
        SearchField.set(name='Access Key 2 Used Region', key='data.access_key_2_last_used_region',
                        data_type='datetime'),
        SearchField.set(name='Access Key 2 Used Service', key='data.access_key_2_last_used_service',
                        data_type='datetime'),
        SearchField.set(name='Cert 1 Active', key='data.cert_1_active'),
        SearchField.set(name='Cert 1 Last Rotated', key='data.cert_1_last_rotated', data_type='datetime'),
        SearchField.set(name='Cert 2 Active', key='data.cert_2_active'),
        SearchField.set(name='Cert 2 Last Rotated', key='data.cert_2_last_rotated', data_type='datetime'),
        SearchField.set(name='User Created', key='data.user_creation_time', data_type='datetime'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(failed_count_conf))
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_iam_cred})
]
