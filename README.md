# saucedemo-ui-automation

基于 [SauceDemo](https://www.saucedemo.com) 公开练习电商站点的 Web UI 自动化测试实践项目：pytest + Selenium，按 **Page Object Model** 组织页面对象，6 个场景覆盖登录 / 加购 / 移除 / 完整结算，无头 Chrome 一键运行，失败自动截图。

## 场景覆盖（6 例）

| 模块 | 用例 | 场景 |
|---|---|---|
| 登录 | `test_valid_login` | 有效账号登录进入商品列表 |
| 登录 | `test_login_wrong_password` | 密码错误 → 提示账号密码不匹配 |
| 登录 | `test_login_locked_out` | 锁定账号 → 提示用户被锁定 |
| 购物车 | `test_add_to_cart` | 加购后角标 +1、按钮变 Remove |
| 购物车 | `test_remove_from_cart` | 移除后角标消失、按钮恢复 |
| 结算 | `test_full_checkout` | 加购 2 件 → 购物车 → 填信息 → 概览核对 → 支付完成页 |

## 工程结构

```
saucedemo-ui-automation/
├── pages/                  # Page Object 层：元素定位与页面操作
│   ├── base_page.py        # 显式等待、输入、点击等公共封装
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py         # 每用例独立无头 Chrome + 失败自动截图
│   ├── test_login.py       # 登录 3 例
│   ├── test_cart.py        # 购物车 2 例
│   └── test_checkout.py    # 结算 1 例
├── pytest.ini
└── requirements.txt
```

## 稳定性设计

- **显式等待**：`WebDriverWait` + `expected_conditions`，全局禁用隐式等待混用；
- **用例隔离**：每条用例独立浏览器会话，互不污染；
- **失败截图**：`pytest_runtest_makereport` 钩子，用例失败自动存 `screenshots/fail_<用例名>.png`；
- **代理环境**：conftest 中强制 `NO_PROXY=127.0.0.1,localhost`，避免系统代理劫持发往本机 chromedriver 的请求。

## 运行

```bash
pip install -r requirements.txt
pytest    # 6 例全跑，报告生成在 reports/report.html
```

**国内环境提示**：Selenium Manager 从 `storage.googleapis.com` 下载 chromedriver 会被墙，可从 [npmmirror 镜像](https://registry.npmmirror.com/binary.html?path=chrome-for-testing/) 下载与本机 Chrome 主版本一致的 `chromedriver-win64.zip`，解压到 `drivers/chromedriver-win64/chromedriver.exe`（conftest 检测到该路径会自动优先使用；`drivers/` 已 gitignore）。
