import json
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ELEMENTS = {
    "username": (By.NAME, "username"),
    "password": (By.NAME, "password"),
    "button login": (By.NAME, "login"),
    "login success info": (By.XPATH, "//div[@class='notice success']")
}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_login_to_admin_panel(driver):
    driver.get("http://localhost/litecart/admin/")
    with open('user_data.json') as json_file:
        data = json.load(json_file)

    get_element(driver, ELEMENTS["username"]).send_keys(data["username"])
    get_element(driver, ELEMENTS["password"]).send_keys(data["password"])
    get_element(driver, ELEMENTS["button login"]).click()
    assert get_element(driver, ELEMENTS["login success info"]).is_displayed()


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])
