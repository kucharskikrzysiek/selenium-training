from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class BaseClass:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, element_tuple, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(element_tuple))
        return self.driver.find_element(element_tuple[0], element_tuple[1])

    def wait_for_page_loaded(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState=='complete'"))

    def element_is_present(self, element_tuple):
        self.driver.implicitly_wait(3)
        flag = True if len(self.driver.find_elements(element_tuple[0], element_tuple[1])) > 0 else False
        self.driver.implicitly_wait(1)
        return flag
