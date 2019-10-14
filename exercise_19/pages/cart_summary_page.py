from app.base_class import (BaseClass,
                            By,
                            WebDriverWait)


class CartSummaryPage(BaseClass):

    def __init__(self, driver):
        BaseClass.__init__(self, driver)
        self.driver = driver

    ELEMENTS = {
        "cart form": (By.NAME, "cart_form"),
        "quantity": (By.NAME, "quantity"),
        "btn update cart item": (By.NAME, "update_cart_item"),
        "number of products in summary": (By.XPATH, "(//div[contains(@id, 'order_confirmation-wrapper')]//td)[1]"),
        "no items info": (By.XPATH, "//*[contains(., 'There are no items in your cart')]")
    }

    def page_is_open(self):
        self.wait_for_page_loaded()
        assert self.cart_form.is_displayed()

    @property
    def cart_form(self):
        return self.wait_for_element(self.ELEMENTS["cart form"])

    @property
    def get_number_of_products_in_summary(self):
        return int(self.wait_for_element(self.ELEMENTS["number of products in summary"]).text)

    @property
    def quantity(self):
        return self.wait_for_element(self.ELEMENTS["quantity"])

    @property
    def button_update_cart_item(self):
        return self.wait_for_element(self.ELEMENTS["btn update cart item"])

    @property
    def no_items_info(self):
        return self.wait_for_element((self.ELEMENTS["no items info"]))

    def wait_for_item_remove(self, item_counter):
        by, selector = self.ELEMENTS["number of products in summary"]
        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_element(by, selector).text == str(
                item_counter - 1))
