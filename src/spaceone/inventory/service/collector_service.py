import time
import logging
import concurrent.futures
from spaceone.inventory.libs.manager import AWSManager
from spaceone.core.service import *
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params.get('options', {})
        secret_data = params.get('secret_data', {})
        aws_manager = AWSManager()
        aws_manager.verify(options, secret_data)
        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def collect(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        start_time = time.time()
        secret_data = params.get('secret_data', {})
        aws_manager = AWSManager()
        params.update({'account_id': aws_manager.get_aws_account(secret_data)})

        _LOGGER.debug("[ EXECUTOR START: Security Compliance cloud service ]")

        # Thread per cloud services
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []

            for execute_manager in CLOUD_SERVICE_MANAGERS:
                _LOGGER.info(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, params))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    yield result

        '''
        for manager in self.execute_managers:
            _LOGGER.debug(f'@@@ {manager} @@@')
            _manager = self.locator.get_manager(manager)

            for resource in _manager.collect_resources(params):
                yield resource.to_primitive()
        '''
        _LOGGER.debug(f'TOTAL TIME : {time.time() - start_time} Seconds')
