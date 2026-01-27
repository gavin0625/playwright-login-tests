#!/usr/bin/env python3
"""
快速运行测试的脚本
"""

import sys
import subprocess
from config import TestConfig


def main():
    """主函数"""
    # 打印配置信息
    TestConfig.print_config()

    # 构建pytest命令
    cmd = [
        "pytest",
        "test_login_advanced.py",
        "-v",
        "--browser", TestConfig.BROWSER,
        f"--base-url={TestConfig.get_base_url()}"
    ]

    # 添加无头模式参数
    if TestConfig.HEADLESS:
        cmd.append("--headed=false")

    # 添加慢动作模式
    if TestConfig.SLOW_MO > 0:
        cmd.append(f"--slow-mo={TestConfig.SLOW_MO}")

    print(f"\n运行命令: {' '.join(cmd)}\n")

    # 运行测试
    result = subprocess.run(cmd)

    # 返回退出码
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
