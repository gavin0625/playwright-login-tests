# CI/CD 集成指南

本文档详细说明如何将 Playwright 自动化测试项目集成到各种 CI/CD 平台。

## 目录

- [GitHub Actions](#github-actions)
- [GitLab CI/CD](#gitlab-cicd)
- [Jenkins](#jenkins)
- [Docker 容器化](#docker-容器化)
- [最佳实践](#最佳实践)
- [故障排查](#故障排查)

---

## GitHub Actions

### 快速开始

1. **将代码推送到 GitHub**

```bash
git init
git add .
git commit -m "Add Playwright tests"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **配置 GitHub Secrets**

进入 GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret

添加以下 Secrets:
- `TEST_URL`: 测试环境 URL (如: `https://alliance-lms.dev.i2hk.net/`)
- `TEST_USERNAME`: 测试用户名 (如: `admin`)
- `TEST_PASSWORD`: 测试密码 (如: `admin123!`)
- `SLACK_WEBHOOK_URL` (可选): Slack 通知 Webhook

3. **查看运行结果**

- 进入 GitHub 仓库 → Actions 标签
- 查看测试运行状态和日志
- 下载测试报告和截图

### 工作流特性

- ✅ 支持 push、PR、定时任务触发
- ✅ 多浏览器并行测试
- ✅ 自动上传测试报告
- ✅ 失败自动截图
- ✅ Slack 通知集成
- ✅ 支持手动触发

### 自定义工作流

编辑 `.github/workflows/playwright-tests.yml`:

```yaml
# 修改触发条件
on:
  push:
    branches: [ main, develop, staging ]  # 添加更多分支

# 修改浏览器矩阵
strategy:
  matrix:
    browser: [chromium, firefox, webkit]  # 测试多个浏览器

# 修改定时任务
schedule:
  - cron: '0 */4 * * *'  # 每4小时运行一次
```

---

## GitLab CI/CD

### 快速开始

1. **将代码推送到 GitLab**

```bash
git remote set-url origin https://gitlab.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **配置 CI/CD Variables**

进入 GitLab 项目 → Settings → CI/CD → Variables

添加以下 Variables:
- `TEST_URL`: 测试环境 URL
- `TEST_USERNAME`: 测试用户名
- `TEST_PASSWORD`: 测试密码
- `SLACK_WEBHOOK_URL` (可选): Slack Webhook

3. **查看 Pipeline 结果**

- 进入 GitLab 项目 → CI/CD → Pipelines
- 查看各阶段执行状态
- 下载测试报告和产物

### Pipeline 阶段

```
test     → 运行测试（Chromium/Firefox/并行）
report   → 生成测试报告
notify   → 发送通知
```

### 自定义 Pipeline

编辑 `.gitlab-ci.yml`:

```yaml
# 修改测试触发条件
test:chromium:
  only:
    - main
    - develop
    - /^feature\/.*/  # 支持 feature 分支

# 添加环境变量
test:chromium:
  variables:
    TEST_ENV: "staging"
    TIMEOUT: "60000"
```

---

## Jenkins

### 快速开始

1. **安装 Jenkins 插件**

确保安装以下插件:
- Pipeline Plugin
- HTML Publisher Plugin
- JUnit Plugin
- Email Extension Plugin (可选)

2. **创建 Pipeline 任务**

- 新建任务 → Pipeline
- 配置 → Pipeline → Definition → Pipeline script from SCM
- 选择 Git，输入仓库 URL
- Script Path: `Jenkinsfile`

3. **配置全局凭据**

Manage Jenkins → Manage Credentials → Global credentials

添加:
- `test-url`: 测试环境 URL
- `test-username`: 测试用户名
- `test-password`: 测试密码

4. **构建任务**

- 点击 "立即构建"
- 查看构建日志
- 查看测试报告（HTML 报告）

### Pipeline 特性

- ✅ 多阶段构建
- ✅ 并行测试支持
- ✅ 自动生成测试报告
- ✅ JUnit 报告集成
- ✅ 邮件通知
- ✅ Slack 通知（需插件）

### Blue Ocean 支持

```groovy
// 在 Jenkinsfile 中添加
pipeline {
    agent any
    options {
        // 启用 Blue Ocean 可视化
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    // ...
}
```

---

## Docker 容器化

### 本地运行

1. **构建 Docker 镜像**

```bash
docker build -t playwright-test:latest .
```

2. **运行测试**

```bash
docker run --rm \
  -e TEST_URL="https://alliance-lms.dev.i2hk.net/" \
  -e TEST_USERNAME="admin" \
  -e TEST_PASSWORD="admin123!" \
  -v $(pwd)/test-report:/app/test-report \
  playwright-test:latest
```

### 使用 Docker Compose（推荐）

1. **创建 .env 文件**

```bash
cat > .env << EOF
TEST_URL=https://alliance-lms.dev.i2hk.net/
TEST_USERNAME=admin
TEST_PASSWORD=admin123!
BROWSER=chromium
HEADLESS=true
EOF
```

2. **运行所有服务**

```bash
# 启动测试和报告服务
docker-compose up --build

# 只运行测试
docker-compose run --rm playwright-test

# 后台运行
docker-compose up -d --build
```

3. **查看测试报告**

- Allure 报告: http://localhost:5050
- Nginx 报告服务器: http://localhost:8080

### Docker Compose 服务

- `playwright-test`: 运行 Playwright 测试
- `allure-report`: 生成 Allure 测试报告
- `report-server`: Nginx 报告服务器

---

## 最佳实践

### 1. 环境变量管理

**推荐做法:**

```yaml
# GitHub Actions
env:
  TEST_URL: ${{ secrets.TEST_URL }}

# GitLab CI/CD
variables:
  TEST_URL: $TEST_URL

# Docker Compose
environment:
  - TEST_URL=${TEST_URL}
```

**不要硬编码:**
```python
# ❌ 不好
BASE_URL = "https://prod.example.com"

# ✅ 好
BASE_URL = os.getenv("TEST_URL", "https://test.example.com")
```

### 2. 测试数据管理

使用环境特定的测试数据:

```python
# config.py
ENVIRONMENTS = {
    "dev": {"username": "dev_admin", "password": "dev_pass"},
    "test": {"username": "test_admin", "password": "test_pass"},
    "prod": {"username": "prod_admin", "password": "prod_pass"},
}
```

### 3. 并行测试策略

**按浏览器并行:**
```yaml
strategy:
  matrix:
    browser: [chromium, firefox, webkit]
```

**按测试套件并行:**
```bash
pytest -n auto  # 使用所有 CPU 核心
```

**按测试文件并行:**
```yaml
# 在 CI/CD 中拆分测试文件
test-suite-1:
  script: pytest test_login.py
test-suite-2:
  script: pytest test_checkout.py
```

### 4. 测试报告管理

**保留策略:**
```yaml
artifacts:
  expire_in: 30 days  # 保留30天
  paths:
    - test_report.json
    - screenshots/
```

**报告归档:**
```groovy
// Jenkins
archiveArtifacts artifacts: '**/*.json,**/*.png', allowEmptyArchive: true
```

### 5. 通知策略

**失败时通知:**
```yaml
notify:slack:
  when: on_failure  # 只在失败时通知
```

**成功和失败都通知:**
```yaml
notify:slack:
  when: always  # 总是通知
```

### 6. 定时任务

**不同平台的定时任务配置:**

```yaml
# GitHub Actions - 每天凌晨2点
schedule:
  - cron: '0 2 * * *'

# GitLab CI/CD - 每天凌晨2点
test:schedule:
  only:
    - schedules
  script: pytest test_login_advanced.py

# Jenkins - 定时构建
# H 2 * * *  (每天凌晨2点)

# Docker + Cron
# 使用宿主机 cron 定期运行 docker-compose
```

### 7. 资源优化

**缓存依赖:**
```yaml
# GitHub Actions
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# GitLab CI/CD
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip
    - venv/
```

**清理工作空间:**
```groovy
// Jenkins
post {
    always {
        cleanWs()  # 清理工作空间
    }
}
```

---

## 故障排查

### GitHub Actions

**问题：测试超时**
```yaml
# 解决：增加超时时间
jobs:
  test:
    timeout-minutes: 60  # 增加到60分钟
```

**问题：浏览器下载失败**
```yaml
# 解决：显式安装浏览器依赖
- name: 安装系统依赖
  run: |
    sudo apt-get update
    sudo apt-get install -y libnss3 libnspr4 ...
```

### GitLab CI/CD

**问题：Runner 不可用**
```bash
# 解决：注册 Runner
sudo gitlab-runner register \
  --url https://gitlab.com/ \
  --registration-token YOUR_TOKEN
```

**问题：产物过期**
```yaml
# 解决：增加保留时间
artifacts:
  expire_in: 90 days  # 增加到90天
```

### Jenkins

**问题：权限错误**
```bash
# 解决：设置正确的文件权限
chmod +x run_tests.py
```

**问题：工作空间不足**
```groovy
// 解决：清理旧构建
options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
}
```

### Docker

**问题：容器无法访问网络**
```bash
# 解决：检查网络配置
docker network inspect test-network
docker-compose down
docker-compose up -d
```

**问题：测试报告未生成**
```bash
# 解决：检查卷挂载
docker-compose run --rm playwright-test ls -la /app/test-report
```

---

## 监控和维护

### 测试通过率监控

设置通过率阈值，低于阈值时告警:

```python
# 在 conftest.py 中添加
def test_pass_rate_threshold():
    report = json.load(open("test_report.json"))
    pass_rate = report["summary"]["pass_rate"]

    if pass_rate < 80.0:
        send_alert(f"通过率过低: {pass_rate}%")
```

### 性能监控

记录测试执行时间:

```yaml
# GitHub Actions
- name: 记录测试时间
  run: |
    START_TIME=$(date +%s)
    pytest test_login_advanced.py
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    echo "测试耗时: ${DURATION}秒"
```

### 日志管理

**保存测试日志:**
```yaml
artifacts:
  paths:
    - test-report.log
    - playwright.log
  when: always
```

**集中日志管理:**
- 使用 ELK Stack
- 使用 Splunk
- 使用云服务（如 CloudWatch、LogRocket）

---

## 高级配置

### 多环境测试

```yaml
test-dev:
  environment:
    name: development
    url: https://dev.example.com
  script: pytest test_login.py

test-staging:
  environment:
    name: staging
    url: https://staging.example.com
  script: pytest test_login.py
```

### 条件执行

```yaml
# 只在特定文件变化时运行
test-changed-files:
  script:
    - |
      if git diff --name-only HEAD~1 HEAD | grep -q "test_"; then
        pytest test_login.py
      else
        echo "无测试文件变化，跳过测试"
      fi
```

### 矩阵构建

```yaml
# 多浏览器 + 多 Python 版本
strategy:
  matrix:
    browser: [chromium, firefox]
    python: [3.8, 3.9, 3.10]
```

---

## 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [GitLab CI/CD 文档](https://docs.gitlab.com/ee/ci/)
- [Jenkins 文档](https://www.jenkins.io/doc/)
- [Playwright 文档](https://playwright.dev/python/)
- [Docker 文档](https://docs.docker.com/)

---

需要帮助？请查看：
- 项目 README.md
- Playwright 官方文档
- CI/CD 平台文档
