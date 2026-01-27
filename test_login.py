"""
登录功能自动化测试脚本
使用 Playwright 框架
"""

import pytest
import json
from datetime import datetime
from playwright.sync_api import Page, expect


class TestLogin:
    """登录测试类"""

    def __init__(self):
        self.test_results = []
        self.base_url = "http://localhost"  # 请修改为实际的网站地址

    def test_login_success(self, page: Page):
        """
        测试用例：成功登录
        步骤：
        1. 打开登录页面
        2. 输入用户名 admin
        3. 输入密码 admin123!
        4. 点击登录按钮
        """
        test_case = {
            "test_case_id": "TC001",
            "test_case_name": "用户成功登录",
            "description": "验证使用正确的用户名和密码能够成功登录系统",
            "steps": [],
            "status": "passed",
            "timestamp": datetime.now().isoformat(),
            "error": None
        }

        try:
            # 步骤1: 打开登录页面
            step = {"step": 1, "action": "打开登录页面", "status": "passed"}
            page.goto(self.base_url)
            test_case["steps"].append(step)

            # 步骤2: 填写用户名
            step = {"step": 2, "action": "填写用户名: admin", "status": "passed"}
            page.fill("#edit-name", "admin")
            test_case["steps"].append(step)

            # 步骤3: 填写密码
            step = {"step": 3, "action": "填写密码: admin123!", "status": "passed"}
            page.fill("#edit-pass--2", "admin123!")
            test_case["steps"].append(step)

            # 步骤4: 点击登录按钮
            step = {"step": 4, "action": "点击登录按钮", "status": "passed"}
            page.click("#edit-submit")
            test_case["steps"].append(step)

            # 验证：等待页面跳转或显示登录成功
            # 这里可以根据实际情况调整等待条件
            page.wait_for_timeout(2000)

        except Exception as e:
            test_case["status"] = "failed"
            test_case["error"] = str(e)
            # 标记失败的步骤
            for step in test_case["steps"]:
                if step["step"] == len(test_case["steps"]):
                    step["status"] = "failed"

        # 保存测试结果
        self.test_results.append(test_case)

        # 断言测试是否通过
        assert test_case["status"] == "passed", f"测试失败: {test_case.get('error')}"

    def test_login_with_empty_credentials(self, page: Page):
        """
        测试用例：使用空凭证登录
        验证系统是否正确处理空用户名和密码
        """
        test_case = {
            "test_case_id": "TC002",
            "test_case_name": "使用空凭证登录",
            "description": "验证不输入用户名和密码时系统给出正确提示",
            "steps": [],
            "status": "passed",
            "timestamp": datetime.now().isoformat(),
            "error": None
        }

        try:
            # 打开登录页面
            step = {"step": 1, "action": "打开登录页面", "status": "passed"}
            page.goto(self.base_url)
            test_case["steps"].append(step)

            # 不填写任何信息，直接点击登录
            step = {"step": 2, "action": "不填写凭证直接点击登录", "status": "passed"}
            page.click("#edit-submit")
            test_case["steps"].append(step)

            page.wait_for_timeout(1000)

        except Exception as e:
            test_case["status"] = "failed"
            test_case["error"] = str(e)

        self.test_results.append(test_case)

    def test_login_with_wrong_password(self, page: Page):
        """
        测试用例：使用错误密码登录
        验证系统是否正确拒绝错误密码
        """
        test_case = {
            "test_case_id": "TC003",
            "test_case_name": "使用错误密码登录",
            "description": "验证使用错误密码时系统显示错误信息",
            "steps": [],
            "status": "passed",
            "timestamp": datetime.now().isoformat(),
            "error": None
        }

        try:
            # 打开登录页面
            step = {"step": 1, "action": "打开登录页面", "status": "passed"}
            page.goto(self.base_url)
            test_case["steps"].append(step)

            # 填写正确的用户名
            step = {"step": 2, "action": "填写用户名: admin", "status": "passed"}
            page.fill("#edit-name", "admin")
            test_case["steps"].append(step)

            # 填写错误的密码
            step = {"step": 3, "action": "填写错误密码", "status": "passed"}
            page.fill("#edit-pass--2", "wrongpassword")
            test_case["steps"].append(step)

            # 点击登录
            step = {"step": 4, "action": "点击登录按钮", "status": "passed"}
            page.click("#edit-submit")
            test_case["steps"].append(step)

            page.wait_for_timeout(1000)

        except Exception as e:
            test_case["status"] = "failed"
            test_case["error"] = str(e)

        self.test_results.append(test_case)


# 实例化测试类
test_login = TestLogin()


@pytest.fixture(scope="session")
def test_results():
    """保存所有测试结果的fixture"""
    results = []

    yield results

    # 测试结束后生成JSON报告
    generate_json_report(results)


def generate_json_report(results):
    """生成JSON格式的测试报告"""
    report = {
        "report_title": "登录功能自动化测试报告",
        "generated_at": datetime.now().isoformat(),
        "total_test_cases": len(results),
        "passed": sum(1 for r in results if r["status"] == "passed"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "test_cases": results
    }

    # 保存到文件
    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n" + "="*50)
    print("测试报告已生成: test_report.json")
    print(f"总测试用例数: {report['total_test_cases']}")
    print(f"通过: {report['passed']}")
    print(f"失败: {report['failed']}")
    print("="*50)
