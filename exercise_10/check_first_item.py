import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gistfile1 import ColorNames

ELEMENTS = {
    "region": (By.ID, "region"),
    "campaigns items": (By.XPATH, '//div[@id="box-campaigns"]//li[contains(@class, "product")]'),
    "box product": (By.ID, "box-product"),
    "product details title": (By.XPATH, "//h1[@class='title']"),
    "product details regular price": (By.CLASS_NAME, "regular-price"),
    "product details campaign price": (By.CLASS_NAME,"campaign-price"),

}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_1_check_first_item(driver):
    driver.get("http://localhost/litecart/")
    get_element(driver, ELEMENTS["region"])
    all_campaigns_items = get_elements(driver, ELEMENTS["campaigns items"])
    first_item = all_campaigns_items[0]
    name_of_item_value = first_item.find_element_by_class_name("name").text
    regular_price = {
        "value": first_item.find_element_by_class_name("regular-price").text,
        "color": get_color(first_item.find_element_by_class_name("regular-price").value_of_css_property("color")),
        "text style": first_item.find_element_by_class_name("regular-price").value_of_css_property("text-decoration"),
    }
    campaign_price = {
        "value": first_item.find_element_by_class_name("campaign-price").text,
        "color": get_color(first_item.find_element_by_class_name("campaign-price").value_of_css_property("color")),
        "text style": first_item.find_element_by_class_name("campaign-price").value_of_css_property("font-weight"),
    }
    first_item.click()
    get_element(driver, ELEMENTS["box product"])
    product_details = {
        "name":
            get_element(driver, ELEMENTS["product details title"]).text,
        "regular price value":
            get_element(driver, ELEMENTS["product details regular price"]).text,
        "regular price color":
            get_color(get_element(driver, ELEMENTS["product details regular price"]).value_of_css_property("color")),
        "regular price text style":
            get_element(driver, ELEMENTS["product details regular price"]).value_of_css_property("text-decoration"),
        "campaign price value":
            get_element(driver, ELEMENTS["product details campaign price"]).text,
        "campaign price color":
            get_color(get_element(driver, ELEMENTS["product details campaign price"]).value_of_css_property("color")),
        "campaign price text style":
            get_element(driver, ELEMENTS["product details campaign price"]).value_of_css_property("font-weight"),
    }
    assert name_of_item_value == product_details["name"]
    assert regular_price["value"] == product_details["regular price value"]
    assert regular_price["color"] == product_details["regular price color"]
    assert regular_price["text style"] == product_details["regular price text style"]
    assert campaign_price["value"] == product_details["campaign price value"]
    assert campaign_price["color"] == product_details["campaign price color"]
    assert campaign_price["text style"] == product_details["campaign price text style"]


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])


def get_elements(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(element_tuple))
    return driver.find_elements(element_tuple[0], element_tuple[1])


def get_color(rgba):
    rgba = rgba.replace("rgba", "").replace("(", "").replace(")", "").split(",")
    color_tuple = (int(rgba[0]), int(rgba[1]), int(rgba[2]))
    return ColorNames.findNearestWebColorName(color_tuple)
