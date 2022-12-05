MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []
DEFAULT_REGION = 'us-east-1'

CLOUD_SERVICE_MANAGERS = [
    'IAMCredentialReportManager',
    'CloudTrailManager'
]

COMPLIANCE_PASSWORD_LAST_CHANGED = 90
COMPLIANCE_ACCESSKEY_ROTATED = 90
