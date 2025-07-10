#!/bin/bash

echo "🚀 墨刀原型抓取器环境安装脚本"
echo "=================================="

# 检查Python版本
echo "📋 检查Python环境..."
python3 --version || {
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
}

# 检查pip
echo "📦 检查pip..."
pip3 --version || {
    echo "❌ pip3 未安装，请先安装pip3"
    exit 1
}

# 安装Python依赖
echo "📥 安装Python依赖..."
pip3 install -r requirements_playwright.txt

if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装成功"
else
    echo "❌ Python依赖安装失败"
    exit 1
fi

# 安装Playwright浏览器
echo "🌐 安装Playwright浏览器..."
playwright install chromium

if [ $? -eq 0 ]; then
    echo "✅ Playwright浏览器安装成功"
else
    echo "❌ Playwright浏览器安装失败"
    exit 1
fi

# 创建输出目录
echo "📁 创建输出目录..."
mkdir -p mockingbot_output/{screenshots,network,dom,reports}

# 设置执行权限
echo "🔧 设置执行权限..."
chmod +x mockingbot_scraper.py
chmod +x example_usage.py

echo ""
echo "🎉 安装完成！"
echo "=================================="
echo "📖 使用方法："
echo "  1. 运行完整抓取器: python3 mockingbot_scraper.py"
echo "  2. 运行示例: python3 example_usage.py"
echo "  3. 查看文档: cat README_MockingBot_Scraper.md"
echo ""
echo "📁 输出目录: mockingbot_output/"
echo "⚙️  配置文件: scraper_config.py"
echo ""
echo "🔍 开始抓取墨刀原型吧！"