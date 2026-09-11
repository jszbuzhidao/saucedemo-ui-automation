"""完整结算场景用例。"""
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

from tests.conftest import STANDARD_USER, VALID_PASSWORD


def test_full_checkout(driver):
    """登录 → 加购 2 件 → 进购物车 → 填写信息 → 概览 → 完成。"""
    LoginPage(driver).open("/").login(STANDARD_USER, VALID_PASSWORD)
    inventory = InventoryPage(driver)

    inventory.add_backpack().add_bike_light()
    cart = inventory.go_to_cart()
    assert cart.item_count() == 2, "购物车里应有 2 件商品"

    checkout = cart.click_checkout().fill_info("Shuojia", "Zhang", "100000")
    assert checkout.overview_item_count() == 2, "结算概览应列出 2 件商品"
    assert "Total" in checkout.summary_total()

    checkout.finish()
    assert "Thank you for your order" in checkout.complete_text(), "支付完成应显示感谢页"
