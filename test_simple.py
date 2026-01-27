"""
简单的登录测试 - 用于调试
"""
import pytest
from playwright.sync_api import Page, expect
import os

BASE_URL = os.getenv("TEST_URL", "https://alliance-lms.dev.i2hk.net/")
USERNAME = os.getenv("TEST_USERNAME", "admin")
PASSWORD = os.getenv("TEST_PASSWORD", "admin123!")
TIMEOUT = 60000


def test_simple_login(page: Page):
    """最简单的登录测试"""
    print(f"\n=== 测试配置 ===")
    print(f"URL: {BASE_URL}")
    print(f"Username: {USERNAME}")
    print(f"Password: {'*' * len(PASSWORD)}")

    # 步骤1: 访问页面
    print(f"\n步骤1: 访问 {BASE_URL}")
    response = page.goto(BASE_URL, timeout=TIMEOUT, wait_until="domcontentloaded")
    print(f"状态码: {response.status}")

    # 等待页面加载
    page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)
    print("✓ 页面已加载")

    # 步骤2: 填写用户名
    print("\n步骤2: 等待用户名输入框...")
    page.wait_for_selector("#edit-name", timeout=TIMEOUT)
    print("✓ 找到用户名输入框")

    page.fill("#edit-name", USERNAME)
    print(f"✓ 已填写用户名: {USERNAME}")

    # 步骤3: 填写密码
    print("\n步骤3: 等待密码输入框...")
    page.wait_for_selector("#edit-pass--2", timeout=TIMEOUT)
    print("✓ 找到密码输入框")

    page.fill("#edit-pass--2", PASSWORD)
    print("✓ 已填写密码")

    # 步骤4: 点击提交
    print("\n步骤4: 等待提交按钮...")
    page.wait_for_selector("#edit-submit", timeout=TIMEOUT)
    print("✓ 找到提交按钮")

    # 截图（调试用）
    page.screenshot(path="screenshot_before_click.png")
    print("✓ 已保存截图: screenshot_before_click.png")

    print("\n点击登录按钮...")
    page.click("#edit-submit")
    print("✓ 已点击登录按钮")

    # 等待导航
    print("\n等待页面跳转...")
    page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)
    print("✓ 页面已跳转")

    # 最终截图
    page.screenshot(path="screenshot_after_login.png")
    print("✓ 已保存截图: screenshot_after_login.png")

    print("\n✅ 测试完成！")
    print(f"最终 URL: {page.url}")
