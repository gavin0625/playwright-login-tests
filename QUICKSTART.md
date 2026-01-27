# 快速开始指南

## 5分钟快速上手

### 步骤 1: 安装依赖

```bash
# 安装Python依赖包
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium
```

### 步骤 2: 配置测试环境

编辑 `config.py` 文件，修改测试环境的URL和凭证：

```python
ENVIRONMENTS = {
    "test": {
        "base_url": "http://your-website.com",  # 修改为实际的URL
        "username": "admin",                     # 修改为实际用户名
        "password": "admin123!",                 # 修改为实际密码
        "timeout": 30000
    }
}
```

或者直接修改 `test_login_advanced.py` 中的配置：

```python
BASE_URL = "http://your-website.com"  # 你的网站URL
USERNAME = "admin"
PASSWORD = "admin123!"
```

### 步骤 3: 运行测试

**方式一：使用快速运行脚本**
```bash
python run_tests.py
```

**方式二：直接使用pytest**
```bash
pytest test_login_advanced.py -v
```

**方式三：指定浏览器运行**
```bash
pytest test_login_advanced.py --browser chromium -v
```

### 步骤 4: 查看测试报告

测试完成后，会在当前目录生成 `test_report.json` 文件：

```bash
# 查看JSON报告
cat test_report.json

# 或使用Python美化输出
python -m json.tool test_report.json
```

## 环境变量配置

可以通过环境变量覆盖配置：

```bash
# 设置测试环境
export TEST_ENV=prod

# 设置浏览器
export BROWSER=firefox

# 设置是否无头模式
export HEADLESS=false

# 设置慢动作模式（方便调试）
export SLOW_MO=1000

# 运行测试
python run_tests.py
```

## 运行特定测试用例

```bash
# 只运行冒烟测试
pytest -m smoke test_login_advanced.py -v

# 只运行登录相关测试
pytest -m login test_login_advanced.py -v

# 运行特定测试用例
pytest test_login_advanced.py::TestLoginAdvanced::test_login_with_valid_credentials -v
```

## 调试技巧

### 1. 使用无头模式查看执行过程
```bash
pytest test_login_advanced.py --headed=false -v
```

### 2. 使用慢动作模式
```bash
pytest test_login_advanced.py --slow-mo=1000 -v
```

### 3. 使用调试模式
```bash
pytest test_login_advanced.py -vv -s
```

### 4. 在代码中添加断点
```python
def test_login_with_valid_credentials(self, page: Page, test_data_collection):
    page.goto(self.BASE_URL)
    breakpoint()  # 程序会在这里暂停
    page.locator("#edit-name").fill(self.USERNAME)
```

## 常见问题解决

### 问题1: 找不到元素
**解决方案**: 增加等待时间
```python
# 等待元素出现
page.wait_for_selector("#edit-name", timeout=10000)

# 或等待特定时间
page.wait_for_timeout(2000)
```

### 问题2: 页面加载慢
**解决方案**: 增加超时时间
```python
# 在测试脚本中修改
TIMEOUT = 60000  # 60秒
```

### 问题3: 选择器错误
**解决方案**: 使用Playwright的录制功能
```bash
playwright codegen http://your-website.com
```

### 问题4: 验证码无法通过
**解决方案**: 联系开发团队提供测试环境的验证码绕过方案

## 下一步

- 阅读 [README.md](README.md) 了解更多详细信息
- 查看生成的测试报告了解测试结果
- 根据实际需求修改和扩展测试用例
- 集成到CI/CD流程

## 示例：添加新的测试用例

```python
@pytest.mark.regression
def test_logout(self, page: Page, test_data_collection):
    """
    TC005: 用户登出测试
    """
    test_case = {
        "test_case_id": "TC005",
        "test_case_name": "用户登出",
        "description": "验证用户能够成功登出",
        "priority": "P1",
        "status": "",
        "steps": []
    }

    start_time = datetime.now()

    try:
        # 先登录
        page.goto(self.BASE_URL)
        page.locator("#edit-name").fill(self.USERNAME)
        page.locator("#edit-pass--2").fill(self.PASSWORD)
        page.locator("#edit-submit").click()

        # 等待登录成功
        page.wait_for_timeout(2000)

        # 点击登出按钮
        page.locator("#logout-button").click()

        test_case["status"] = "passed"
    except Exception as e:
        test_case["status"] = "failed"
        test_case["error"] = str(e)
        raise
    finally:
        duration = (datetime.now() - start_time).total_seconds()
        test_case["duration"] = f"{duration:.3f}s"
        test_data_collection["test_cases"].append(test_case)
```

祝测试顺利！
