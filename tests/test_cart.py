"""购物车场景用例（加购 1 + 移除 1）。"""
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

from tests.conftest import STANDARD_USER, VALID_PASSWORD


@pytest.fixture(scope="function")
def inventory(driver):
    """登录后进入商品列表页。"""
    LoginPage(driver).open("/").login(STANDARD_USER, VALID_PASSWORD)
    return InventoryPage(driver)


class TestCart:

    def test_add_to_cart(self, inventory):
        """加购商品 → 角标计数 +1，按钮变为 Remove。"""
        page = inventory.add_backpack()
        assert page.cart_count() == "1", "加购一件后角标应显示 1"
        assert page.driver.find_elements(*InventoryPage.REMOVE_BACKPACK)

    def test_remove_from_cart(self, inventory):
        """加购后移除 → 角标消失，按钮恢复 Add to cart。"""
        page = inventory.add_backpack().remove_backpack()
        assert page.cart_count() == "", "移除后角标应消失"
        assert page.driver.find_elements(*InventoryPage.ADD_BACKPACK)
