import os
from spaceone.inventory.libs.utils import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

"""
IAM Credential
"""
cst_iam_cred = CloudServiceTypeResource()
cst_iam_cred.name = 'RootUserSecurity'
cst_iam_cred.group = 'Compliance'
cst_iam_cred.provider = 'aws'
cst_iam_cred.labels = ['Security']
cst_iam_cred.is_major = True
cst_iam_cred.is_primary = True
cst_iam_cred.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Identity-and-Access-Management_IAM.svg',
    'spaceone:display_name': 'RootUserSecurity'
}

cst_iam_cred._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ARN', 'data.arn'),
        DateTimeDyField.data_source('User Created', 'data.user_creation_time')
    ],
    search=[
        SearchField.set(name='ARN', key='data.arn'),
        SearchField.set(name='User Created', key='data.user_creation_time', data_type='datetime'),
    ]
)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_iam_cred})
]
