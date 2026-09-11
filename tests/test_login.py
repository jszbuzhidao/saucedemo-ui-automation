"""登录场景用例（有效 1 + 无效 2）。"""
import pytest

from pages.login_page import LoginPage

from tests.conftest import LOCKED_USER, STANDARD_USER, VALID_PASSWORD


@pytest.mark.usefixtures("driver")
class TestLogin:

    def test_valid_login(self, driver):
        """有效账号登录 → 进入商品列表页。"""
        page = LoginPage(driver).open("/").login(STANDARD_USER, VALID_PASSWORD)
        assert page.is_login_successful(), "有效账号应登录成功并看到商品列表"

    def test_login_wrong_password(self, driver):
        """密码错误 → 提示账号密码不匹配。"""
        page = LoginPage(driver).open("/").login(STANDARD_USER, "wrong_password")
        assert "do not match" in page.error_text().lower()

    def test_login_locked_out(self, driver):
        """锁定账号登录 → 提示用户已被锁定。"""
        page = LoginPage(driver).open("/").login(LOCKED_USER, VALID_PASSWORD)
        assert "locked out" in page.error_text().lower()
