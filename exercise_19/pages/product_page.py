from app.base_class import (BaseClass,
                            By,
                            Select,
                            WebDriverWait)


class ProductPage(BaseClass):

    def __init__(self, driver):
        BaseClass.__init__(self, driver)
        self.driver = driver

    ELEMENTS = {
        "btn add cart product": (By.NAME, "add_cart_product"),
        "number of products": (By.CSS_SELECTOR, "span.quantity"),
        "select size": (By.CSS_SELECTOR, "select[name='options[Size]']"),
        "checkout cart": (By.CSS_SELECTOR, "a.link[href*=checkout]"),
    }

    def page_is_open(self):
        self.wait_for_page_loaded()
        assert self.btn_add_cart_product.is_displayed()

    @property
    def btn_add_cart_product(self):
        return self.wait_for_element(self.ELEMENTS["btn add cart product"])

    @property
    def get_number_of_products(self):
        return int(self.wait_for_element(self.ELEMENTS["number of products"]).text)

    @property
    def product_size_is_present(self):
        return self.element_is_present(self.ELEMENTS["select size"])

    @property
    def checkout_cart(self):
        return self.wait_for_element(self.ELEMENTS["checkout cart"])

    def select_first_product_size(self):
        select_field = Select(self.wait_for_element(self.ELEMENTS["select size"]))
        select_field.select_by_index(1)

    def wait_for_next_product_in_cart(self, number_of_products_before_add_to_cart):
        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_element(self.ELEMENTS["number of products"][0],
                                     self.ELEMENTS["number of products"][1]).text == str(
                number_of_products_before_add_to_cart + 1))
