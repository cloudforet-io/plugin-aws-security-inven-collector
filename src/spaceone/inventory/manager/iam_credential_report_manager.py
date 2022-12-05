import time
import datetime
from dateutil import parser
import logging
import csv
from io import StringIO
from spaceone.inventory.libs.manager import AWSManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.iam_credential_report import IAMCredentialReportConnector
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.inventory.model.iam_credential_report.data import IAMCredential
from spaceone.inventory.model.iam_credential_report.cloud_service import IAMCredentialResource, IAMCredentialResponse
from spaceone.inventory.model.iam_credential_report.cloud_service_type import CLOUD_SERVICE_TYPES

__all__ = ['IAMCredentialReportManager']
_LOGGER = logging.getLogger(__name__)


class IAMCredentialReportManager(AWSManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cloud_service_types = CLOUD_SERVICE_TYPES
        self.connector_name = 'IAMCredentialReportConnector'

    def collect_cloud_service(self, params):
        """
            Args:
                params (dict):
                    - 'options' : 'dict'
                    - 'secret_data' : 'dict'
                    - 'account_id': 'str'
            Response:
                CloudServiceResponse (list) : dictionary of IAM Credential Report resource information
                ErrorResourceResponse (list) : list of error resource information

        """
        _LOGGER.debug("** IAM Credential Report START **")
        start_time = time.time()

        iam_cred_conn: IAMCredentialReportConnector = self.locator.get_connector(self.connector_name, **params)
        iam_cred_responses = []
        error_responses = []
        iam_user = ''

        iam_credential_report_b64 = iam_cred_conn.get_credential_report()
        iam_credential_report_csv = iam_credential_report_b64.decode()

        iam_cred_reports = self.convert_csv_to_dict(iam_credential_report_csv)

        for iam_cred in iam_cred_reports:
            try:
                self.check_compliance(iam_cred)
                iam_user = iam_cred.get('user')
                iam_credential_data = IAMCredential(iam_cred, strict=False)
                iam_credential_resource = IAMCredentialResource({
                    'data': iam_credential_data,
                    'region_code': 'global',
                    'reference': ReferenceModel(iam_credential_data.reference()),
                    'name': iam_user,
                    'account': params.get('account_id')
                })
                iam_cred_responses.append(IAMCredentialResponse({'resource': iam_credential_resource}))

            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] {iam_user} {e}', exc_info=True)
                error_resource_response = self.generate_resource_error_response(e, 'Compliance', 'IAMCredential',
                                                                                iam_user)
                error_responses.append(error_resource_response)

        _LOGGER.debug(f'** IAM Credential Report Finished {time.time() - start_time} Seconds **')
        return iam_cred_responses, error_responses

    def check_compliance(self, iam_cred):
        total_compliance_status = 'PASS'
        utcnow = datetime.datetime.utcnow()

        # Root User Security
        if iam_cred.get('user') == '<root_account>':
            rules_result = self.check_root_user_security(iam_cred, utcnow)
        else:
            rules_result = self.iam_user_security(iam_cred, utcnow)

        for rule in rules_result:
            if rule.get('status') != 'PASS':
                total_compliance_status = 'FAILED'
                break

        iam_cred.update({
            'status': total_compliance_status,
            'rules': rules_result
        })

    def check_root_user_security(self, iam_cred, utcnow):
        user = iam_cred.get('user')

        rules = [
            self.check_password_used(user, iam_cred, utcnow),
            self.check_mfa_active(user, iam_cred),
            self.check_access_key_used(user, iam_cred, utcnow),
        ]

        return rules

    def iam_user_security(self, iam_cred, utcnow):
        user = iam_cred.get('user')

        rules = [
            self.check_password_used(user, iam_cred, utcnow),
            self.check_mfa_active(user, iam_cred),
            self.check_access_key_used(user, iam_cred, utcnow),
        ]

        return rules

    @staticmethod
    def check_password_used(user, iam_cred, now):
        report = {
            'name': 'Password Changed',
            'status': 'FAILED',
            'fail_reason': ''
        }

        if iam_cred.get('password_enabled') in ['not_supported', 'false']:
            report.update({'status': 'PASS'})
        else:
            last_changed = iam_cred.get('password_last_changed')

            if last_changed == 'not_supported':
                report.update({'status': 'PASS'})
            else:
                last_changed = parser.parse(last_changed)
                now = now.replace(tzinfo=None)
                last_changed = last_changed.replace(tzinfo=None)

                time_diff = now - last_changed

                if time_diff.days > COMPLIANCE_PASSWORD_LAST_CHANGED:
                    report['fail_reason'] = f'User "{user}" has been {time_diff.days} days since the last password change. ' \
                                            f'The last password change date must be within {COMPLIANCE_PASSWORD_LAST_CHANGED} days.'
                else:
                    report['status'] = 'PASS'

        return report

    def check_mfa_active(self, user, iam_cred):
        report = {
            'name': 'MFA Activated',
            'status': 'FAILED',
            'fail_reason': ''
        }

        password_enabled = iam_cred.get('password_enabled')
        mfa_active = iam_cred.get('mfa_active')

        if user == '<root_account>':
            report = self._check_mfa(user, mfa_active, report)
        else:
            if password_enabled in ['true']:
                report = self._check_mfa(user, mfa_active, report)
            else:
                report['status'] = 'PASS'

        return report

    @staticmethod
    def _check_mfa(user, mfa_active, report):
        if mfa_active == 'true':
            report['status'] = 'PASS'
        else:
            report['fail_reason'] = f'User "{user}" must enable the MFA active to log in to the AWS Console'

        return report

    def check_access_key_used(self, user, iam_cred, now):
        access_key_1_active = iam_cred.get('access_key_1_active')
        access_key_2_active = iam_cred.get('access_key_2_active')

        report = {
            'name': 'AccessKey Activated',
            'status': 'FAILED',
            'fail_reason': ''
        }

        if user == '<root_account>':
            if access_key_1_active == 'false' and access_key_2_active == 'false':
                report.update({'status': 'PASS'})
            else:
                report['fail_reason'] = f'User "{user}" must not used the Access Key'
        else:
            if access_key_1_active == 'true':
                access_key_1_last_rotated = iam_cred.get('access_key_1_last_rotated')
                report = self._check_access_key(access_key_1_last_rotated, now, report)
            else:
                report.update({'status': 'PASS'})

            if access_key_2_active == 'true':
                access_key_2_last_rotated = iam_cred.get('access_key_2_last_rotated')
                report = self._check_access_key(access_key_2_last_rotated, now, report)
            else:
                report.update({'status': 'PASS'})

        return report

    @staticmethod
    def _check_access_key(access_key_last_rotated, now, report):
        if access_key_last_rotated == 'N/A':
            report['fail_reason'] = f'Access key must be replaced periodically within {COMPLIANCE_ACCESSKEY_ROTATED} days.'
        else:
            access_key_last_rotated = parser.parse(access_key_last_rotated)
            now = now.replace(tzinfo=None)
            last_rotated = access_key_last_rotated.replace(tzinfo=None)

            time_diff = now - last_rotated

            if time_diff.days > COMPLIANCE_ACCESSKEY_ROTATED:
                report['fail_reason'] = f'Access key must be replaced periodically within {COMPLIANCE_ACCESSKEY_ROTATED} days.'
            else:
                report['status'] = 'PASS'

        return report

    @staticmethod
    def convert_csv_to_dict(raw_csv):
        csv_text = StringIO(raw_csv)
        reader = csv.DictReader(csv_text, delimiter=',')

        return [row for row in reader]
