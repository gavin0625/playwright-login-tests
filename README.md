# 登录功能自动化测试项目

基于 Playwright 和 Python 的登录功能自动化测试项目，支持生成 JSON 格式的测试报告。

## 项目结构

```
login/
├── requirements.txt              # Python依赖包
├── pytest.ini                    # Pytest配置文件
├── conftest.py                   # Pytest配置和报告生成
├── test_login.py                 # 基础版测试脚本
├── test_login_advanced.py        # 增强版测试脚本（推荐使用）
├── test_report.json              # 生成的JSON测试报告
├── screenshots/                  # 失败测试截图（自动创建）
└── README.md                     # 项目说明文档
```

## 环境要求

- Python 3.8+
- pip 包管理器

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install
```

如果需要安装所有浏览器：
```bash
playwright install --all-browsers
```

如果只需要安装 Chromium（推荐）：
```bash
playwright install chromium
```

## 配置说明

在使用前，请修改测试脚本中的配置：

### test_login.py 或 test_login_advanced.py

```python
BASE_URL = "http://localhost"  # 修改为实际的网站URL
USERNAME = "admin"             # 默认用户名
PASSWORD = "admin123!"         # 默认密码
```

## 运行测试

### 基础运行

运行所有测试：
```bash
pytest test_login.py
```

或运行增强版测试（推荐）：
```bash
pytest test_login_advanced.py
```

### 指定标记运行

只运行冒烟测试：
```bash
pytest -m smoke
```

只运行登录相关测试：
```bash
pytest -m login
```

### 详细输出

显示详细测试信息：
```bash
pytest -v -s test_login_advanced.py
```

### 指定浏览器

使用 Chrome 运行：
```bash
pytest --browser chromium test_login_advanced.py
```

使用 Firefox 运行：
```bash
pytest --browser firefox test_login_advanced.py
```

使用 WebKit 运行：
```bash
pytest --browser webkit test_login_advanced.py
```

### 并行运行

安装 pytest-xdist 后可以并行运行：
```bash
pip install pytest-xdist
pytest -n 2 test_login_advanced.py
```

## 测试用例说明

### TC001: 使用有效凭证登录
- **描述**: 验证使用正确的用户名和密码能够成功登录
- **步骤**:
  1. 打开登录页面
  2. 输入用户名: admin
  3. 输入密码: admin123!
  4. 点击登录按钮 (#edit-submit)
- **预期结果**: 用户成功登录系统

### TC002: 使用无效用户名登录
- **描述**: 验证使用错误的用户名无法登录
- **预期结果**: 显示错误提示信息

### TC003: 使用无效密码登录
- **描述**: 验证使用错误的密码无法登录
- **预期结果**: 显示错误提示信息

### TC004: 使用空字段登录
- **描述**: 验证不填写任何信息时无法提交
- **预期结果**: 显示必填字段提示

## 测试报告

测试运行完成后会自动生成 `test_report.json` 文件，包含：

### 报告结构

```json
{
  "report_info": {
    "title": "登录功能自动化测试报告",
    "generated_at": "2025-01-27T18:00:00",
    "framework": "Playwright + Pytest",
    "version": "1.0.0"
  },
  "summary": {
    "total_test_cases": 4,
    "passed": 3,
    "failed": 1,
    "skipped": 0,
    "pass_rate": 75.0
  },
  "test_execution": {
    "start_time": "2025-01-27T18:00:00",
    "end_time": "2025-01-27T18:00:30"
  },
  "test_cases": [
    {
      "test_case_id": "TC001",
      "test_case_name": "使用有效凭证登录",
      "description": "验证使用正确的用户名和密码能够成功登录",
      "priority": "P0",
      "tags": ["smoke", "login", "positive"],
      "status": "passed",
      "duration": "2.345s",
      "steps": [...]
    }
  ]
}
```

### 查看报告

直接查看 JSON 文件：
```bash
cat test_report.json
```

或使用 JSON 格式化工具：
```bash
python -m json.tool test_report.json
```

## 截图功能

当测试失败时，系统会自动截图并保存到 `screenshots/` 目录：
```
screenshots/
├── fail_TC001_20250127_180000.png
└── fail_TC003_20250127_180015.png
```

## 自定义配置

### 修改超时时间

在测试脚本中修改：
```python
TIMEOUT = 60000  # 改为60秒
```

### 添加更多测试用例

在 `TestLoginAdvanced` 类中添加新的测试方法：
```python
def test_your_test_case(self, page: Page, test_data_collection):
    """
    你的测试用例描述
    """
    # 测试代码
    pass
```

## 常见问题

### 1. 找不到元素错误
- 检查页面是否完全加载
- 增加 `page.wait_for_timeout()` 等待时间
- 验证元素选择器是否正确

### 2. 超时错误
- 增加 `TIMEOUT` 配置值
- 检查网络连接
- 使用 `page.wait_for_selector()` 等待特定元素

### 3. 浏览器未安装
```bash
playwright install --all-browsers
```

### 4. 权限错误（Linux/Mac）
```bash
playwright install --with-deps
```

## 扩展功能

### 生成 HTML 报告

安装 pytest-html：
```bash
pip install pytest-html
```

运行测试：
```bash
pytest --html=test_report.html --self-contained-html test_login_advanced.py
```

### 添加 Allure 报告

安装 Allure：
```bash
pip install allure-pytest
```

运行测试：
```bash
pytest --alluredir=allure-results test_login_advanced.py
allure serve allure-results
```

### 添加重试机制

安装 pytest-rerunfailures：
```bash
pip install pytest-rerunfailures
```

运行测试：
```bash
pytest --reruns 3 test_login_advanced.py
```

## 最佳实践

1. **使用 Page Object Model**: 对于大型项目，建议使用 POM 设计模式
2. **添加等待策略**: 使用智能等待而非固定时间
3. **参数化测试**: 使用 `@pytest.mark.parametrize` 实现数据驱动
4. **环境隔离**: 为不同环境（开发、测试、生产）创建不同配置
5. **持续集成**: 集成到 CI/CD 流程中自动运行

## 联系方式

如有问题或建议，请联系测试团队。
