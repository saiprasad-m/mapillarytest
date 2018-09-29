import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("driver_init")
class BasePage:

    def __init__(self):
        self.heading = EC.visibility_of_element_located((By.CSS_SELECTOR, "h3#heading"))

        self.userlist = EC.visibility_of_element_located((By.CSS_SELECTOR, "body > h4"))

        self.column_header_number = EC.visibility_of_element_located((By.CSS_SELECTOR, "th:nth-child(1)"))
        self.column_header_username = EC.visibility_of_element_located((By.CSS_SELECTOR, "th:nth-child(2)"))
        self.column_header_email = EC.visibility_of_element_located((By.CSS_SELECTOR, "th:nth-child(3)"))
        self.column_header_birthdate = EC.visibility_of_element_located((By.CSS_SELECTOR, "th:nth-child(4)"))
        self.column_header_address = EC.visibility_of_element_located((By.CSS_SELECTOR, "th:nth-child(5)"))

        self.username = EC.visibility_of_element_located((By.ID, "username"))
        self.email = EC.visibility_of_element_located((By.ID, "email"))
        self.birthdate = EC.visibility_of_element_located((By.ID, "birthdate"))
        self.address = EC.visibility_of_element_located((By.ID, "address"))
        self.add = EC.visibility_of_element_located((By.ID, "add"))
        self.username = EC.visibility_of_element_located((By.ID, "username"))

        self.q = EC.visibility_of_element_located((By.CSS_SELECTOR, "#q"))
        self.search = EC.visibility_of_element_located((By.ID, "search"))

        self.table_value = (By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(2)")


pass
