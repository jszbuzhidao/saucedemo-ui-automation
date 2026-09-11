"""购物车页面对象。"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CSS_SELECTOR, "div[data-test='inventory-item']")
    CHECKOUT_BTN = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")

    def item_count(self) -> int:
        """等待购物车条目渲染完成后再计数（页面加载有短暂空窗）。"""
        self.wait_visible(self.CART_ITEM)
        return len(self.driver.find_elements(*self.CART_ITEM))

    def click_checkout(self):
        self.wait_clickable(self.CHECKOUT_BTN).click()
        return CheckoutPage(self.driver, self.base_url)


from pages.checkout_page import CheckoutPage  # noqa: E402
