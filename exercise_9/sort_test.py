import json
import pytest
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
    "countries form": (By.NAME, "countries_form"),
    "country name": (By.NAME, "name"),
    "geo zones title": (By.XPATH, "//h1[contains(text(), 'Geo Zones')]"),
    "zone name": (By.NAME, "name")
}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def login_to_admin_panel(driver):
    driver.get("http://localhost/litecart/admin/")
    with open('user_data.json') as json_file:
        data = json.load(json_file)

    get_element(driver, ELEMENTS["username"]).send_keys(data["username"])
    get_element(driver, ELEMENTS["password"]).send_keys(data["password"])
    get_element(driver, ELEMENTS["button login"]).click()
    assert get_element(driver, ELEMENTS["login success info"]).is_displayed()


def test_ex_1(driver):
    login_to_admin_panel(driver)
    open_countries_table(driver)
    countries = []
    countries_with_zones = []
    for element in driver.find_elements_by_xpath("//tr[@class='row']"):
        country = element.find_element_by_xpath(".//a[contains(@href, 'country')][1]").text
        countries.append(country)
        zones_number = element.find_element_by_xpath("./td[6]").text
        if int(zones_number) > 0:
            countries_with_zones.append(country)
    assert countries == sorted(countries), "Countries are not sorted properly"
    for country_with_zones in countries_with_zones:
        zones_list = []
        open_countries_table(driver)
        driver.find_element_by_xpath("//a[text()='%s']" % country_with_zones).click()
        get_element(driver, ELEMENTS["country name"])
        for element in driver.find_elements_by_xpath("//input[contains(@name,'[name]')]"):
            zone_name = element.get_attribute('value')
            if len(zone_name) > 0:
                zones_list.append(zone_name)
        assert zones_list == sorted(zones_list), "Zones for %s are not sorted properly" % country_with_zones
    logout(driver)


def test_ex_2(driver):
    login_to_admin_panel(driver)
    open_geo_zones_page(driver)
    geo_zones_list = []
    for element in driver.find_elements_by_xpath("//tr[@class='row']/td[3]/a"):
        geo_zones_list.append(element.text)
    for geo_zone in geo_zones_list:
        driver.find_element_by_xpath("//a[text()='%s']" % geo_zone).click()
        get_element(driver, ELEMENTS["zone name"])
        if geo_zone == "European Union":
            pass
        else:
            zones_list = [Select(element).first_selected_option.text
                          for element in driver.find_elements_by_xpath("//select[contains(@name, '[zone_code]')]")]
            assert zones_list == sorted(zones_list), "Zones are not sorted properly"
        open_geo_zones_page(driver)
    logout(driver)


def open_countries_table(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    get_element(driver, ELEMENTS["countries form"])


def logout(driver):
    driver.get("http://localhost/litecart/admin/logout.php")
    get_element(driver, ELEMENTS["username"])


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])


def open_geo_zones_page(driver):
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    get_element(driver, ELEMENTS["geo zones title"])
