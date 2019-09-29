from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

ELEMENTS = {
    "first name": (By.NAME, "firstname"),
    "last name": (By.NAME, "lastname"),
    "address1": (By.NAME, "address1"),
    "postcode": (By.NAME, "postcode"),
    "city": (By.NAME, "city"),
    "country combobox": (By.CSS_SELECTOR, "span[role=combobox]"),
    "country input": (By.CSS_SELECTOR, "input.select2-search__field"),
    "email": (By.NAME, "email"),
    "phone":(By.NAME, "phone"),
    "password": (By.NAME, "password"),
    "repeat password": (By.NAME, "confirmed_password"),
    "btn create account": (By.NAME, "create_account"),
    "account created info": (By.XPATH, "//div[contains(text(), 'Your customer account has been created')]"),
    "box account": (By.ID, "box-account"),
    "btn login": (By.NAME, "login")
}


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def get_element(driver, element_tuple, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_tuple))
    return driver.find_element(element_tuple[0], element_tuple[1])


def test_register_new_account(driver):
    driver.get("http://localhost/litecart/en/create_account")
    get_element(driver, ELEMENTS["first name"])
    user_data = generate_new_account_data()
    fill_register_form(driver, user_data)
    get_element(driver, ELEMENTS["account created info"])
    get_element(driver, ELEMENTS["box account"])
    logout(driver)
    login(driver, user_data)
    logout(driver)


def fill_register_form(driver, user_data):
    type_text(driver, ELEMENTS["first name"], user_data["firstname"])
    type_text(driver, ELEMENTS["last name"], user_data["lastname"])
    type_text(driver, ELEMENTS["address1"], user_data["address"])
    type_text(driver, ELEMENTS["postcode"], user_data["postcode"])
    type_text(driver, ELEMENTS["city"], user_data["city"])
    get_element(driver, ELEMENTS["country combobox"]).click()
    type_text(driver, ELEMENTS["country input"], user_data["country"] + Keys.ENTER)
    type_text(driver, ELEMENTS["email"], user_data["email"])
    type_text(driver, ELEMENTS["phone"], user_data["phone"])
    type_text(driver, ELEMENTS["password"], user_data["password"])
    type_text(driver, ELEMENTS["repeat password"], user_data["password"])
    get_element(driver, ELEMENTS["btn create account"]).click()


def type_text(driver, element_tuple, text_to_input, clear=True):
    element = get_element(driver, element_tuple)
    if clear:
        element.clear()
    element.send_keys(text_to_input)


def generate_new_account_data():
    return {
        "firstname": random.choice(["Pedro", "Santiago", "Michael"]),
        "lastname": random.choice(["Gonzales", "De Sousa"]),
        "address": "%s %d" % (random.choice(["Dluga", "Prosta", "Krzywa"]), random.randint(1, 999)),
        "postcode": "{:05d}".format(random.randint(0, 99999)),
        "city": random.choice(["Barcelona", "Madrid"]),
        "country": "Spain",
        "email": "user%s@testmail.com" % datetime.now().strftime("%Y%m%d%H%M%S"),
        "phone": "+%d%d" % (random.randint(0, 99), random.randint(100000000, 999999999)),
        "password":
            ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(8)])
    }


def logout(driver):
    driver.get("http://localhost/litecart/en/logout")
    get_element(driver, ELEMENTS["email"])


def login(driver, user_data):
    type_text(driver, ELEMENTS["email"], user_data["email"])
    type_text(driver, ELEMENTS["password"], user_data["password"])
    get_element(driver, ELEMENTS["btn login"]).click()
    get_element(driver, ELEMENTS["box account"])
