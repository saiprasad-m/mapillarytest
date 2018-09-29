import pytest
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from test.testobject.BaseTest import BaseTest
from test.pageobject.BasePage import BasePage

'''
    All the test data for seeding the elasticsearch index will be listed here.
    Prior to running the tests, you may have to drop the index "user" from elastic search 
    refer: api\dropindex.py (Crude way to remove indexes from elastic
'''

seeddata = [
    ("a", "a", "1900-01-01", "a street"),
    ("b", "b", "1900-01-01", "b street"),
    ("c", "c", "1900-01-01", "c street"),
    ("d", "d", "1900-01-01", "d street"),
    ("e", "e", "1900-01-01", "e street"),
]

testdata = [
    ("test1", "test1@test1.com", "1900-01-01", "test1 street"),
    ("test2", "test2@test2.com", "1900-02-02", "test2 street"),
    ("test3", "test3@test2.com", "1900-03-03", "test3 street"),
    ("test4", "test4@test2.com", "1900-04-04", "test4 street"),
]

search = [
    ("a", True),
    ("test1", False),
    ("e", True),
    ("test4", False),
]


@pytest.mark.incremental
class TestMappillary(BaseTest):

    @pytest.mark.parametrize("url", ["http://localhost:9100"])
    @pytest.allure.step("Launch Mapillary test webapp and check heading")
    def test_user_list_heading(self, url):
        basepage = BasePage()
        '''
            Using Pytest for parameterising the URL
        '''
        wait = WebDriverWait(self.driver, 15)
        self.driver.get(url)
        elem = basepage.heading
        wait.until(elem)
        assert self.driver.find_element(*elem.locator).is_displayed(), "Page heading displayed"

    @pytest.allure.step("Validate about the User List header")
    def test_user_list_table(self):
        basepage = BasePage()
        '''

        :return:
        '''
        wait = WebDriverWait(self.driver, 10)
        elem = basepage.userlist
        wait.until(elem)
        elem = self.driver.find_element(*elem.locator)
        text = elem.text
        print(text)
        with pytest.raises(AssertionError):
            assert text.strip() != "User List"

    @pytest.allure.step("Validate about the User List table headers")
    def test_user_list_table_columns(self):
        basepage = BasePage()
        '''
            Validate all the Table columns for UserList
        :return:
        '''
        wait = WebDriverWait(self.driver, 2)
        elem = basepage.column_header_number
        wait.until(elem)
        text = self.driver.find_element_by_tag_name("th")
        assert self.driver.find_element(*elem.locator).is_displayed(), "Numbering Column"
        elem = basepage.column_header_username
        assert self.driver.find_element(*elem.locator).is_displayed(), "Username Column"
        elem = basepage.column_header_email
        assert self.driver.find_element(*elem.locator).is_displayed(), "Email Column"
        elem = basepage.column_header_birthdate
        assert self.driver.find_element(*elem.locator).is_displayed(), "Birthdate Column"
        elem = basepage.column_header_address
        assert self.driver.find_element(*elem.locator).is_displayed(), "Address Column"


    @pytest.allure.step("Seeding the UserList with seed data")
    @pytest.mark.parametrize("username,email,birthdate,address", seeddata)
    def test_user_with_seed_data(self, username, email, birthdate, address):
        basepage = BasePage()
        '''

        :return:
        '''
        wait = WebDriverWait(self.driver, 4)
        elem = basepage.username
        wait.until(elem).click()
        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(username)

        elem = basepage.email
        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(email)

        elem = basepage.birthdate
        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(birthdate)

        elem = basepage.address
        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(address)

        elem = basepage.add
        q = self.driver.find_element(*elem.locator)
        q.click()
        time.sleep(2.5)

    @pytest.allure.step("Validate about the Search options, perform a search")
    @pytest.mark.parametrize("qry,value", search)
    def test_user_list_search_query(self, qry,value):
        basepage = BasePage()
        '''

        :return:
        '''
        wait = WebDriverWait(self.driver, 5)
        elem = basepage.q
        wait.until(elem).click()
        assert self.driver.find_element(*elem.locator).is_displayed(), "Search textbox"
        elem = basepage.search
        assert self.driver.find_element(*elem.locator).is_displayed(), "Search button"

        elem = basepage.q
        qr = self.driver.find_element(*elem.locator)
        qr.clear()
        qr.send_keys(qry)
        time.sleep(1)
        qr.send_keys(Keys.RETURN)
        time.sleep(5)
        if value is True:
            assert self.driver.find_element(*basepage.table_value).is_displayed(), "Search result"
        try:
            self.driver.find_element(*basepage.table_value)
        except NoSuchElementException:
            assert value is False, "Search result"


    @pytest.allure.step("Validate about the Search result and return a empty search")
    def test_user_list_search(self):
        basepage = BasePage()
        '''

        :return:
        '''
        wait = WebDriverWait(self.driver, 5)
        elem = basepage.q
        wait.until(elem).click()
        qr = self.driver.find_element(*elem.locator)
        qr.clear()
        time.sleep(1)
        qr.send_keys("")
        qr.send_keys(Keys.RETURN)
        time.sleep(5)

    @pytest.allure.step("Validate about the Search result and return a empty search")
    def test_user_input(self):
        basepage = BasePage()
        '''

        :return:
        '''
        wait = WebDriverWait(self.driver, 2)
        wait.until(basepage.username).click()
        elem = basepage.username
        assert self.driver.find_element(*elem.locator).is_displayed(), "username textbox"
        elem = basepage.email
        assert self.driver.find_element(*elem.locator).is_displayed(), "email textbox"
        elem = basepage.address
        assert self.driver.find_element(*elem.locator).is_displayed(), "address textbox"
        elem = basepage.birthdate
        assert self.driver.find_element(*elem.locator).is_displayed(), "birthdate textbox"
        elem = basepage.add
        assert self.driver.find_element(*elem.locator).is_displayed(), "add button"

    @pytest.allure.step("Seeding the UserList with testdata")
    @pytest.mark.parametrize("username,email,birthdate,address", testdata)
    def test_user_with_test_data(self, username, email, birthdate, address):
        basepage = BasePage()
        '''

        :return:
        '''
        wait = WebDriverWait(self.driver, 5)
        elem = basepage.username
        wait.until(elem).click()

        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(username)

        elem = basepage.email
        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(email)

        elem = basepage.birthdate
        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(birthdate)

        elem = basepage.address
        q = self.driver.find_element(*elem.locator)
        q.clear()
        q.send_keys(address)

        elem = basepage.add
        q = self.driver.find_element(*elem.locator)
        q.click()
        time.sleep(3)
