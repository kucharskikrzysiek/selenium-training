from selenium import webdriver
from pages.cart_summary_page import CartSummaryPage
from pages.main_page import MainPage
from pages.product_page import ProductPage


class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_summary_page = CartSummaryPage(self.driver)

    def quit(self):
        self.driver.quit()

    def add_product_x_times(self, product_name, number_of_products):
        for i in range(number_of_products):
            self.add_product_x(product_name)
            self.main_page.open().page_is_open()

    def add_product_x(self, product_name):
        self.main_page.get_product_x(product_name).click()
        self.product_page.page_is_open()
        number_of_products_before_add_to_cart = self.product_page.get_number_of_products
        if self.product_page.product_size_is_present:
            self.product_page.select_first_product_size()
        self.product_page.btn_add_cart_product.click()
        self.product_page.wait_for_next_product_in_cart(number_of_products_before_add_to_cart)
        assert number_of_products_before_add_to_cart < self.product_page.get_number_of_products

    def remove_all_products_one_by_one(self, number_of_products):
        self.product_page.checkout_cart.click()
        self.cart_summary_page.page_is_open()
        for i in range(number_of_products):
            item_counter = self.cart_summary_page.get_number_of_products_in_summary
            self.cart_summary_page.quantity.clear()
            self.cart_summary_page.quantity.send_keys(str(item_counter-1))
            self.cart_summary_page.button_update_cart_item.click()
            if item_counter == 1:
                assert self.cart_summary_page.no_items_info.is_displayed()
                return
            self.cart_summary_page.wait_for_item_remove(item_counter)