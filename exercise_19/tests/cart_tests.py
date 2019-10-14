import pytest


@pytest.mark.parametrize("number_of_products", [3])
def test_cart(app, number_of_products):
    app.main_page.open().page_is_open()
    test_product_name = app.main_page.get_most_popular_product_title
    app.add_product_x_times(test_product_name, number_of_products)
    app.remove_all_products_one_by_one(number_of_products)
