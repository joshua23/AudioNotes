# 墨刀原型全自动抓取器

基于 Headless Playwright 1.53 的墨刀原型全自动抓取解决方案，实现网络接口截获、DOM抓取、截屏和结构化输出。

## 🎯 核心功能

- **网络接口截获**: 自动捕获和分析所有网络请求/响应
- **DOM结构抓取**: 完整抓取页面DOM结构并解析关键信息
- **智能截屏**: 全页面和视口截屏，保留视觉参考
- **结构化输出**: 生成JSON、Markdown、HTML三种格式的报告
- **API接口分析**: 自动识别和提取API接口信息

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements_playwright.txt

# 安装Playwright浏览器
playwright install chromium
```

### 2. 运行抓取器

```bash
# 运行完整抓取器
python mockingbot_scraper.py

# 或运行示例
python example_usage.py
```

### 3. 查看结果

抓取完成后，结果将保存在 `mockingbot_output/` 目录中：

```
mockingbot_output/
├── screenshots/          # 页面截屏
│   ├── full_page_*.png   # 全页面截屏
│   └── viewport_*.png    # 视口截屏
├── network/              # 网络分析
│   └── api_endpoints.json # API接口列表
├── dom/                  # DOM结构
│   ├── full_dom.html     # 完整DOM
│   └── page_structure.json # 结构化DOM信息
└── reports/              # 报告文件
    ├── scraping_report.json  # JSON报告
    ├── scraping_report.md    # Markdown报告
    └── scraping_report.html  # HTML报告
```

## 📋 使用方法

### 基础使用

```python
import asyncio
from mockingbot_scraper import MockingBotScraper

async def main():
    # 创建抓取器
    scraper = MockingBotScraper(output_dir="my_output")
    
    # 执行抓取
    report = await scraper.scrape_mockingbot_prototype(
        url="https://modao.cc/proto/your-prototype-url",
        wait_time=15
    )
    
    print(f"抓取完成！页面标题: {report['page_info']['title']}")

asyncio.run(main())
```

### 高级配置

编辑 `scraper_config.py` 文件来自定义配置：

```python
# 浏览器配置
BROWSER_CONFIG = {
    'headless': True,
    'viewport': {'width': 1920, 'height': 1080},
    'wait_time': 15,
}

# 输出配置
OUTPUT_CONFIG = {
    'base_dir': 'custom_output',
    'screenshots_dir': 'images',
    'network_dir': 'api_data',
}
```

## 🔧 核心原理

### 1. 页面渲染流程

```
访问页面 → 等待网络空闲 → 等待渲染完成 → 开始抓取
```

### 2. 数据抓取策略

- **网络监听**: 使用Playwright的网络事件监听器
- **DOM抓取**: 获取完整页面内容并解析结构
- **截屏策略**: 全页面 + 视口双重截屏
- **API识别**: 基于关键词过滤识别API接口

### 3. 输出结构

```json
{
  "metadata": {
    "scraper_version": "1.0.0",
    "timestamp": "2024-01-01T12:00:00"
  },
  "page_info": {
    "title": "页面标题",
    "url": "页面URL",
    "viewport": {"width": 1920, "height": 1080}
  },
  "network_analysis": {
    "total_requests": 150,
    "api_endpoints_count": 25
  },
  "dom_analysis": {
    "has_dom_snapshot": true,
    "dom_size_bytes": 50000
  },
  "screenshots": [
    {
      "type": "full_page",
      "path": "screenshots/full_page_20240101_120000.png"
    }
  ]
}
```

## 🛠️ 技术特性

### 浏览器优化

- **无头模式**: 提高性能和稳定性
- **沙箱禁用**: 避免权限问题
- **GPU禁用**: 减少资源消耗
- **自定义User-Agent**: 模拟真实浏览器

### 网络分析

- **请求监听**: 捕获所有HTTP请求
- **响应分析**: 分析响应内容和状态
- **API识别**: 智能识别API接口
- **内容提取**: 提取文本响应内容

### DOM处理

- **完整快照**: 保存完整DOM结构
- **结构化解析**: 提取关键页面元素
- **资源分析**: 分析脚本、样式、图片等资源

### 报告生成

- **多格式输出**: JSON、Markdown、HTML
- **截图嵌入**: HTML报告中嵌入base64截图
- **结构化数据**: 便于后续处理和分析

## 📊 输出示例

### JSON报告片段

```json
{
  "page_info": {
    "title": "AI聊天安卓APP-原型-分享",
    "url": "https://modao.cc/proto/MShAKNLmsyponvrscCKL56/sharing",
    "viewport": {"width": 1920, "height": 1080}
  },
  "network_analysis": {
    "total_requests": 156,
    "api_endpoints_count": 23,
    "api_endpoints": [
      {
        "url": "https://api.modao.cc/proto/data",
        "method": "GET",
        "headers": {...}
      }
    ]
  }
}
```

### Markdown报告

```markdown
# 墨刀原型抓取报告

## 基本信息
- **抓取时间**: 2024-01-01T12:00:00
- **页面标题**: AI聊天安卓APP-原型-分享
- **页面URL**: https://modao.cc/proto/...

## 网络分析
- **总请求数**: 156
- **API接口数**: 23

## 截屏信息
- **全页面截屏**: screenshots/full_page_20240101_120000.png
- **视口截屏**: screenshots/viewport_20240101_120000.png
```

## 🔍 高级功能

### 自定义网络过滤

```python
# 在 scraper_config.py 中自定义API关键词
API_KEYWORDS = ['api', 'ajax', 'json', 'data', 'rest', 'graphql', 'custom']
```

### 多页面抓取

```python
async def scrape_multiple_pages():
    urls = [
        "https://modao.cc/proto/page1",
        "https://modao.cc/proto/page2",
        "https://modao.cc/proto/page3"
    ]
    
    for i, url in enumerate(urls):
        scraper = MockingBotScraper(output_dir=f"output_page_{i}")
        await scraper.scrape_mockingbot_prototype(url)
```

### 自定义等待策略

```python
# 等待特定元素出现
await page.wait_for_selector('.prototype-container', timeout=30000)

# 等待网络空闲
await page.wait_for_load_state('networkidle')
```

## 🚨 注意事项

1. **反爬虫机制**: 墨刀可能有反爬虫措施，建议适当调整等待时间
2. **网络稳定性**: 确保网络连接稳定，避免抓取中断
3. **资源消耗**: 抓取过程会消耗较多内存和CPU资源
4. **法律合规**: 请确保遵守网站的使用条款和法律法规

## 🐛 故障排除

### 常见问题

1. **Playwright安装失败**
   ```bash
   # 重新安装
   pip uninstall playwright
   pip install playwright
   playwright install chromium
   ```

2. **页面加载超时**
   ```python
   # 增加超时时间
   await page.goto(url, timeout=120000)  # 2分钟
   ```

3. **截图失败**
   ```python
   # 检查页面是否完全加载
   await page.wait_for_load_state('domcontentloaded')
   ```

### 调试模式

```python
# 启用有头模式进行调试
browser = await playwright.chromium.launch(headless=False)
```

## 📈 性能优化

1. **并发抓取**: 使用异步并发处理多个页面
2. **资源限制**: 限制同时打开的浏览器实例数量
3. **缓存机制**: 缓存已抓取的页面避免重复请求
4. **增量更新**: 只抓取变化的部分

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

---

**作者**: AI Assistant  
**版本**: 1.0.0  
**更新时间**: 2024年1月