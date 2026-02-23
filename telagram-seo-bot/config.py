{\rtf1\ansi\ansicpg936\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """\
Telegram SEO Bot \uc0\u37197 \u32622 \u25991 \u20214 \
\uc0\u25152 \u26377 \u25935 \u24863 \u20449 \u24687 \u20174 \u29615 \u22659 \u21464 \u37327 \u35835 \u21462 \u65292 \u36866 \u37197  Railway \u37096 \u32626 \
"""\
\
import os\
\
# Telegram API \uc0\u37197 \u32622 \u65288 \u20174 \u29615 \u22659 \u21464 \u37327 \u35835 \u21462 \u65289 \
API_ID = int(os.getenv('API_ID', '0'))\
API_HASH = os.getenv('API_HASH', '')\
BOT_TOKEN = os.getenv('BOT_TOKEN', '')\
\
# SEO \uc0\u37197 \u32622 \
TARGET_KEYWORDS = os.getenv('TARGET_KEYWORDS', 'Telegram\uc0\u33829 \u38144 ,\u39057 \u36947 \u36816 \u33829 ,\u31038 \u32676 \u22686 \u38271 ').split(',')\
COMPETITOR_CHANNELS = os.getenv('COMPETITOR_CHANNELS', '').split(',') if os.getenv('COMPETITOR_CHANNELS') else []\
\
# \uc0\u20869 \u23481 \u35268 \u21017 \
CONTENT_RULES = \{\
    'title_max_length': 30,\
    'desc_max_length': 140,\
    'keyword_density': 0.03,  # 3%\
    'min_engagement_rate': 0.6  # 60%\
\}\
\
# \uc0\u21457 \u24067 \u35745 \u21010 \
POSTING_SCHEDULE = \{\
    'optimal_times': ['09:00', '19:00'],\
    'frequency': 'daily'\
\}\
\
# \uc0\u25968 \u25454 \u23384 \u20648 \u36335 \u24452 \u65288 Railway Volume \u25346 \u36733 \u28857 \u65289 \
DATA_DIR = '/app/data'\
SESSION_PATH = f'\{DATA_DIR\}/seo_bot_session'\
\
# \uc0\u30830 \u20445 \u30446 \u24405 \u23384 \u22312 \
os.makedirs(DATA_DIR, exist_ok=True)\
}