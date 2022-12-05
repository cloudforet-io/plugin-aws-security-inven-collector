from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType
from spaceone.inventory.libs.schema.resource import AWSCloudService
from spaceone.inventory.conf.cloud_service_conf import *


class SecurityCheckRule(Model):
    name = StringType(default='')
    status = StringType(choices=('PASS', 'FAILED'))
    fail_reason = StringType(default='')


class IAMCredential(AWSCloudService):
    user = StringType()
    status = StringType(choices=('PASS', 'FAILED'))
    rules = ListType(ModelType(SecurityCheckRule), default=[])
    arn = StringType()
    user_creation_time = DateTimeType(serialize_when_none=False)
    password_enabled = StringType(serialize_when_none=False)
    password_last_used = StringType(serialize_when_none=False)
    password_last_changed = StringType(serialize_when_none=False)
    password_next_rotation = StringType(serialize_when_none=False)
    mfa_active = StringType(serialize_when_none=False)
    access_key_1_active = StringType(serialize_when_none=False)
    access_key_1_last_rotated = StringType(serialize_when_none=False)
    access_key_1_last_used_date = StringType(serialize_when_none=False)
    access_key_1_last_used_region = StringType(serialize_when_none=False)
    access_key_1_last_used_service = StringType(serialize_when_none=False)
    access_key_2_active = StringType(serialize_when_none=False)
    access_key_2_last_rotated = StringType(serialize_when_none=False)
    access_key_2_last_used_date = StringType(serialize_when_none=False)
    access_key_2_last_used_region = StringType(serialize_when_none=False)
    access_key_2_last_used_service = StringType(serialize_when_none=False)
    cert_1_active = StringType(serialize_when_none=False)
    cert_1_last_rotated = StringType(serialize_when_none=False)
    cert_2_active = StringType(serialize_when_none=False)
    cert_2_last_rotated = StringType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/iam/home?region={DEFAULT_REGION}#/users/{self.user}"
        }
