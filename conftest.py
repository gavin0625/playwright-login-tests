"""
Pytest配置文件
用于生成JSON格式的测试报告
"""

import pytest
import json
from datetime import datetime
from playwright.sync_api import BrowserContext


@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    """
    创建页面实例，并设置基本配置
    """
    # 创建新页面
    page = context.new_page()

    # 设置视口大小
    page.set_viewport_size({"width": 1920, "height": 1080})

    # 设置默认超时时间
    page.set_default_timeout(30000)

    yield page

    # 测试结束后关闭页面
    page.close()


@pytest.fixture(scope="session", autouse=True)
def test_data_collection():
    """
    收集所有测试数据的fixture
    """
    test_data = {
        "start_time": datetime.now().isoformat(),
        "test_cases": []
    }

    yield test_data

    # 测试会话结束后生成最终报告
    test_data["end_time"] = datetime.now().isoformat()
    generate_final_report(test_data)


def generate_final_report(test_data):
    """
    生成最终的JSON测试报告
    """
    report = {
        "report_info": {
            "title": "登录功能自动化测试报告",
            "generated_at": datetime.now().isoformat(),
            "framework": "Playwright + Pytest",
            "version": "1.0.0"
        },
        "summary": {
            "total_test_cases": len(test_data["test_cases"]),
            "passed": sum(1 for tc in test_data["test_cases"] if tc["status"] == "passed"),
            "failed": sum(1 for tc in test_data["test_cases"] if tc["status"] == "failed"),
            "skipped": sum(1 for tc in test_data["test_cases"] if tc["status"] == "skipped"),
            "pass_rate": 0
        },
        "test_execution": {
            "start_time": test_data["start_time"],
            "end_time": test_data["end_time"]
        },
        "test_cases": test_data["test_cases"]
    }

    # 计算通过率
    if report["summary"]["total_test_cases"] > 0:
        report["summary"]["pass_rate"] = round(
            (report["summary"]["passed"] / report["summary"]["total_test_cases"]) * 100, 2
        )

    # 保存JSON报告
    report_file = "test_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 打印测试摘要
    print("\n" + "=" * 70)
    print("测试报告已生成")
    print("=" * 70)
    print(f"报告文件: {report_file}")
    print(f"总测试用例数: {report['summary']['total_test_cases']}")
    print(f"通过: {report['summary']['passed']}")
    print(f"失败: {report['summary']['failed']}")
    print(f"跳过: {report['summary']['skipped']}")
    print(f"通过率: {report['summary']['pass_rate']}%")
    print("=" * 70)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    监听每个测试用例的执行结果
    """
    outcome = yield
    report = outcome.get_result()

    # 只在测试调用阶段处理
    if report.when == "call":
        test_data = item.funcargs.get("test_data_collection")
        if test_data is None:
            return

        # 提取测试用例信息
        test_case_info = {
            "test_case_id": getattr(item.obj, "__doc__", item.name).split("\n")[0] if getattr(item.obj, "__doc__") else item.name,
            "test_case_name": item.name,
            "status": report.outcome,
            "duration": f"{report.duration:.3f}s",
            "timestamp": datetime.now().isoformat()
        }

        # 如果测试失败，添加错误信息
        if report.failed:
            test_case_info["error"] = str(report.longreprtext) if hasattr(report, 'longreprtext') else "Test failed"

        # 添加到测试数据中
        test_data["test_cases"].append(test_case_info)
