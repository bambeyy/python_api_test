import allure
from helpers.api.client import HttpClient
from settings import config


class UserAPI(object):
    API_HOST = config.get('api_host')

    def __init__(self):
        self._http_client = HttpClient(api_host=self.API_HOST)

    @allure.step
    def get_groups_tariffs(self):
        return self._http_client.request('/tariffs/groups', method='GET')

    @allure.step
    def get_tariffs(self, IdTariffGroup):
        if IdTariffGroup:
            data = {"IdTariffGroup": IdTariffGroup}
        else:
            data = {}
        return self._http_client.request('/tariffs/groups/' + str(IdTariffGroup), method='GET', data=data)

    @allure.step
    def get_create_preorder(self, data):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return self._http_client.request('/preorder/create', method='POST', data=data, headers=headers)

    @allure.step
    def get_list_partners(self):
        return self._http_client.request('/public/Partners', method='GET')


user_api = UserAPI()
