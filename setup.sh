#!/bin/bash

# 自动化测试项目安装脚本

echo "=========================================="
echo "   登录功能自动化测试 - 安装脚本"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "✅ Python3 版本: $(python3 --version)"
echo ""

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到 pip3"
    echo "请先安装 pip"
    exit 1
fi

echo "✅ pip3 已安装"
echo ""

# 安装Python依赖
echo "📦 安装Python依赖包..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖包安装失败"
    exit 1
fi

echo "✅ Python依赖包安装完成"
echo ""

# 安装Playwright浏览器
echo "🌐 安装 Playwright 浏览器..."
echo "建议安装 chromium (推荐)"
echo "如果要安装所有浏览器，请运行: playwright install --all-browsers"
echo ""

read -p "是否安装 chromium 浏览器? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    playwright install chromium

    if [ $? -ne 0 ]; then
        echo "❌ Playwright浏览器安装失败"
        exit 1
    fi

    echo "✅ Playwright浏览器安装完成"
else
    echo "⚠️  跳过浏览器安装"
    echo "稍后可以手动运行: playwright install chromium"
fi

echo ""
echo "=========================================="
echo "   安装完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 编辑 config.py 配置测试环境的URL和凭证"
echo "2. 运行测试: python3 run_tests.py"
echo "   或: pytest test_login_advanced.py -v"
echo ""
echo "更多信息请查看: QUICKSTART.md"
echo ""
