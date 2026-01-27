# GitHub Actions 设置指南

按照以下步骤将测试项目集成到 GitHub Actions。

## 📋 前置要求

- ✅ GitHub 账户
- ✅ Git 已安装
- ✅ 代码已提交到本地 Git（已完成 ✅）

---

## 🚀 设置步骤

### 步骤 1: 创建 GitHub 仓库

#### 方式 A: 通过 GitHub 网页创建（推荐）

1. **访问 GitHub**
   - 打开 https://github.com
   - 登录你的账户

2. **创建新仓库**
   - 点击右上角 `+` → `New repository`
   - 填写仓库信息：
     ```
     Repository name: playwright-login-tests
     Description: Playwright 自动化登录测试项目
     Visibility: Private（私有）或 Public（公开）
     ```
   - ❌ **不要**勾选 "Add a README file"
   - ❌ **不要**勾选 "Add .gitignore"
   - ❌ **不要**选择 "Choose a license"
   - 点击 `Create repository`

3. **推送代码到 GitHub**
   - 复制 GitHub 显示的仓库 URL（类似：`https://github.com/YOUR_USERNAME/playwright-login-tests.git`）
   - 在项目目录运行以下命令：

   ```bash
   # 添加远程仓库（替换为你的实际 URL）
   git remote add origin https://github.com/YOUR_USERNAME/playwright-login-tests.git

   # 推送代码到 GitHub
   git push -u origin main
   ```

#### 方式 B: 使用 GitHub CLI（需要安装 gh）

```bash
# 安装 GitHub CLI（如果还没安装）
# macOS:
brew install gh

# 登录 GitHub
gh auth login

# 创建仓库并推送
gh repo create playwright-login-tests --public --source=. --remote=origin --push
```

---

### 步骤 2: 配置 GitHub Secrets

1. **打开仓库设置**
   - 进入你的 GitHub 仓库
   - 点击 `Settings` 标签

2. **添加 Secrets**
   - 左侧菜单找到 `Secrets and variables` → `Actions`
   - 点击 `New repository secret`
   - 添加以下三个 Secrets：

   #### Secret 1: TEST_URL
   ```
   Name: TEST_URL
   Value: https://alliance-lms.dev.i2hk.net/
   ```

   #### Secret 2: TEST_USERNAME
   ```
   Name: TEST_USERNAME
   Value: admin
   ```

   #### Secret 3: TEST_PASSWORD
   ```
   Name: TEST_PASSWORD
   Value: admin123!
   ```

   #### Secret 4 (可选): SLACK_WEBHOOK_URL
   ```
   Name: SLACK_WEBHOOK_URL
   Value: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

3. **验证 Secrets**
   - 每个 Secret 添加后会显示在列表中
   - 确保 Secrets 已正确保存（Values 不可见）

---

### 步骤 3: 运行 GitHub Actions

#### 自动触发（推荐）

1. **推送代码（如果还没推送）**
   ```bash
   # 如果已经推送过，可以跳过这一步
   git push
   ```

2. **查看 Actions 运行**
   - 进入 GitHub 仓库
   - 点击 `Actions` 标签
   - 你会看到 "Playwright 自动化测试" workflow 正在运行
   - 点击运行记录查看详细日志

#### 手动触发

1. **进入 Actions 页面**
   - 点击 `Actions` 标签

2. **选择 Workflow**
   - 左侧选择 "Playwright 自动化测试"

3. **点击 "Run workflow"**
   - 选择分支：`main`
   - 点击绿色按钮 `Run workflow`

---

### 步骤 4: 查看测试结果

#### 1. 查看 Workflow 运行状态

```
Actions → Playwright 自动化测试 → 选择运行记录
```

- ✅ 绿色 ✓ - 所有测试通过
- ❌ 红色 ✗ - 测试失败
- 🟡 黄色 ○ - 运行中

#### 2. 查看测试日志

- 点击运行的 job
- 展开每个步骤查看详细日志
- 查看测试输出和错误信息

#### 3. 下载测试报告

- 滚动到页面底部的 `Artifacts` 部分
- 下载 `test-report-chromium.zip`
- 解压后查看：
  - `test_report.json` - JSON 格式报告
  - `screenshots/` - 失败截图（如果有）

---

## 🔧 自定义配置

### 修改触发条件

编辑 `.github/workflows/playwright-tests.yml`:

```yaml
on:
  push:
    branches: [ main, develop, staging ]  # 添加更多分支
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 */4 * * *'  # 每4小时运行一次
  workflow_dispatch:  # 允许手动触发
```

### 添加更多浏览器

```yaml
strategy:
  matrix:
    browser: [chromium, firefox, webkit]  # 添加更多浏览器
```

### 修改定时任务

```yaml
schedule:
  # 每天凌晨2点
  - cron: '0 2 * * *'
  # 每小时
  - cron: '0 * * * *'
  # 每周一早上9点
  - cron: '0 9 * * 1'
```

---

## 📊 测试报告说明

### 自动生成的报告

每次运行后会生成：

1. **JSON 报告** (`test_report.json`)
   - 测试概要信息
   - 每个测试用例的详细步骤
   - 执行时间和状态
   - 错误信息（如果有）

2. **截图** (`screenshots/`)
   - 测试失败时自动截图
   - 帮助快速定位问题

3. **HTML 报告** (可选)
   - 可视化的测试结果
   - 更容易查看

### 报告保留

- GitHub Artifacts 保留 30 天
- 可以手动下载保存

---

## 🎯 常见使用场景

### 场景 1: 代码推送时自动测试

```bash
# 修改测试代码后
git add .
git commit -m "Update test cases"
git push

# GitHub Actions 自动运行测试
```

### 场景 2: Pull Request 时验证

```bash
# 创建新分支
git checkout -b feature/new-tests

# 修改测试
git add .
git commit -m "Add new test cases"
git push origin feature/new-tests

# 在 GitHub 创建 PR
# Actions 自动运行测试验证
```

### 场景 3: 定时监控

```yaml
# 已配置为每天凌晨2点运行
schedule:
  - cron: '0 2 * * *'
```

### 场景 4: 手动运行

- 在 GitHub Actions 页面
- 点击 "Run workflow"
- 立即运行测试

---

## ⚠️ 故障排查

### 问题 1: Workflow 未触发

**原因**: 分支不匹配、文件路径错误

**解决**:
```yaml
# 检查 .github/workflows/playwright-tests.yml
on:
  push:
    branches: [ main ]  # 确保分支名正确
```

### 问题 2: Secrets 读取失败

**原因**: Secret 名称拼写错误、未设置 Secret

**解决**:
1. 检查 Secret 名称是否完全匹配（区分大小写）
2. 重新添加 Secrets
3. 查看 Actions 日志确认

### 问题 3: 测试超时

**原因**: 网络慢、元素加载慢

**解决**:
```yaml
# 增加超时时间
jobs:
  test:
    timeout-minutes: 60  # 增加到60分钟
```

### 问题 4: 测试失败，本地通过

**原因**: 环境差异、网络问题

**解决**:
```python
# 增加等待时间
page.wait_for_timeout(3000)

# 或使用显式等待
page.wait_for_selector("#edit-name", timeout=30000)
```

### 问题 5: 浏览器下载失败

**原因**: 网络问题

**解决**:
```yaml
- name: 安装 Playwright 浏览器
  run: python -m playwright install --with-deps chromium
```

---

## 🔐 安全最佳实践

1. **永远不要在代码中硬编码凭证**
   ```python
   # ❌ 错误
   PASSWORD = "admin123!"

   # ✅ 正确
   PASSWORD = os.getenv("TEST_PASSWORD")
   ```

2. **使用 GitHub Secrets**
   - Secrets 在日志中自动隐藏
   - 不会在代码中暴露

3. **限制仓库访问**
   - 敏感项目使用 Private 仓库
   - 控制协作者权限

4. **定期更新凭证**
   - 定期更换测试密码
   - 更新 GitHub Secrets

---

## 📈 优化建议

### 1. 使用缓存加快速度

```yaml
- name: 缓存 Playwright 浏览器
  uses: actions/cache@v3
  with:
    path: ~/.cache/ms-playwright
    key: ${{ runner.os }}-playwright-${{ hashFiles('**/requirements.txt') }}
```

### 2. 并行测试

```yaml
strategy:
  matrix:
    browser: [chromium, firefox]
    shard: [1/2, 2/2]  # 分成2个并行任务
```

### 3. 条件执行

```yaml
- name: 运行测试
  if: github.event_name == 'push' || github.event_name == 'workflow_dispatch'
  run: pytest test_login_advanced.py
```

---

## 📚 相关资源

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [Playwright Python 文档](https://playwright.dev/python/)
- [项目 CI/CD 集成文档](CI_CD_INTEGRATION.md)
- [快速参考指南](QUICK_REFERENCE.md)

---

## ✅ 检查清单

完成设置后，确认以下项目：

- [ ] 代码已推送到 GitHub
- [ ] GitHub Secrets 已配置（TEST_URL, TEST_USERNAME, TEST_PASSWORD）
- [ ] Actions workflow 已触发
- [ ] 测试成功运行（绿色 ✓）
- [ ] 能够下载和查看测试报告
- [ ] 了解如何查看测试日志

---

## 🎉 完成！

现在你的测试项目已成功集成到 GitHub Actions！

每次推送代码、创建 PR 或定时触发时，测试会自动运行。

查看测试结果：
- GitHub 仓库 → Actions 标签
- 下载测试报告和截图
- 根据结果调整测试代码

需要帮助？查看详细文档或联系团队！
