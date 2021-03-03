import pytest
import json
import os

from settings import server_settings


def pytest_addoption(parser):
    """
    Additional command line options
    :param parser: command line parser
    """
    # Test categorisation
    parser.addoption('--categories', action='store', metavar='NAME',
                     help='only run tests matches with categories')


def config(request):
    server_settings.SERVER = request.config.getoption("--server")


def pytest_configure(config):
    """
    Register an additional marker in pytest.ini
    :param config: pytest.ini
    """
    config.addinivalue_line('markers',
                            'categories(params): mark the test (ex. suite=sanity, severity=critical, component=cart)')


def pytest_collection_modifyitems(session, config, items):
    """
    Skip tests, which  not satisfying categories param
    :param session: Current session
    :param config: pytest.ini
    :param items: all founded tests
    :return: tests, which satisfy 'categories' param
    """
    market_categories = config.option.categories
    if not market_categories or market_categories == 'all':
        return

    categories_filter = dict(x.split('=') for x in market_categories.split(','))
    if not categories_filter:
        return

    selected = []
    deselected = []
    for item in items:
        markers_on_tests = item.get_marker('categories')
        if not markers_on_tests:
            deselected.append(item)
            continue

        found = False
        for category_filter in categories_filter:
            if not markers_on_tests.kwargs.get(category_filter):
                deselected.append(item)
                found = True
                break

            if categories_filter[category_filter] not in markers_on_tests.kwargs.get(category_filter):
                deselected.append(item)
                found = True
                break

        if not found:
            selected.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    """ This method use for accessing test execution info (failed, passed, skipped, etc)
    Uses for pytest fixtures """
    # execute all other hooks to obtain the report object
    rep = __multicall__.execute()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def test_data(request):
    return request.param


def pytest_generate_tests(metafunc):
    if 'test_data' in metafunc.fixturenames:
        testdata = get_test_data('tariffs.json')
        metafunc.parametrize('test_data', testdata, indirect=True)


def get_test_data(filename):
    folder_path = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(folder_path, 'Data')
    jsonfile = os.path.join(folder, filename)
    with open(jsonfile) as file:
        data = json.load(file)
    valid_data = [(item, 1) for item in data]
    data = valid_data
    return data