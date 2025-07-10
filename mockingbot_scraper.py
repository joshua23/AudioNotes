#!/usr/bin/env python3
"""
墨刀原型全自动抓取器
使用 Headless Playwright 1.53 抓取墨刀原型页面
核心功能：网络接口截获 + DOM抓取 + 截屏 + 结构化输出
"""

import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs

from playwright.async_api import async_playwright, Browser, Page, Response, Request
import markdown
from bs4 import BeautifulSoup
import base64


class MockingBotScraper:
    """墨刀原型抓取器主类"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 存储抓取的数据
        self.network_requests: List[Dict] = []
        self.network_responses: List[Dict] = []
        self.dom_snapshot: Optional[str] = None
        self.screenshots: List[Dict] = []
        self.page_info: Dict = {}
        
        # 创建子目录
        (self.output_dir / "screenshots").mkdir(exist_ok=True)
        (self.output_dir / "network").mkdir(exist_ok=True)
        (self.output_dir / "dom").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
    
    async def setup_browser(self) -> Browser:
        """设置浏览器环境"""
        playwright = await async_playwright().start()
        
        # 启动浏览器，启用网络监听
        browser = await playwright.chromium.launch(
            headless=True,  # 无头模式
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
            ]
        )
        
        return browser
    
    async def setup_page(self, browser: Browser) -> Page:
        """设置页面和网络监听"""
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # 设置网络请求监听
        await self._setup_network_listeners(page)
        
        return page
    
    async def _setup_network_listeners(self, page: Page):
        """设置网络请求和响应监听器"""
        
        async def handle_request(request: Request):
            """处理网络请求"""
            request_data = {
                'url': request.url,
                'method': request.method,
                'headers': dict(request.headers),
                'post_data': request.post_data,
                'timestamp': time.time(),
                'resource_type': request.resource_type,
                'frame': request.frame.name if request.frame else None
            }
            self.network_requests.append(request_data)
        
        async def handle_response(response: Response):
            """处理网络响应"""
            try:
                response_data = {
                    'url': response.url,
                    'status': response.status,
                    'headers': dict(response.headers),
                    'timestamp': time.time(),
                    'content_type': response.headers.get('content-type', ''),
                    'content_length': response.headers.get('content-length', '0')
                }
                
                # 尝试获取响应内容（仅对文本类型）
                if 'text' in response.headers.get('content-type', '').lower():
                    try:
                        response_data['content'] = await response.text()
                    except:
                        response_data['content'] = None
                
                self.network_responses.append(response_data)
            except Exception as e:
                print(f"处理响应时出错: {e}")
        
        # 绑定监听器
        page.on('request', handle_request)
        page.on('response', handle_response)
    
    async def scrape_mockingbot_prototype(self, url: str, wait_time: int = 10) -> Dict:
        """主抓取方法"""
        print(f"开始抓取墨刀原型: {url}")
        
        async with async_playwright() as p:
            browser = await self.setup_browser()
            page = await self.setup_page(browser)
            
            try:
                # 1. 访问页面并等待加载
                print("正在加载页面...")
                await page.goto(url, wait_until='networkidle', timeout=60000)
                
                # 2. 等待页面完全渲染
                print(f"等待页面渲染完成 ({wait_time}秒)...")
                await asyncio.sleep(wait_time)
                
                # 3. 获取页面基本信息
                await self._capture_page_info(page)
                
                # 4. 截获网络接口
                print("正在分析网络请求...")
                await self._analyze_network_requests()
                
                # 5. 抓取DOM结构
                print("正在抓取DOM结构...")
                await self._capture_dom_structure(page)
                
                # 6. 截屏
                print("正在截屏...")
                await self._capture_screenshots(page)
                
                # 7. 生成结构化报告
                print("正在生成报告...")
                report = await self._generate_structured_report()
                
                return report
                
            finally:
                await browser.close()
    
    async def _capture_page_info(self, page: Page):
        """获取页面基本信息"""
        self.page_info = {
            'title': await page.title(),
            'url': page.url,
            'viewport': await page.evaluate('() => ({ width: window.innerWidth, height: window.innerHeight })'),
            'user_agent': await page.evaluate('() => navigator.userAgent'),
            'timestamp': datetime.now().isoformat()
        }
    
    async def _analyze_network_requests(self):
        """分析网络请求，提取API接口"""
        api_endpoints = []
        
        for request in self.network_requests:
            if any(keyword in request['url'].lower() for keyword in ['api', 'ajax', 'json', 'data']):
                api_endpoints.append({
                    'url': request['url'],
                    'method': request['method'],
                    'headers': request['headers'],
                    'post_data': request['post_data'],
                    'resource_type': request['resource_type']
                })
        
        # 保存API接口信息
        api_file = self.output_dir / "network" / "api_endpoints.json"
        with open(api_file, 'w', encoding='utf-8') as f:
            json.dump(api_endpoints, f, ensure_ascii=False, indent=2)
        
        print(f"发现 {len(api_endpoints)} 个API接口")
    
    async def _capture_dom_structure(self, page: Page):
        """抓取DOM结构"""
        # 获取完整的DOM
        dom_content = await page.content()
        self.dom_snapshot = dom_content
        
        # 保存原始DOM
        dom_file = self.output_dir / "dom" / "full_dom.html"
        with open(dom_file, 'w', encoding='utf-8') as f:
            f.write(dom_content)
        
        # 解析DOM结构，提取关键信息
        soup = BeautifulSoup(dom_content, 'html.parser')
        
        # 提取页面结构信息
        page_structure = {
            'title': soup.title.string if soup.title else '',
            'meta_tags': [{'name': meta.get('name'), 'content': meta.get('content')} 
                         for meta in soup.find_all('meta')],
            'scripts': [script.get('src') for script in soup.find_all('script', src=True)],
            'stylesheets': [link.get('href') for link in soup.find_all('link', rel='stylesheet')],
            'images': [img.get('src') for img in soup.find_all('img', src=True)],
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'forms': [{'action': form.get('action'), 'method': form.get('method')} 
                     for form in soup.find_all('form')]
        }
        
        # 保存结构化DOM信息
        structure_file = self.output_dir / "dom" / "page_structure.json"
        with open(structure_file, 'w', encoding='utf-8') as f:
            json.dump(page_structure, f, ensure_ascii=False, indent=2)
        
        print("DOM结构抓取完成")
    
    async def _capture_screenshots(self, page: Page):
        """截屏功能"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 全页面截屏
        full_screenshot_path = self.output_dir / "screenshots" / f"full_page_{timestamp}.png"
        await page.screenshot(path=str(full_screenshot_path), full_page=True)
        
        # 2. 视口截屏
        viewport_screenshot_path = self.output_dir / "screenshots" / f"viewport_{timestamp}.png"
        await page.screenshot(path=str(viewport_screenshot_path))
        
        # 3. 获取页面尺寸信息
        page_size = await page.evaluate('''() => {
            return {
                scrollWidth: document.documentElement.scrollWidth,
                scrollHeight: document.documentElement.scrollHeight,
                clientWidth: document.documentElement.clientWidth,
                clientHeight: document.documentElement.clientHeight
            }
        }''')
        
        self.screenshots = [
            {
                'type': 'full_page',
                'path': str(full_screenshot_path),
                'size': page_size,
                'timestamp': timestamp
            },
            {
                'type': 'viewport',
                'path': str(viewport_screenshot_path),
                'size': page_size,
                'timestamp': timestamp
            }
        ]
        
        print("截屏完成")
    
    async def _generate_structured_report(self) -> Dict:
        """生成结构化报告"""
        report = {
            'metadata': {
                'scraper_version': '1.0.0',
                'timestamp': datetime.now().isoformat(),
                'output_directory': str(self.output_dir)
            },
            'page_info': self.page_info,
            'network_analysis': {
                'total_requests': len(self.network_requests),
                'total_responses': len(self.network_responses),
                'api_endpoints_count': len([r for r in self.network_requests 
                                          if any(k in r['url'].lower() for k in ['api', 'ajax', 'json', 'data'])])
            },
            'dom_analysis': {
                'has_dom_snapshot': bool(self.dom_snapshot),
                'dom_size_bytes': len(self.dom_snapshot) if self.dom_snapshot else 0
            },
            'screenshots': self.screenshots,
            'files_generated': self._get_generated_files()
        }
        
        # 保存JSON报告
        report_file = self.output_dir / "reports" / "scraping_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成Markdown报告
        markdown_report = self._generate_markdown_report(report)
        md_file = self.output_dir / "reports" / "scraping_report.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        
        # 生成HTML报告
        html_report = self._generate_html_report(report)
        html_file = self.output_dir / "reports" / "scraping_report.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        return report
    
    def _get_generated_files(self) -> List[str]:
        """获取生成的文件列表"""
        files = []
        for file_path in self.output_dir.rglob('*'):
            if file_path.is_file():
                files.append(str(file_path.relative_to(self.output_dir)))
        return files
    
    def _generate_markdown_report(self, report: Dict) -> str:
        """生成Markdown格式报告"""
        md_content = f"""# 墨刀原型抓取报告

## 基本信息
- **抓取时间**: {report['metadata']['timestamp']}
- **页面标题**: {report['page_info']['title']}
- **页面URL**: {report['page_info']['url']}

## 网络分析
- **总请求数**: {report['network_analysis']['total_requests']}
- **总响应数**: {report['network_analysis']['total_responses']}
- **API接口数**: {report['network_analysis']['api_endpoints_count']}

## DOM分析
- **DOM快照**: {'已生成' if report['dom_analysis']['has_dom_snapshot'] else '未生成'}
- **DOM大小**: {report['dom_analysis']['dom_size_bytes']} 字节

## 截屏信息
"""
        
        for screenshot in report['screenshots']:
            md_content += f"- **{screenshot['type']}**: {screenshot['path']}\n"
        
        md_content += f"""
## 生成的文件
"""
        
        for file_path in report['files_generated']:
            md_content += f"- {file_path}\n"
        
        return md_content
    
    def _generate_html_report(self, report: Dict) -> str:
        """生成HTML格式报告"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>墨刀原型抓取报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; padding: 10px; background: #e8f4fd; border-radius: 5px; }}
        .screenshot {{ margin: 10px 0; }}
        .screenshot img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 5px; }}
        .file-list {{ background: #f9f9f9; padding: 15px; border-radius: 5px; }}
        .file-list li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>墨刀原型抓取报告</h1>
        <p><strong>抓取时间:</strong> {report['metadata']['timestamp']}</p>
        <p><strong>页面标题:</strong> {report['page_info']['title']}</p>
        <p><strong>页面URL:</strong> <a href="{report['page_info']['url']}" target="_blank">{report['page_info']['url']}</a></p>
    </div>
    
    <div class="section">
        <h2>网络分析</h2>
        <div class="metric"><strong>总请求数:</strong> {report['network_analysis']['total_requests']}</div>
        <div class="metric"><strong>总响应数:</strong> {report['network_analysis']['total_responses']}</div>
        <div class="metric"><strong>API接口数:</strong> {report['network_analysis']['api_endpoints_count']}</div>
    </div>
    
    <div class="section">
        <h2>DOM分析</h2>
        <div class="metric"><strong>DOM快照:</strong> {'已生成' if report['dom_analysis']['has_dom_snapshot'] else '未生成'}</div>
        <div class="metric"><strong>DOM大小:</strong> {report['dom_analysis']['dom_size_bytes']} 字节</div>
    </div>
    
    <div class="section">
        <h2>截屏信息</h2>
"""
        
        for screenshot in report['screenshots']:
            # 将截图转换为base64嵌入HTML
            try:
                with open(screenshot['path'], 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    img_ext = screenshot['path'].split('.')[-1]
                    html_content += f"""
        <div class="screenshot">
            <h3>{screenshot['type']}</h3>
            <img src="data:image/{img_ext};base64,{img_base64}" alt="{screenshot['type']}">
            <p><strong>路径:</strong> {screenshot['path']}</p>
            <p><strong>时间戳:</strong> {screenshot['timestamp']}</p>
        </div>
"""
            except Exception as e:
                html_content += f"""
        <div class="screenshot">
            <h3>{screenshot['type']}</h3>
            <p><strong>路径:</strong> {screenshot['path']} (加载失败: {e})</p>
        </div>
"""
        
        html_content += f"""
    </div>
    
    <div class="section">
        <h2>生成的文件</h2>
        <div class="file-list">
            <ul>
"""
        
        for file_path in report['files_generated']:
            html_content += f"                <li>{file_path}</li>\n"
        
        html_content += """
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        return html_content


async def main():
    """主函数"""
    # 墨刀原型链接
    mockingbot_url = "https://modao.cc/proto/MShAKNLmsyponvrscCKL56/sharing?view_mode=read_only&screen=slyifi77UpgXwJoCyfvUjo"
    
    # 创建抓取器实例
    scraper = MockingBotScraper(output_dir="mockingbot_output")
    
    try:
        # 执行抓取
        report = await scraper.scrape_mockingbot_prototype(
            url=mockingbot_url,
            wait_time=15  # 等待15秒确保页面完全加载
        )
        
        print("\n" + "="*50)
        print("抓取完成！")
        print(f"输出目录: {scraper.output_dir}")
        print(f"页面标题: {report['page_info']['title']}")
        print(f"网络请求数: {report['network_analysis']['total_requests']}")
        print(f"API接口数: {report['network_analysis']['api_endpoints_count']}")
        print(f"截屏数量: {len(report['screenshots'])}")
        print("="*50)
        
        # 显示生成的文件
        print("\n生成的文件:")
        for file_path in report['files_generated']:
            print(f"  - {file_path}")
        
    except Exception as e:
        print(f"抓取过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())