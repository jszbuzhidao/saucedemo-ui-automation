"""结算流程页面对象：信息填写 → 概览 → 完成。"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    OVERVIEW_ITEMS = (By.CSS_SELECTOR, "div[data-test='inventory-item']")
    SUMMARY_TOTAL = (By.CSS_SELECTOR, "div[data-test='total-label']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "h2[data-test='complete-header']")

    def fill_info(self, first: str, last: str, postal: str):
        self.type_into(self.FIRST_NAME, first)
        self.type_into(self.LAST_NAME, last)
        self.type_into(self.POSTAL_CODE, postal)
        self.wait_clickable(self.CONTINUE_BTN).click()
        return self

    def overview_item_count(self) -> int:
        self.wait_visible(self.OVERVIEW_ITEMS)
        return len(self.driver.find_elements(*self.OVERVIEW_ITEMS))

    def summary_total(self) -> str:
        return self.wait_visible(self.SUMMARY_TOTAL).text

    def finish(self):
        self.wait_clickable(self.FINISH_BTN).click()
        return self

    def complete_text(self) -> str:
        return self.try_text(self.COMPLETE_HEADER)
