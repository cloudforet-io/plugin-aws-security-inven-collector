from schematics.types import ModelType, StringType, PolyModelType, FloatType, DateTimeType

from spaceone.inventory.model.iam_credential_report.data import IAMCredential
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField, SizeField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout,ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


# TAB - Default
iam_cred_info_meta = ItemDynamicLayout.set_fields('Disks', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('User ARN', 'data.arn'),
])

iam_cred_meta = CloudServiceMeta.set_layouts([iam_cred_info_meta])


class ComputeResource(CloudServiceResource):
    cloud_service_group = StringType(default='Compliance')


class IAMCredentialResource(ComputeResource):
    cloud_service_type = StringType(default='RootUserSecurity')
    data = ModelType(IAMCredential)
    _metadata = ModelType(CloudServiceMeta, default=iam_cred_meta, serialized_name='metadata')
    name = StringType()
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)


class IAMCredentialResponse(CloudServiceResponse):
    resource = PolyModelType(IAMCredentialResource)
