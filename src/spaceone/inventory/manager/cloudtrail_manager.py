import time
import logging
from spaceone.inventory.libs.manager import AWSManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.cloudtrail import CloudTrailConnector, S3Connector
from spaceone.inventory.model.cloudtrail.data import Trail
from spaceone.inventory.model.cloudtrail.cloud_service import TrailResource, TrailResponse
from spaceone.inventory.model.cloudtrail.cloud_service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.conf.cloud_service_conf import *


__all__ = ['CloudTrailManager']

_LOGGER = logging.getLogger(__name__)


class CloudTrailManager(AWSManager):
    connector_name = 'CloudTrailConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        """
            Args:
                params (dict):
                    - 'options' : 'dict'
                    - 'secret_data' : 'dict'
                    - 'account_id': 'str'
            Response:
                CloudServiceResponse (list) : dictionary of Cloud Trail resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug("** Cloud Trail START **")
        s3_connector_name = 'S3Connector'
        start_time = time.time()

        trail_conn: CloudTrailConnector = self.locator.get_connector(self.connector_name, **params)
        trail_responses = []
        error_responses = []
        trail_name = ''

        s3_conn: S3Connector = self.locator.get_connector(s3_connector_name, **params)

        for trail in trail_conn.describe_trails():
            try:
                trail_name = trail.get('Name')
                s3_bucket_name = trail.get('S3BucketName')

                versioning_info = s3_conn.get_bucket_versioning(s3_bucket_name)
                bucket_encryption_info = s3_conn.get_bucket_encryption(s3_bucket_name)
                policy_status_info = s3_conn.get_bucket_policy_status(s3_bucket_name)

                if versioning_info.get('MFADelete') and versioning_info['MFADelete'] == 'Enabled':
                    trail.update({'s3_bucket_mfa_delete': True})

                for _rule in bucket_encryption_info.get('Rules', []):
                    if _rule.get('BucketKeyEnabled'):
                        trail.update({'s3_bucket_encryption': True})

                if policy_status_info.get('IsPublic'):
                    trail.update({'s3_bucket_public': True})

                self.check_compliance(trail)

                trail_data = Trail(trail, strict=False)
                trail_resource = TrailResource({
                    'data': trail_data,
                    'region_code': trail.get('HomeRegion'),
                    'reference': ReferenceModel(trail_data.reference()),
                    'name': trail_name,
                    'account': params.get('account_id')
                })
                trail_responses.append(TrailResponse({'resource': trail_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] {trail_name} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Compliance', 'CloudTrail',
                                                                                trail_name)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** Cloud Trail Finished {time.time() - start_time} Seconds **')
        return trail_responses, error_responses

    def check_compliance(self, trail):
        total_compliance_status = 'PASS'

        rules = [
            self.check_multi_region(trail),
            self.check_log_file_validation(trail),
            self.check_s3_bucket_access(trail),
            self.check_s3_bucket_mfa_delete(trail),
            self.check_s3_bucket_encryption(trail)
        ]

        for rule in rules:
            if rule.get('status') != 'PASS':
                total_compliance_status = 'FAILED'
                break

        trail.update({
            'status': total_compliance_status,
            'rules': rules
        })

    @staticmethod
    def check_multi_region(trail):
        report = {
            'name': 'Multi Region Trail Enabled',
            'status': 'FAILED',
            'fail_reason': ''
        }

        if trail.get('IsMultiRegionTrail'):
            report.update({'status': 'PASS'})
        else:
            report.update({'fail_reason': 'Cloud Trail Multi Region setting must be enabled.'})

        return report

    @staticmethod
    def check_log_file_validation(trail):
        report = {
            'name': 'Log file Validation Enabled',
            'status': 'FAILED',
            'fail_reason': ''
        }

        if trail.get('LogFileValidationEnabled'):
            report.update({'status': 'PASS'})
        else:
            report.update({'fail_reason': 'Log file validation setting must be enabled.'})

        return report

    @staticmethod
    def check_s3_bucket_access(trail):
        report = {
            'name': 'S3 Bucket Access',
            'status': 'FAILED',
            'fail_reason': ''
        }

        if trail.get('s3_bucket_public') is False:
            report.update({'status': 'PASS'})
        else:
            report.update({'fail_reason': 'S3 Bucket of Cloud Trail must be blocked public access.'})

        return report

    @staticmethod
    def check_s3_bucket_mfa_delete(trail):
        report = {
            'name': 'S3 Bucket MFA Delete Enabled',
            'status': 'FAILED',
            'fail_reason': ''
        }

        if trail.get('s3_bucket_mfa_delete'):
            report.update({'status': 'PASS'})
        else:
            report.update({'fail_reason': 'S3 Bucket of Cloud Trail must be MFA delete enabled.'})

        return report

    @staticmethod
    def check_s3_bucket_encryption(trail):
        report = {
            'name': 'S3 Bucket SSE (Server-Side Encryption)',
            'status': 'FAILED',
            'fail_reason': ''
        }

        if trail.get('s3_bucket_encryption'):
            report.update({'status': 'PASS'})
        else:
            report.update({'fail_reason': 'S3 Bucket of Cloud Trail must be enable SSE(Server-Side Encryption).'})

        return report

