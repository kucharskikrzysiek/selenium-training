import json
import pytest
import os
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


ELEMENTS = {
    "username": (By.NAME, "username"),
    "password": (By.NAME, "password"),
    "button login": (By.NAME, "login"),
    "login success info": (By.XPATH, "//div[@class='notice success']"),
    "btn catalog": (By.XPATH, "//a[contains(@href,'doc=catalog')]/span[@class='name']"),
    "catalog form": (By.NAME, "catalog_form"),
    "btn add new product": (By.CSS_SELECTOR, "a.button[href*=edit_product]"),
    "status enabled": (By.CSS_SELECTOR, "input[name=status][value='1']"),
    "product name": (By.NAME, "name[en]"),
    "product description": (By.XPATH, "//div[contains(@class, 'editor')][../textarea]"),
    "head title": (By.NAME, "head_title[en]"),
    "product manufacturer select": (By.NAME, "manufacturer_id"),
    "product image": (By.NAME, "new_images[]"),
    "tab information": (By.CSS_SELECTOR, "a[href='#tab-information']"),
    "tab prices": (By.CSS_SELECTOR, "a[href='#tab-prices']"),
    "price usd": (By.NAME, "prices[USD]"),
    "btn save": (By.NAME, "save"),
    "changes info": (By.XPATH, "//div[contains(text(), 'Changes were successfully saved')]"),
    "email": (By.NAME, "email"),
    "new product title": (By.CSS_SELECTOR, "a[title={0}")
}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_add_new_product(driver):
    login_to_admin_panel(driver)
    navigate_to_catalog_by_left_menu(driver)
    product_data = generate_new_product()
    add_new_product(driver, product_data)
    get_element(driver, ELEMENTS["changes info"])
    check_created_product(driver, product_data)


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])


def type_text(driver, element_tuple, text_to_input, clear=True):
    element = get_element(driver, element_tuple)
    if clear:
        element.clear()
    element.send_keys(text_to_input)


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


def navigate_to_catalog_by_left_menu(driver):
    get_element(driver, ELEMENTS["btn catalog"]).click()
    assert get_element(driver, ELEMENTS["catalog form"]).is_displayed()


def generate_new_product():
    return {
        "name": "product%s" % datetime.now().strftime("%Y%m%d%H%M%S"),
        "description": "Test description",
        "manufacturer": "ACME Corp.",
        "image": os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_duck.png"),
        "currency": "EUR",
        "price": str(round(random.uniform(1.01, 99.99), 2))
    }


def add_new_product(driver, product_data):
    get_element(driver, ELEMENTS["btn add new product"]).click()
    get_element(driver, ELEMENTS["product name"])
    # general tab
    get_element(driver, ELEMENTS["status enabled"]).click()
    type_text(driver, ELEMENTS["product name"], product_data["name"])
    type_text(driver, ELEMENTS["product image"], product_data["image"], False)
    get_element(driver, ELEMENTS["tab information"]).click()
    # information tab
    select_field = Select(get_element(driver, ELEMENTS["product manufacturer select"]))
    select_field.select_by_visible_text(product_data["manufacturer"])
    type_text(driver, ELEMENTS["product description"], product_data["description"])
    get_element(driver, ELEMENTS["tab prices"]).click()
    # prices tab
    type_text(driver, ELEMENTS["price usd"], product_data["price"])
    get_element(driver, ELEMENTS["btn save"]).click()


def check_created_product(driver, product_data):
    driver.get("http://localhost/litecart/")
    get_element(driver, ELEMENTS["email"])
    new_product_element_tuple = \
        (ELEMENTS["new product title"][0], ELEMENTS["new product title"][1].format(product_data["name"]))
    assert get_element(driver, new_product_element_tuple).is_displayed()
