from schematics.types import ModelType, StringType, PolyModelType, FloatType

from spaceone.inventory.model.iam_credential_report.data import IAMCredential
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


# TAB - Default
iam_cred_info_meta = ItemDynamicLayout.set_fields('IAM User', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Status', 'data.status', default_badge={
        'indigo.500': ['PASS'],
        'coral.600': ['FAILED']
    }),
    TextDyField.data_source('User ARN', 'data.arn'),
    DateTimeDyField.data_source('User Created', 'data.user_creation_time'),
    TextDyField.data_source('Password Enabled', 'data.password_enabled'),
    TextDyField.data_source('MFA Active', 'data.mfa_active'),
    TextDyField.data_source('Access Key 1 Active', 'data.access_key_1_active'),
    TextDyField.data_source('Access Key 2 Active', 'data.access_key_2_active'),
    DateTimeDyField.data_source('Password Last Used', 'data.password_last_used'),
    DateTimeDyField.data_source('Password Last Changed', 'data.password_last_changed'),
    TextDyField.data_source('Password Next Rotation', 'data.password_next_rotation'),
    TextDyField.data_source('Access Key 1 Active', 'data.access_key_1_active'),
    DateTimeDyField.data_source('Access Key 1 Rotated', 'data.access_key_1_last_rotated'),
    DateTimeDyField.data_source('Access Key 1 Used Date', 'data.access_key_1_last_used_date'),
    TextDyField.data_source('Access Key 1 Last Used Region', 'data.access_key_1_last_used_region'),
    TextDyField.data_source('Access Key 1 Last Used Service', 'data.access_key_1_last_used_service'),
    TextDyField.data_source('Access Key 2 Active', 'data.access_key_2_active'),
    DateTimeDyField.data_source('Access Key 2 Rotated', 'data.access_key_2_last_rotated'),
    DateTimeDyField.data_source('Access Key 2 Used Date', 'data.access_key_2_last_used_date'),
    TextDyField.data_source('Access Key 2 Last Used Region', 'data.access_key_2_last_used_region'),
    TextDyField.data_source('Access Key 2 Last Used Service', 'data.access_key_2_last_used_service'),
    TextDyField.data_source('Cert 1 Active', 'data.cert_1_active'),
    DateTimeDyField.data_source('Cert 1 Last Rotated', 'data.cert_1_last_rotated'),
    TextDyField.data_source('Cert 2 Active', 'data.cert_2_active'),
    DateTimeDyField.data_source('Cert 2 Last Rotated', 'data.cert_2_last_rotated'),
])

compliance_rules_meta = TableDynamicLayout.set_fields('Rules', 'data.rules', fields=[
    TextDyField.data_source('Rule Name', 'name'),
    EnumDyField.data_source('Status', 'status', default_badge={
        'indigo.500': ['PASS'], 'coral.600': ['FAILED']
    }),
    TextDyField.data_source('Fail Reason', 'fail_reason')
])

iam_cred_meta = CloudServiceMeta.set_layouts([iam_cred_info_meta, compliance_rules_meta])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compliance')


class IAMCredentialResource(ComputeResource):
    cloud_service_type = StringType(default='UserSecurity')
    data = ModelType(IAMCredential)
    _metadata = ModelType(CloudServiceMeta, default=iam_cred_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class IAMCredentialResponse(CloudServiceResponse):
    resource = PolyModelType(IAMCredentialResource)
