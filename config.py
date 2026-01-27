"""
测试配置文件
用于管理不同环境的测试配置
"""

import os


class TestConfig:
    """测试配置类"""

    # 环境选择：dev, test, staging, prod
    ENV = os.getenv("TEST_ENV", "test")

    # 环境配置
    ENVIRONMENTS = {
        "dev": {
            "base_url": "http://localhost:3000",
            "username": "admin",
            "password": "admin123!",
            "timeout": 30000
        },
        "test": {
            "base_url": "https://alliance-lms.dev.i2hk.net/",
            "username": "admin",
            "password": "admin123!",
            "timeout": 30000
        },
        "staging": {
            "base_url": "http://staging.example.com",
            "username": "staging_admin",
            "password": "staging123!",
            "timeout": 30000
        },
        "prod": {
            "base_url": "http://www.example.com",
            "username": "prod_admin",
            "password": "prod123!",
            "timeout": 30000
        }
    }

    # 浏览器配置
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # 慢动作模式（毫秒）

    # 视口配置
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080

    # 截图配置
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = "screenshots"

    # 视频录制配置（可选）
    VIDEO_DIR = "videos"
    RECORD_VIDEO = False

    # 超时配置
    DEFAULT_TIMEOUT = 30000
    NAVIGATION_TIMEOUT = 30000

    # 测试数据
    TEST_DATA = {
        "valid_user": {
            "username": "admin",
            "password": "admin123!"
        },
        "invalid_user": {
            "username": "invalid_user",
            "password": "wrongpassword"
        },
        "empty_fields": {
            "username": "",
            "password": ""
        }
    }

    @classmethod
    def get_config(cls):
        """获取当前环境的配置"""
        return cls.ENVIRONMENTS[cls.ENV]

    @classmethod
    def get_base_url(cls):
        """获取当前环境的Base URL"""
        return cls.ENVIRONMENTS[cls.ENV]["base_url"]

    @classmethod
    def get_credentials(cls):
        """获取当前环境的凭证"""
        env_config = cls.ENVIRONMENTS[cls.ENV]
        return {
            "username": env_config["username"],
            "password": env_config["password"]
        }

    @classmethod
    def print_config(cls):
        """打印当前配置"""
        config = cls.get_config()
        print("\n" + "=" * 50)
        print("测试配置信息")
        print("=" * 50)
        print(f"环境: {cls.ENV}")
        print(f"Base URL: {config['base_url']}")
        print(f"浏览器: {cls.BROWSER}")
        print(f"无头模式: {cls.HEADLESS}")
        print(f"视口大小: {cls.VIEWPORT_WIDTH}x{cls.VIEWPORT_HEIGHT}")
        print("=" * 50 + "\n")
