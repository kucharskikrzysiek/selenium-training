from app.base_class import (BaseClass,
                            By)


class MainPage(BaseClass):

    def __init__(self, driver):
        BaseClass.__init__(self, driver)
        self.driver = driver

    ELEMENTS = {
        "email": (By.NAME, "email"),
        "most popular products": (By.CSS_SELECTOR, "div#box-most-popular li a.link"),
        "test product cart": (By.CSS_SELECTOR, "div[id=box-most-popular] a.link[title='{0}']"),
    }

    def open(self):
        self.driver.get("http://localhost/litecart/")
        return self

    def page_is_open(self):
        self.wait_for_page_loaded()
        assert self.email_input.is_displayed()

    @property
    def email_input(self):
        return self.wait_for_element(self.ELEMENTS["email"])

    @property
    def get_most_popular_product_title(self):
        return self.wait_for_element(self.ELEMENTS["most popular products"]).get_attribute("title")

    def get_product_x(self, product_name):
        element_tuple = (self.ELEMENTS["test product cart"][0],
                         self.ELEMENTS["test product cart"][1].format(product_name))
        return self.wait_for_element(element_tuple)
