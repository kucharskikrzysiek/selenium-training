import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


ELEMENTS = {
    "email": (By.NAME, "email"),
    "most popular products": (By.CSS_SELECTOR, "div[id=box-most-popular] li a.link"),
    "test product cart": (By.CSS_SELECTOR, "div[id=box-most-popular] a.link[title='{0}']"),
    "btn add cart product": (By.NAME, "add_cart_product"),
    "number of products": (By.CSS_SELECTOR, "span.quantity"),
    "select size": (By.CSS_SELECTOR, "select[name='options[Size]']"),
    "checkout cart": (By.CSS_SELECTOR, "a.link[href*=checkout]"),
    "cart form": (By.NAME, "cart_form"),
    "quantity": (By.NAME, "quantity"),
    "btn update cart item": (By.NAME, "update_cart_item"),
    "number of products in summary": (By.XPATH, "(//div[contains(@id, 'order_confirmation-wrapper')]//td)[1]"),
    "no items info": (By.XPATH, "//*[contains(., 'There are no items in your cart')]")
}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])


def type_text(driver, element_tuple, text_to_input, clear=True):
    element = get_element(driver, element_tuple)
    if clear:
        element.clear()
    element.send_keys(text_to_input)


def test_cart_test(driver):
    open_main_page(driver)
    test_product_name = get_element(driver, ELEMENTS["most popular products"]).get_attribute("title")
    number_of_products = 3
    for i in range(number_of_products):
        add_product_to_cart(driver, test_product_name)
        open_main_page(driver)
    remove_all_products_one_by_one(driver, number_of_products)


def open_main_page(driver):
    driver.get("http://localhost/litecart/")
    get_element(driver, ELEMENTS["email"])


def add_product_to_cart(driver, test_product_name):
    test_product_element_tuple = \
        (ELEMENTS["test product cart"][0], ELEMENTS["test product cart"][1].format(test_product_name))
    get_element(driver, test_product_element_tuple).click()
    get_element(driver, ELEMENTS["btn add cart product"])
    number_of_products_before_add_to_cart = get_number_of_products_in_cart(driver)
    if element_is_present(driver, ELEMENTS["select size"]):
        select_field = Select(get_element(driver, ELEMENTS["select size"]))
        select_field.select_by_index(1)
    get_element(driver, ELEMENTS["btn add cart product"]).click()
    WebDriverWait(driver, 15).until(
        lambda d: d.find_element(ELEMENTS["number of products"][0], ELEMENTS["number of products"][1]).text == str(
            number_of_products_before_add_to_cart + 1))
    assert number_of_products_before_add_to_cart < get_number_of_products_in_cart(driver)


def get_number_of_products_in_cart(driver):
    return int(get_element(driver, ELEMENTS["number of products"]).text)


def element_is_present(driver, element_tuple):
    driver.implicitly_wait(5)
    flag = True if len(driver.find_elements(element_tuple[0], element_tuple[1])) > 0 else False
    driver.implicitly_wait(1)
    return flag


def navigate_to_cart_summary(driver):
    get_element(driver, ELEMENTS["checkout cart"]).click()
    get_element(driver, ELEMENTS["cart form"])


def remove_all_products_one_by_one(driver, number_of_products):
    navigate_to_cart_summary(driver)
    for i in range(number_of_products):
        item_counter = int(get_element(driver, ELEMENTS["number of products in summary"]).text)
        type_text(driver, ELEMENTS["quantity"], str(item_counter-1))
        get_element(driver, ELEMENTS["btn update cart item"]).click()
        if item_counter == 1:
            get_element(driver, ELEMENTS["no items info"])
            return
        cell_tuple = ELEMENTS["number of products in summary"]
        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(cell_tuple[0], cell_tuple[1]).text == str(
                item_counter - 1))
