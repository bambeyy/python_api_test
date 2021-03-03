import json
import allure
import pytest
from requests import request
from helpers.api.user import user_api

preorder_json_file = 'Data/preorder.json'


@allure.feature('Test')
class TestAPI(object):

    # test GET /tariffs/groups
    def test_group_tariffs(self):
        response = user_api.get_groups_tariffs()
        assert response.status_code == 200, 'Expected 200 status_code, but actual is %d' % response.status_code
        with open('Data/tariffs.json', 'w') as file:
            json.dump(response.json(), file)
        response = response.json()
        assert len(response) > 0, 'Expected at least 1 argument, but actual is %s' % len(response)
        assert isinstance(response, list), 'Expected `list` response object type, but actual is %s' % type(response)

    # test GET /tariffs/groups/{groupId}
    def test_tariffs(self, test_data):
        IdTariffGroup = test_data[0]["IdTariffGroup"]
        response = user_api.get_tariffs(IdTariffGroup)
        assert response.status_code == 200, 'Expected 200 status_code, but actual is %d' % response.status_code
        response = response.json()
        assert isinstance(response, list), 'Expected `list` response object type, but actual is %s' % type(response)

    # test POST /preorder/create
    def test_create_preorder(self):
        with open(preorder_json_file, 'r', encoding='utf-8') as json_data:
            data = json.load(json_data)
        response = user_api.get_create_preorder(data)
        assert response.status_code == 200, 'Expected 200 status_code, but actual is %d' % response.status_code
        response = response.json()
        assert len(response) > 0, 'Expected at least 1 argument , but actual is %s' % len(response)
        assert isinstance(response, str), 'Expected `Str` response object type, but actual is %s' % type(response)

    # test GET /public/Partners
    def test_list_partners(self):
        response = user_api.get_list_partners()
        assert response.status_code == 200, 'Expected 200 status_code, but actual is %d' % response.status_code
        with open('Data/partners.json', 'w') as file:
            json.dump(response.json(), file)
        response = response.json()
        assert len(response) > 0, 'Expected at least 1 argument, but actual is %s' % len(response)
        assert isinstance(response, list), 'Expected `list` response object type, but actual is %s' % type(response)

