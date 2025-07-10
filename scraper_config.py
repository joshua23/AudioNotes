#!/usr/bin/env python3
"""
墨刀原型抓取器配置文件
"""

# 墨刀原型链接配置
MOCKINGBOT_URL = "https://modao.cc/proto/MShAKNLmsyponvrscCKL56/sharing?view_mode=read_only&screen=slyifi77UpgXwJoCyfvUjo"

# 浏览器配置
BROWSER_CONFIG = {
    'headless': True,  # 无头模式
    'viewport': {'width': 1920, 'height': 1080},
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'timeout': 60000,  # 页面加载超时时间（毫秒）
    'wait_time': 15,   # 页面渲染等待时间（秒）
}

# 浏览器启动参数
BROWSER_ARGS = [
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

# 输出配置
OUTPUT_CONFIG = {
    'base_dir': 'mockingbot_output',
    'screenshots_dir': 'screenshots',
    'network_dir': 'network',
    'dom_dir': 'dom',
    'reports_dir': 'reports',
}

# 网络请求过滤关键词
API_KEYWORDS = ['api', 'ajax', 'json', 'data', 'rest', 'graphql']

# 报告配置
REPORT_CONFIG = {
    'generate_json': True,
    'generate_markdown': True,
    'generate_html': True,
    'embed_screenshots_in_html': True,
}