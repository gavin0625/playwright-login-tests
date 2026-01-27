# CI/CD 集成快速参考

## 🚀 快速开始

### GitHub Actions（推荐用于 GitHub）

```bash
# 1. 推送代码到 GitHub
git init
git add .
git commit -m "Add Playwright tests"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# 2. 在 GitHub 仓库设置中添加 Secrets
# TEST_URL, TEST_USERNAME, TEST_PASSWORD

# 3. 查看运行结果
# GitHub 仓库 → Actions 标签
```

### GitLab CI/CD（推荐用于 GitLab）

```bash
# 1. 推送代码到 GitLab
git remote set-url origin https://gitlab.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# 2. 在 GitLab 项目设置中添加 Variables
# Settings → CI/CD → Variables

# 3. 查看 Pipeline
# GitLab 项目 → CI/CD → Pipelines
```

### Jenkins（推荐用于自托管）

```bash
# 1. 安装 Jenkins 插件
# - Pipeline Plugin
# - HTML Publisher Plugin

# 2. 创建 Pipeline 任务
# - 选择 Pipeline
# - Script Path: Jenkinsfile

# 3. 配置凭据
# Manage Jenkins → Credentials → Add Credentials
```

### Docker（推荐用于容器化）

```bash
# 1. 使用 Docker Compose
cp .env.example .env
# 编辑 .env 文件

# 2. 运行测试
docker-compose up --build

# 3. 查看报告
# Allure: http://localhost:5050
# Nginx: http://localhost:8080
```

---

## 📋 配置清单

### GitHub Secrets
- ✅ TEST_URL
- ✅ TEST_USERNAME
- ✅ TEST_PASSWORD
- ✅ SLACK_WEBHOOK_URL (可选)

### GitLab CI/CD Variables
- ✅ TEST_URL
- ✅ TEST_USERNAME
- ✅ TEST_PASSWORD
- ✅ SLACK_WEBHOOK_URL (可选)

### Jenkins Credentials
- ✅ test-url
- ✅ test-username
- ✅ test-password

### Docker .env File
- ✅ TEST_URL
- ✅ TEST_USERNAME
- ✅ TEST_PASSWORD
- ✅ BROWSER
- ✅ HEADLESS

---

## 🔧 常用命令

### 本地测试
```bash
# 运行所有测试
pytest test_login_advanced.py -v

# 运行特定测试
pytest test_login_advanced.py::TestLoginAdvanced::test_login_with_valid_credentials -v

# 并行运行
pytest test_login_advanced.py -v -n auto

# 生成报告
pytest test_login_advanced.py -v --html=report.html
```

### Docker 命令
```bash
# 构建镜像
docker build -t playwright-test .

# 运行容器
docker run --rm -v $(pwd)/report:/app/report playwright-test

# 使用 Compose
docker-compose up --build
docker-compose run --rm playwright-test
docker-compose down
```

### CI/CD 命令
```bash
# GitHub Actions - 手动触发
# 在 Actions 页面点击 "Run workflow"

# GitLab CI/CD - 手动触发
# 在 Pipeline 页面点击 "Play" 按钮

# Jenkins - 手动构建
# 在项目页面点击 "立即构建"
```

---

## 📊 测试报告位置

### GitHub Actions
- 位置: Actions → 选择运行 → Artifacts
- 下载: `test-report-chromium.zip`
- 保留期: 30 天

### GitLab CI/CD
- 位置: CI/CD → Pipelines → 选择 Pipeline → Jobs
- 下载: Job 页面右侧 "Download artifacts"
- 保留期: 30 天

### Jenkins
- 位置: 构建页面 → 测试报告
- HTML 报告: 构建页面 → "Playwright Test Report"
- 截图: 构建页面 → "Build Artifacts"

### Docker
- 位置: `./test-report/`
- 本地访问: `http://localhost:8080`

---

## ⚙️ 配置文件说明

| 文件 | 用途 | 平台 |
|------|------|------|
| `.github/workflows/playwright-tests.yml` | GitHub Actions 工作流 | GitHub |
| `.gitlab-ci.yml` | GitLab Pipeline 配置 | GitLab |
| `Jenkinsfile` | Jenkins Pipeline 脚本 | Jenkins |
| `Dockerfile` | Docker 镜像构建 | Docker |
| `docker-compose.yml` | Docker Compose 配置 | Docker |
| `.env` | 环境变量 | Docker/本地 |
| `conftest.py` | pytest 配置 | 所有 |
| `pytest.ini` | pytest 设置 | 所有 |

---

## 🎯 不同场景推荐

### 🏢 企业内部项目
**推荐**: Jenkins 或 GitLab (自托管)
- ✅ 完全控制
- ✅ 安全性高
- ✅ 自定义灵活

### 🌐 开源项目
**推荐**: GitHub Actions
- ✅ 免费公开仓库
- ✅ 社区集成好
- ✅ 配置简单

### 🚀 快速验证
**推荐**: Docker
- ✅ 环境一致
- ✅ 快速启动
- ✅ 易于分享

### 🔄 频繁测试
**推荐**: GitLab CI/CD 或 GitHub Actions
- ✅ 实时反馈
- ✅ 自动触发
- ✅ 并行执行

---

## 🔍 故障排查快速指南

### 问题：测试在 CI 上失败，本地通过
**原因**: 环境差异、网络问题、超时
**解决**:
```yaml
# 增加超时
timeout-minutes: 60

# 使用重试
pip install pytest-rerunfailures
pytest --reruns 3
```

### 问题：找不到元素
**原因**: 页面加载慢、选择器错误
**解决**:
```python
# 显式等待
page.wait_for_selector("#edit-name", timeout=30000)

# 增加等待时间
page.wait_for_timeout(2000)
```

### 问题：CI 环境中浏览器无法启动
**原因**: 缺少系统依赖
**解决**:
```bash
# 安装 Playwright 系统依赖
python -m playwright install --with-deps chromium
```

### 问题：测试报告未生成
**原因**: 文件路径错误、权限问题
**解决**:
```python
# 使用绝对路径
report_path = os.path.abspath("test_report.json")

# 检查目录权限
mkdir -p test-results
chmod 755 test-results
```

---

## 📚 相关文档

- 📖 [完整 CI/CD 集成文档](CI_CD_INTEGRATION.md)
- 📖 [快速开始指南](QUICKSTART.md)
- 📖 [项目 README](README.md)

---

## 💡 提示

1. **首次设置建议**: 从 Docker 开始，验证测试无误后再集成 CI/CD
2. **安全性**: 永远不要在代码中硬编码凭证，使用 Secrets/Variables
3. **性能**: 使用并行测试和缓存来加快执行速度
4. **监控**: 设置通知，及时了解测试结果
5. **维护**: 定期更新依赖，清理旧的测试报告

---

需要更多帮助？查看详细文档或联系团队！
