#!/usr/bin/env python3
"""
墨刀原型抓取器使用示例
"""

import asyncio
from mockingbot_scraper import MockingBotScraper
from scraper_config import MOCKINGBOT_URL, BROWSER_CONFIG

async def simple_scrape_example():
    """简单抓取示例"""
    print("=== 墨刀原型抓取器使用示例 ===")
    
    # 创建抓取器实例
    scraper = MockingBotScraper(output_dir="example_output")
    
    try:
        # 执行抓取
        report = await scraper.scrape_mockingbot_prototype(
            url=MOCKINGBOT_URL,
            wait_time=BROWSER_CONFIG['wait_time']
        )
        
        # 显示结果摘要
        print("\n📊 抓取结果摘要:")
        print(f"  页面标题: {report['page_info']['title']}")
        print(f"  网络请求数: {report['network_analysis']['total_requests']}")
        print(f"  API接口数: {report['network_analysis']['api_endpoints_count']}")
        print(f"  截屏数量: {len(report['screenshots'])}")
        print(f"  输出目录: {scraper.output_dir}")
        
        return report
        
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return None

async def advanced_scrape_example():
    """高级抓取示例 - 自定义配置"""
    print("\n=== 高级抓取示例 ===")
    
    # 自定义配置
    custom_scraper = MockingBotScraper(output_dir="advanced_output")
    
    try:
        # 可以在这里添加自定义的抓取逻辑
        report = await custom_scraper.scrape_mockingbot_prototype(
            url=MOCKINGBOT_URL,
            wait_time=20  # 更长的等待时间
        )
        
        # 分析API接口
        print("\n🔍 API接口分析:")
        api_file = custom_scraper.output_dir / "network" / "api_endpoints.json"
        if api_file.exists():
            import json
            with open(api_file, 'r', encoding='utf-8') as f:
                apis = json.load(f)
                for i, api in enumerate(apis[:5], 1):  # 显示前5个API
                    print(f"  {i}. {api['method']} {api['url']}")
                if len(apis) > 5:
                    print(f"  ... 还有 {len(apis) - 5} 个API接口")
        
        return report
        
    except Exception as e:
        print(f"❌ 高级抓取失败: {e}")
        return None

def show_usage_instructions():
    """显示使用说明"""
    print("""
=== 墨刀原型抓取器使用说明 ===

1. 安装依赖:
   pip install -r requirements_playwright.txt
   playwright install chromium

2. 运行简单示例:
   python example_usage.py

3. 运行完整抓取器:
   python mockingbot_scraper.py

4. 自定义配置:
   编辑 scraper_config.py 文件

=== 输出文件说明 ===
- screenshots/: 页面截屏
- network/: 网络请求和API接口
- dom/: DOM结构和页面信息
- reports/: 结构化报告 (JSON/MD/HTML)

=== 核心功能 ===
✅ 网络接口截获
✅ DOM结构抓取
✅ 页面截屏
✅ 结构化报告生成
✅ 多种输出格式 (JSON/Markdown/HTML)
""")

if __name__ == "__main__":
    # 显示使用说明
    show_usage_instructions()
    
    # 运行示例
    async def main():
        # 简单示例
        await simple_scrape_example()
        
        # 高级示例
        await advanced_scrape_example()
    
    asyncio.run(main())