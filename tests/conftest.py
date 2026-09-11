"""浏览器驱动 fixture 与失败截图钩子。"""
import os

# 代理环境下必须让发往本机 chromedriver 的请求直连，否则会被代理劫持报 unhandled request
os.environ.setdefault("NO_PROXY", "127.0.0.1,localhost")
os.environ.setdefault("no_proxy", "127.0.0.1,localhost")

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

STANDARD_USER = "standard_user"
LOCKED_USER = "locked_out_user"
VALID_PASSWORD = "secret_sauce"

# 本地 drivers/ 目录存在 chromedriver 时优先使用（国内 Selenium Manager 下载易被墙）
LOCAL_DRIVER = os.path.join(os.path.dirname(__file__), "..", "drivers",
                            "chromedriver-win64", "chromedriver.exe")


def _make_driver() -> webdriver.Chrome:
    """无头 Chrome：本地与 CI 均可直接运行。"""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    if os.path.exists(LOCAL_DRIVER):
        return webdriver.Chrome(service=Service(LOCAL_DRIVER), options=opts)
    return webdriver.Chrome(options=opts)


@pytest.fixture(scope="function")
def driver():
    """每条用例一个独立浏览器会话，保证用例间无状态污染。"""
    d = _make_driver()
    d.implicitly_wait(0)  # 统一用显式等待，禁用隐式等待混用
    yield d
    d.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """用例失败时自动截图到 screenshots/ 目录。"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = getattr(item, "funcargs", {}).get("driver")
        if driver is not None:
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(f"screenshots/fail_{item.name}.png")
