# Playwright 测试 Docker 镜像
# 用于在容器中运行自动化测试

FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    # Playwright 依赖
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    # 其他实用工具
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Playwright 浏览器
RUN python -m playwright install --with-deps chromium

# 复制测试文件
COPY test_login_advanced.py .
COPY conftest.py .
COPY config.py .
COPY pytest.ini .

# 创建截图和报告目录
RUN mkdir -p screenshots test-results test-reports

# 设置用户（可选，出于安全考虑）
# RUN useradd -m -u 1000 tester
# USER tester

# 默认命令：运行测试
CMD ["python", "-m", "pytest", "test_login_advanced.py", "-v", "--browser", "chromium"]

# 构建镜像示例:
# docker build -t playwright-test:latest .
#
# 运行测试示例:
# docker run --rm \
#   -e TEST_URL="https://alliance-lms.dev.i2hk.net/" \
#   -e TEST_USERNAME="admin" \
#   -e TEST_PASSWORD="admin123!" \
#   -v $(pwd)/test-report:/app/test-report \
#   playwright-test:latest
