import pytest


@pytest.fixture(params=["chrome"], scope="class")
def driver_init(request):
    '''
        Config pytest for chrome and
    '''
    from selenium import webdriver
    if request.param == "chrome":
        web_driver = webdriver.Chrome(r'C:\Users\SaiPrasad\Downloads\chromedriver_win32\chromedriver.exe')

    request.cls.driver = web_driver
    request.cls.driver.implicitly_wait(15)
    request.cls.driver.maximize_window()
    yield
    web_driver.quit()

    request.addfinalizer(web_driver.quit)


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)
