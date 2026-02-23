"""
Telegram SEO Bot 配置文件
所有敏感信息从环境变量读取，适配 Railway 部署
"""

import os

# Telegram API 配置（从环境变量读取）
API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# SEO 配置
TARGET_KEYWORDS = os.getenv('TARGET_KEYWORDS', 'Telegram营销,频道运营,社群增长').split(',')
COMPETITOR_CHANNELS = os.getenv('COMPETITOR_CHANNELS', '').split(',') if os.getenv('COMPETITOR_CHANNELS') else []

# 内容规则
CONTENT_RULES = {
    'title_max_length': 30,
    'desc_max_length': 140,
    'keyword_density': 0.03,  # 3%
    'min_engagement_rate': 0.6  # 60%
}

# 发布计划
POSTING_SCHEDULE = {
    'optimal_times': ['09:00', '19:00'],
    'frequency': 'daily'
}

# 数据存储路径（Railway Volume 挂载点）
DATA_DIR = '/app/data'
SESSION_PATH = f'{DATA_DIR}/seo_bot_session'

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)
