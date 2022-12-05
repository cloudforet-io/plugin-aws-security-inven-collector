CONNECTORS = {
    'AWSConnector': {
        'backend': 'spaceone.inventory.libs.connector.AWSConnector',
    },
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'Collector.collect': [
                    'secret_data'
                ]
            }
        }
    }
}

HANDLERS = {
}

ENDPOINTS = {
}
