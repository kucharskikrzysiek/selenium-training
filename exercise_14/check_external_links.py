import pytest
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ELEMENTS = {
    "username": (By.NAME, "username"),
    "password": (By.NAME, "password"),
    "button login": (By.NAME, "login"),
    "login success info": (By.XPATH, "//div[@class='notice success']"),
    "countries form": (By.NAME, "countries_form"),
    "poland edit pencil": (By.CSS_SELECTOR, "a[href*=PL] i.fa-pencil"),
    "country name": (By.NAME, "name"),
    "icon external link": (By.CSS_SELECTOR, "i.fa-external-link"),
    "external link body": (By.CSS_SELECTOR, "body")
}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_check_links_for_new_window(driver):
    login_to_admin_panel(driver)
    navigate_to_countries(driver)
    get_element(driver, ELEMENTS["poland edit pencil"]).click()
    get_element(driver, ELEMENTS["country name"])
    all_icon_elements = get_elements(driver, ELEMENTS["icon external link"])
    check_all_external_links(driver, all_icon_elements)


def navigate_to_countries(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    get_element(driver, ELEMENTS["countries form"])


def login_to_admin_panel(driver):
    driver.get("http://localhost/litecart/admin/")
    with open('user_data.json') as json_file:
        data = json.load(json_file)

    get_element(driver, ELEMENTS["username"]).send_keys(data["username"])
    get_element(driver, ELEMENTS["password"]).send_keys(data["password"])
    get_element(driver, ELEMENTS["button login"]).click()
    assert get_element(driver, ELEMENTS["login success info"]).is_displayed()


def wait_for_page_loaded(driver):
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState=='complete'"))


def wait_for_new_tab(driver, number_of_windows):
    WebDriverWait(driver, 10).until(
        lambda d: len(d.window_handles) > number_of_windows)
    wait_for_page_loaded(driver)


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])


def get_elements(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_elements(element_tuple[0], element_tuple[1])


def check_all_external_links(driver, external_link_elements):
    for element in external_link_elements:
        number_of_windows = len(driver.window_handles)
        element.click()
        wait_for_new_tab(driver, number_of_windows)
        # switch_to_window alert: DeprecationWarning: use driver.switch_to.window instead
        driver.switch_to.window(driver.window_handles[number_of_windows])
        get_element(driver, ELEMENTS["external link body"])
        driver.close()
        driver.switch_to.window(driver.window_handles[number_of_windows-1])

