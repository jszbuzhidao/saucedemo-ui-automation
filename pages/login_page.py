"""登录页面对象。"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")
    # 登录成功后跳转到商品列表页
    INVENTORY_WRAPPER = (By.ID, "inventory_container")

    def login(self, username: str, password: str):
        self.type_into(self.USERNAME, username)
        self.type_into(self.PASSWORD, password)
        self.wait_clickable(self.LOGIN_BTN).click()
        return self

    def error_text(self) -> str:
        return self.try_text(self.ERROR_MSG)

    def is_login_successful(self) -> bool:
        try:
            self.wait.until_not(
                lambda d: d.current_url.rstrip("/").endswith("saucedemo.com/")
            )
        except Exception:
            pass
        return bool(self.driver.find_elements(*self.INVENTORY_WRAPPER))
