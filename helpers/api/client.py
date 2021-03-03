import requests
import json
from helpers import utils
from helpers.logger import logger
from requests.auth import HTTPBasicAuth


class HttpClient(object):

    def __init__(self, api_host, timeout=120):
        self.api_host = api_host
        self.timeout = timeout

    def request(self, endpoint, method='POST', data=None, headers=None, cookies=None, verify=None):
        url = '%s%s' % (self.api_host, endpoint)
        data = data or dict()
        cookies = cookies or dict()
        headers = headers or dict()
        verify = False
        headers["content-type"] = "application/json"
        request_kwargs = dict(method=method, url=url, headers=headers, timeout=self.timeout, cookies=cookies,
                              verify=verify)

        if method in ('POST', 'PUT'):
            request_kwargs['data'] = json.dumps(data)
        else:
            request_kwargs['params'] = data
        requests.packages.urllib3.disable_warnings()
        response = requests.request(**request_kwargs, auth=HTTPBasicAuth('m.ganin@isoit.ru', 'Ganina'))
        self.write_log(**request_kwargs)

        if not str(response.status_code).startswith('2'):
            logger.warning('We have got response code %s with message %s' % (response.status_code, response.content))
            utils.allure_attach('Bad status code', 'Status code:%s\n\nError message:\n%s\n' % (response.status_code,
                                                                                               response.content))

        return response

    @staticmethod
    def write_log(url, **kwargs):
        as_curl = utils.request_as_curl(url,
                                        method=kwargs.get('method'),
                                        data=kwargs.get('Data'),
                                        params=kwargs.get('params'),
                                        headers=kwargs.get('headers'),
                                        cookies=kwargs.get('cookies'),
                                        verify=kwargs.get('verify'))

        utils.allure_attach('curl', as_curl)
        logger.debug(as_curl)
