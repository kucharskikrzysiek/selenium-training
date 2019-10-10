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
    "login success info": (By.XPATH, "//div[@class='notice success']"),
    "catalog form": (By.NAME, "catalog_form"),
    "products": (By.XPATH, "//a[contains(@href,'product_id')][../img]"),
    "product": (By.XPATH, "//a[contains(@href,'product_id') and .='{0}'][../img]"),

}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])


def get_elements(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_elements(element_tuple[0], element_tuple[1])


def type_text(driver, element_tuple, text_to_input, clear=True):
    element = get_element(driver, element_tuple)
    if clear:
        element.clear()
    element.send_keys(text_to_input)


def test_check_browser_logs(driver):
    login_to_admin_panel(driver)
    navigate_to_catalog_categories(driver)
    open_product_and_check_browser_logs(driver)


def login_to_admin_panel(driver):
    driver.get("http://localhost/litecart/admin/")
    with open('user_data.json') as json_file:
        data = json.load(json_file)

    get_element(driver, ELEMENTS["username"]).send_keys(data["username"])
    get_element(driver, ELEMENTS["password"]).send_keys(data["password"])
    get_element(driver, ELEMENTS["button login"]).click()
    assert get_element(driver, ELEMENTS["login success info"]).is_displayed()


def logout(driver):
    driver.get("http://localhost/litecart/admin/logout.php")
    get_element(driver, ELEMENTS["username"])


def navigate_to_catalog_categories(driver):
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    get_element(driver, ELEMENTS["catalog form"])


def check_browser_logs(driver):
    logs = driver.get_log("browser")
    assert len(logs) == 0, "Unexpected entries in browser logs: " + str(logs)


def open_product_and_check_browser_logs(driver):
    product_names = [element.text for element in get_elements(driver, ELEMENTS["products"])]
    for product_name in product_names:
        by, selector = ELEMENTS["product"]
        get_element(driver, (by, selector.format(product_name))).click()
        check_browser_logs(driver)
        navigate_to_catalog_categories(driver)
