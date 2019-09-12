import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_01(driver):
    driver.get("https://qa-courses.com/")
    WebDriverWait(driver, 15).until(EC.title_contains("QA-courses"))
