"""商品列表页面对象。"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    CART_BADGE = (By.CSS_SELECTOR, "span[data-test='shopping-cart-badge']")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    ITEM_NAME = (By.CSS_SELECTOR, "div[data-test='inventory-item-name']")

    def add_backpack(self):
        self.wait_clickable(self.ADD_BACKPACK).click()
        return self

    def add_bike_light(self):
        self.wait_clickable(self.ADD_BIKE_LIGHT).click()
        return self

    def remove_backpack(self):
        self.wait_clickable(self.REMOVE_BACKPACK).click()
        return self

    def cart_count(self) -> str:
        """购物车角标数字；未加购时角标不渲染，返回空串。"""
        badges = self.driver.find_elements(*self.CART_BADGE)
        return badges[0].text if badges else ""

    def go_to_cart(self):
        self.driver.find_element(By.ID, "shopping_cart_container").click()
        return CartPage(self.driver, self.base_url)


# 避免循环导入，CartPage 在方法内部延迟构造，这里单独导入放到文件底部
from pages.cart_page import CartPage  # noqa: E402
