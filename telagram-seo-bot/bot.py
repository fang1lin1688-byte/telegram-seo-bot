{\rtf1\ansi\ansicpg936\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
"""\
Telegram SEO Bot - \uc0\u33258 \u21160 \u21270 \u20248 \u21270 \u21161 \u25163 \
\uc0\u21151 \u33021 \u65306 SEO\u35786 \u26029 \u12289 \u20851 \u38190 \u35789 \u30417 \u25511 \u12289 \u20869 \u23481 \u20248 \u21270 \u24314 \u35758 \u12289 \u25968 \u25454 \u36861 \u36394 \
"""\
\
import asyncio\
import json\
import re\
import os\
from datetime import datetime, timedelta\
from collections import Counter\
from telethon import TelegramClient, events\
from telethon.tl.functions.channels import GetFullChannelRequest\
from telethon.tl.functions.messages import GetHistoryRequest\
\
from config import (\
    API_ID, API_HASH, BOT_TOKEN, TARGET_KEYWORDS,\
    CONTENT_RULES, POSTING_SCHEDULE, SESSION_PATH, DATA_DIR\
)\
\
\
class TelegramSEOBot:\
    def __init__(self):\
        self.client = TelegramClient(SESSION_PATH, API_ID, API_HASH)\
        self.bot_token = BOT_TOKEN\
        self.config = \{\
            'target_keywords': [k.strip() for k in TARGET_KEYWORDS],\
            'competitor_channels': [c.strip() for c in COMPETITOR_CHANNELS],\
            'content_rules': CONTENT_RULES,\
            'posting_schedule': POSTING_SCHEDULE\
        \}\
        self.monitored_channels = self.load_monitored_channels()\
        \
    def load_monitored_channels(self):\
        """\uc0\u21152 \u36733 \u30417 \u25511 \u21015 \u34920 """\
        file_path = f'\{DATA_DIR\}/monitored_channels.json'\
        try:\
            with open(file_path, 'r', encoding='utf-8') as f:\
                return json.load(f)\
        except:\
            return \{\}\
    \
    def save_monitored_channels(self):\
        """\uc0\u20445 \u23384 \u30417 \u25511 \u21015 \u34920 """\
        file_path = f'\{DATA_DIR\}/monitored_channels.json'\
        with open(file_path, 'w', encoding='utf-8') as f:\
            json.dump(self.monitored_channels, f, ensure_ascii=False, indent=2)\
    \
    async def start(self):\
        """\uc0\u21551 \u21160 \u26426 \u22120 \u20154 """\
        print(f"\uc0\u55357 \u56960  \u27491 \u22312 \u21551 \u21160  Telegram SEO Bot...")\
        print(f"\uc0\u55357 \u56522  \u25968 \u25454 \u30446 \u24405 : \{DATA_DIR\}")\
        print(f"\uc0\u55356 \u57263  \u30446 \u26631 \u20851 \u38190 \u35789 : \{self.config['target_keywords']\}")\
        \
        await self.client.start(bot_token=self.bot_token)\
        me = await self.client.get_me()\
        print(f"\uc0\u9989  \u26426 \u22120 \u20154 \u24050 \u21551 \u21160 : @\{me.username\}")\
        \
        self.register_handlers()\
        print("\uc0\u55357 \u56541  \u31995 \u32479 \u24050 \u23601 \u32490 \u65292 \u31561 \u24453 \u21629 \u20196 ...")\
        await self.client.run_until_disconnected()\
    \
    def register_handlers(self):\
        """\uc0\u27880 \u20876 \u21629 \u20196 \u22788 \u29702 \u22120 """\
        \
        @self.client.on(events.NewMessage(pattern='/start'))\
        async def start_handler(event):\
            welcome_text = """\
\uc0\u55358 \u56598  **Telegram SEO Bot** - \u20320 \u30340 \u39057 \u36947 \u20248 \u21270 \u21161 \u25163 \
\
\uc0\u25105 \u21487 \u20197 \u24110 \u20320 \u65306 \
\uc0\u55357 \u56522  **SEO\u35786 \u26029 ** - \u20998 \u26512 \u39057 \u36947 \u20248 \u21270 \u24230 \
\uc0\u55357 \u56520  **\u25968 \u25454 \u30417 \u25511 ** - \u36861 \u36394 \u20851 \u38190 \u25351 \u26631 \
\uc0\u55357 \u56481  **\u20869 \u23481 \u24314 \u35758 ** - \u29983 \u25104 \u20248 \u21270 \u26041 \u26696 \
\uc0\u55357 \u56589  **\u20851 \u38190 \u35789 \u20998 \u26512 ** - \u26816 \u26597 \u23494 \u24230 \u21644 \u25490 \u21517 \
\
**\uc0\u24555 \u36895 \u24320 \u22987 \u65306 **\
/audit `@\uc0\u20320 \u30340 \u39057 \u36947 ` - \u20840 \u38754 SEO\u35786 \u26029 \
/monitor `@\uc0\u20320 \u30340 \u39057 \u36947 ` - \u24320 \u22987 \u30417 \u25511 \
/suggest - \uc0\u33719 \u21462 \u20869 \u23481 \u24314 \u35758 \
/help - \uc0\u26597 \u30475 \u25152 \u26377 \u21629 \u20196 \
            """\
            await event.respond(welcome_text.strip())\
        \
        @self.client.on(events.NewMessage(pattern='/help'))\
        async def help_handler(event):\
            help_text = """\
\uc0\u55357 \u56538  **\u21487 \u29992 \u21629 \u20196 \u21015 \u34920 **\
\
**\uc0\u35786 \u26029 \u20998 \u26512 \u65306 **\
/audit `<\uc0\u39057 \u36947 \u21517 >` - SEO\u20840 \u38754 \u35786 \u26029 \
/keywords - \uc0\u26597 \u30475 \u20851 \u38190 \u35789 \u34920 \u29616 \
\
**\uc0\u30417 \u25511 \u31649 \u29702 \u65306 **\
/monitor `<\uc0\u39057 \u36947 \u21517 >` - \u28155 \u21152 \u30417 \u25511 \
/unmonitor `<\uc0\u39057 \u36947 \u21517 >` - \u21462 \u28040 \u30417 \u25511 \
/list - \uc0\u26597 \u30475 \u30417 \u25511 \u21015 \u34920 \
\
**\uc0\u20869 \u23481 \u20248 \u21270 \u65306 **\
/suggest `<\uc0\u20027 \u39064 >` - \u29983 \u25104 \u20248 \u21270 \u20869 \u23481 \
/schedule - \uc0\u26597 \u30475 \u26368 \u20339 \u21457 \u24067 \u26102 \u38388 \
\
**\uc0\u25968 \u25454 \u25253 \u21578 \u65306 **\
/report `<\uc0\u39057 \u36947 \u21517 >` - \u29983 \u25104 \u25968 \u25454 \u25253 \u21578 \
\
**\uc0\u31995 \u32479 \u65306 **\
/status - \uc0\u26597 \u30475 \u31995 \u32479 \u29366 \u24577 \
/config - \uc0\u26597 \u30475 \u24403 \u21069 \u37197 \u32622 \
\
\uc0\u55357 \u56481  **\u25552 \u31034 \u65306 ** \u39057 \u36947 \u21517 \u38656 \u21253 \u21547 @\u31526 \u21495 \u65292 \u22914  @channelname\
            """\
            await event.respond(help_text.strip())\
        \
        @self.client.on(events.NewMessage(pattern='/audit (@\\\\w+)'))\
        async def audit_handler(event):\
            channel = event.pattern_match.group(1)\
            await event.respond(f"\uc0\u55357 \u56589  \u27491 \u22312 \u20998 \u26512  \{channel\} \u30340 SEO\u29366 \u24577 \u65292 \u35831 \u31245 \u20505 ...")\
            \
            try:\
                analysis = await self.analyze_channel_seo(channel)\
                if 'error' in analysis:\
                    await event.respond(f"\uc0\u10060  \u20998 \u26512 \u22833 \u36133 \u65306 \{analysis['error']\}")\
                    return\
                \
                report = self.format_audit_report(analysis, channel)\
                await event.respond(report)\
                self.save_analysis(channel, analysis)\
                \
            except Exception as e:\
                await event.respond(f"\uc0\u10060  \u20998 \u26512 \u20986 \u38169 \u65306 \{str(e)\}")\
        \
        @self.client.on(events.NewMessage(pattern='/monitor (@\\\\w+)'))\
        async def monitor_handler(event):\
            channel = event.pattern_match.group(1)\
            \
            if channel in self.monitored_channels:\
                await event.respond(f"\uc0\u9888 \u65039  \{channel\} \u24050 \u22312 \u30417 \u25511 \u21015 \u34920 \u20013 ")\
                return\
            \
            self.monitored_channels[channel] = \{\
                'added_at': datetime.now().isoformat(),\
                'added_by': event.sender_id\
            \}\
            self.save_monitored_channels()\
            \
            await event.respond(f"""\
\uc0\u9989  **\u24050 \u28155 \u21152 \u30417 \u25511 **\
\
\uc0\u39057 \u36947 \u65306 \{channel\}\
\uc0\u28155 \u21152 \u26102 \u38388 \u65306 \{datetime.now().strftime('%Y-%m-%d %H:%M')\}\
\
**\uc0\u33258 \u21160 \u20219 \u21153 \u65306 **\
\'95 \uc0\u27599 \u26085 09:00 SEO\u20581 \u24247 \u26816 \u26597 \
\'95 \uc0\u27599 \u21608 \u19968 \u25968 \u25454 \u25253 \u21578 \
\
\uc0\u20351 \u29992  /list \u26597 \u30475 \u25152 \u26377 \u30417 \u25511 \u39057 \u36947 \
            """)\
        \
        @self.client.on(events.NewMessage(pattern='/unmonitor (@\\\\w+)'))\
        async def unmonitor_handler(event):\
            channel = event.pattern_match.group(1)\
            \
            if channel not in self.monitored_channels:\
                await event.respond(f"\uc0\u9888 \u65039  \{channel\} \u19981 \u22312 \u30417 \u25511 \u21015 \u34920 \u20013 ")\
                return\
            \
            del self.monitored_channels[channel]\
            self.save_monitored_channels()\
            \
            await event.respond(f"\uc0\u9989  \u24050 \u21462 \u28040 \u30417 \u25511  \{channel\}")\
        \
        @self.client.on(events.NewMessage(pattern='/list'))\
        async def list_handler(event):\
            if not self.monitored_channels:\
                await event.respond("\uc0\u55357 \u56557  \u24403 \u21069 \u27809 \u26377 \u30417 \u25511 \u20219 \u20309 \u39057 \u36947 ")\
                return\
            \
            text = "\uc0\u55357 \u56522  **\u30417 \u25511 \u39057 \u36947 \u21015 \u34920 **\\n\\n"\
            for i, (channel, info) in enumerate(self.monitored_channels.items(), 1):\
                added_time = datetime.fromisoformat(info['added_at']).strftime('%m-%d')\
                text += f"\{i\}. \{channel\} (\uc0\u28155 \u21152 \u20110  \{added_time\})\\n"\
            \
            text += f"\\n\uc0\u20849  \{len(self.monitored_channels)\} \u20010 \u39057 \u36947 "\
            await event.respond(text)\
        \
        @self.client.on(events.NewMessage(pattern='/suggest(.*)'))\
        async def suggest_handler(event):\
            topic = event.pattern_match.group(1).strip() or "\uc0\u28909 \u38376 \u35805 \u39064 "\
            \
            await event.respond(f"\uc0\u55357 \u56481  \u27491 \u22312 \u29983 \u25104 \u12300 \{topic\}\u12301 \u30340 \u20248 \u21270 \u20869 \u23481 ...")\
            \
            try:\
                suggestions = await self.generate_optimized_content(topic)\
                response = f"""\
\uc0\u55357 \u56481  **SEO\u20248 \u21270 \u20869 \u23481 \u24314 \u35758 **\
\
**\uc0\u20027 \u39064 \u65306 ** \{topic\}\
\
**\uc0\u25512 \u33616 \u26631 \u39064 \u65306 **\
\{suggestions['title']\}\
\
**\uc0\u24320 \u22836 Hook\u65288 \u21560 \u24341 \u28857 \u20987 \u65289 \u65306 **\
\{suggestions['hook']\}\
\
**\uc0\u34892 \u21160 \u21495 \u21484 \u65288 CTA\u65289 \u65306 **\
\{suggestions['cta']\}\
\
**\uc0\u25512 \u33616 \u26631 \u31614 \u65306 **\
\{' '.join(suggestions['hashtags'])\}\
\
**\uc0\u20851 \u38190 \u35789 \u24067 \u23616 \u65306 **\
\'95 \uc0\u26631 \u39064 \u21069 15\u23383 \u65306 \{suggestions['keywords_in_title']\}\
\'95 \uc0\u39044 \u20272 \u20851 \u38190 \u35789 \u23494 \u24230 \u65306 \{suggestions['keyword_density']\}%\
\
\uc0\u9989  \u25353 \u27492 \u32467 \u26500 \u21457 \u24067 \u65292 \u25628 \u32034 \u25490 \u21517 \u25552 \u21319 50%+\
                """\
                await event.respond(response.strip())\
                \
            except Exception as e:\
                await event.respond(f"\uc0\u10060  \u29983 \u25104 \u22833 \u36133 \u65306 \{str(e)\}")\
        \
        @self.client.on(events.NewMessage(pattern='/report (@\\\\w+)'))\
        async def report_handler(event):\
            channel = event.pattern_match.group(1)\
            \
            await event.respond(f"\uc0\u55357 \u56520  \u27491 \u22312 \u29983 \u25104  \{channel\} \u30340 \u25968 \u25454 \u25253 \u21578 ...")\
            \
            try:\
                metrics = await self.track_channel_metrics(channel)\
                report = self.format_metrics_report(channel, metrics)\
                await event.respond(report)\
            except Exception as e:\
                await event.respond(f"\uc0\u10060  \u25253 \u21578 \u29983 \u25104 \u22833 \u36133 \u65306 \{str(e)\}")\
        \
        @self.client.on(events.NewMessage(pattern='/keywords'))\
        async def keywords_handler(event):\
            keywords_text = "\uc0\u55356 \u57263  **\u24403 \u21069 \u30446 \u26631 \u20851 \u38190 \u35789 **\\n\\n"\
            for i, kw in enumerate(self.config['target_keywords'], 1):\
                keywords_text += f"\{i\}. \{kw\}\\n"\
            \
            keywords_text += f"\\n\uc0\u55357 \u56481  **\u20248 \u21270 \u24314 \u35758 \u65306 **\\n"\
            keywords_text += "\'95 \uc0\u39057 \u36947 \u21517 \u24212 \u21253 \u21547 \u21069 3\u20010 \u20851 \u38190 \u35789 \u20043 \u19968 \\n"\
            keywords_text += "\'95 \uc0\u25551 \u36848 \u21069 60\u23383 \u24517 \u39035 \u20986 \u29616 \u26680 \u24515 \u20851 \u38190 \u35789 \\n"\
            keywords_text += "\'95 \uc0\u27599 \u31687 \u20869 \u23481 \u20445 \u25345 2-3%\u20851 \u38190 \u35789 \u23494 \u24230 "\
            \
            await event.respond(keywords_text)\
        \
        @self.client.on(events.NewMessage(pattern='/config'))\
        async def config_handler(event):\
            config_text = f"""\
\uc0\u9881 \u65039  **\u24403 \u21069 SEO\u37197 \u32622 **\
\
**\uc0\u30446 \u26631 \u20851 \u38190 \u35789 \u65306 ** \{', '.join(self.config['target_keywords'])\}\
**\uc0\u30417 \u25511 \u39057 \u36947 \u25968 \u65306 ** \{len(self.monitored_channels)\}\
\
**\uc0\u20869 \u23481 \u35268 \u21017 \u65306 **\
\'95 \uc0\u26631 \u39064 \u38271 \u24230  \u8804  \{CONTENT_RULES['title_max_length']\}\u23383 \u31526 \
\'95 \uc0\u25551 \u36848 \u38271 \u24230  \u8804  \{CONTENT_RULES['desc_max_length']\}\u23383 \u31526 \
\'95 \uc0\u20851 \u38190 \u35789 \u23494 \u24230  \{CONTENT_RULES['keyword_density']*100\}%\
\'95 \uc0\u26368 \u20302 \u20114 \u21160 \u29575  \{CONTENT_RULES['min_engagement_rate']*100\}%\
\
**\uc0\u21457 \u24067 \u35745 \u21010 \u65306 **\
\'95 \uc0\u26368 \u20339 \u26102 \u38388 \u65306 \{', '.join(POSTING_SCHEDULE['optimal_times'])\}\
\'95 \uc0\u21457 \u24067 \u39057 \u29575 \u65306 \{POSTING_SCHEDULE['frequency']\}\
            """\
            await event.respond(config_text.strip())\
        \
        @self.client.on(events.NewMessage(pattern='/status'))\
        async def status_handler(event):\
            uptime = datetime.now() - datetime.fromtimestamp(os.path.getctime(__file__))\
            status_text = f"""\
\uc0\u55358 \u56598  **\u31995 \u32479 \u29366 \u24577 **\
\
**\uc0\u36816 \u34892 \u29366 \u24577 \u65306 ** \u9989  \u27491 \u24120 \
**\uc0\u36816 \u34892 \u26102 \u38388 \u65306 ** \{uptime.days\}\u22825  \{uptime.seconds//3600\}\u23567 \u26102 \
**\uc0\u30417 \u25511 \u39057 \u36947 \u65306 ** \{len(self.monitored_channels)\}\u20010 \
**\uc0\u25968 \u25454 \u30446 \u24405 \u65306 ** \{DATA_DIR\}\
            """\
            await event.respond(status_text.strip())\
    \
    async def analyze_channel_seo(self, channel_username):\
        """\uc0\u20998 \u26512 \u39057 \u36947 SEO\u29366 \u24577 """\
        try:\
            channel = await self.client.get_entity(channel_username)\
            full = await self.client(GetFullChannelRequest(channel))\
            \
            title = channel.title\
            description = full.full_chat.about or ""\
            \
            seo_score = 0\
            suggestions = []\
            checks = []\
            \
            title_check = self.check_title_optimization(title)\
            seo_score += title_check['score']\
            suggestions.extend(title_check['suggestions'])\
            checks.append(('\uc0\u26631 \u39064 \u20248 \u21270 ', title_check['score'], 30))\
            \
            desc_check = self.check_description_optimization(description)\
            seo_score += desc_check['score']\
            suggestions.extend(desc_check['suggestions'])\
            checks.append(('\uc0\u25551 \u36848 \u20248 \u21270 ', desc_check['score'], 30))\
            \
            keyword_analysis = self.analyze_keyword_density(title, description)\
            keyword_score = self.calculate_keyword_score(keyword_analysis)\
            seo_score += keyword_score\
            checks.append(('\uc0\u20851 \u38190 \u35789 \u24067 \u23616 ', keyword_score, 20))\
            \
            activity_score = await self.assess_channel_activity(channel)\
            seo_score += activity_score\
            checks.append(('\uc0\u27963 \u36291 \u24230 ', activity_score, 20))\
            \
            return \{\
                'channel': channel_username,\
                'seo_score': min(100, seo_score),\
                'title': title,\
                'description': description,\
                'suggestions': suggestions,\
                'checks': checks,\
                'keyword_analysis': keyword_analysis,\
                'timestamp': datetime.now().isoformat()\
            \}\
            \
        except Exception as e:\
            return \{'error': str(e)\}\
    \
    def check_title_optimization(self, title):\
        """\uc0\u26816 \u26597 \u26631 \u39064 \u20248 \u21270 \u24230 """\
        score = 0\
        suggestions = []\
        \
        if len(title) <= 30:\
            score += 10\
        else:\
            suggestions.append(f"\uc0\u9888 \u65039  \u26631 \u39064 \u36807 \u38271 (\{len(title)\}\u23383 \u31526 )\u65292 \u24314 \u35758 \u8804 30\u23383 \u31526 ")\
        \
        keywords = self.config['target_keywords']\
        has_keyword_front = any(kw in title[:15] for kw in keywords)\
        if has_keyword_front:\
            score += 10\
        else:\
            suggestions.append("\uc0\u55357 \u56481  \u24314 \u35758 \u23558 \u26680 \u24515 \u20851 \u38190 \u35789 \u25918 \u22312 \u26631 \u39064 \u21069 15\u20010 \u23383 \u31526 \u20869 ")\
        \
        if '|' in title or '\'b7' in title:\
            score += 5\
        else:\
            suggestions.append("\uc0\u55357 \u56481  \u24314 \u35758 \u20351 \u29992 '|'\u25110 '\'b7'\u20998 \u38548 \u20851 \u38190 \u35789 ")\
        \
        has_chinese = bool(re.search(r'[\\u4e00-\\u9fff]', title))\
        has_english = bool(re.search(r'[a-zA-Z]', title))\
        if has_chinese and has_english:\
            score += 5\
        else:\
            suggestions.append("\uc0\u55357 \u56481  \u24314 \u35758 \u21516 \u26102 \u21253 \u21547 \u20013 \u33521 \u25991 \u20851 \u38190 \u35789 ")\
        \
        return \{'score': score, 'suggestions': suggestions\}\
    \
    def check_description_optimization(self, description):\
        """\uc0\u26816 \u26597 \u25551 \u36848 \u20248 \u21270 \u24230 """\
        score = 0\
        suggestions = []\
        \
        if 50 <= len(description) <= 140:\
            score += 10\
        elif len(description) > 140:\
            suggestions.append(f"\uc0\u9888 \u65039  \u25551 \u36848 \u36807 \u38271 (\{len(description)\}\u23383 \u31526 )")\
        else:\
            suggestions.append(f"\uc0\u55357 \u56481  \u25551 \u36848 \u36807 \u30701 (\{len(description)\}\u23383 \u31526 )")\
        \
        keywords = self.config['target_keywords']\
        front_keywords = [kw for kw in keywords if kw in description[:60]]\
        if front_keywords:\
            score += 10\
        else:\
            suggestions.append("\uc0\u55357 \u56481  \u25551 \u36848 \u21069 60\u23383 \u31526 \u24517 \u39035 \u21253 \u21547 \u26680 \u24515 \u20851 \u38190 \u35789 ")\
        \
        keyword_counts = Counter()\
        for kw in keywords:\
            keyword_counts[kw] = description.lower().count(kw.lower())\
        \
        overused = [kw for kw, count in keyword_counts.items() if count > 3]\
        if overused:\
            suggestions.append(f"\uc0\u9888 \u65039  \u20851 \u38190 \u35789 \u37325 \u22797 \u36807 \u22810 ")\
        else:\
            score += 5\
        \
        if any(cta in description for cta in ['\uc0\u35746 \u38405 ', '\u20851 \u27880 ', '\u21152 \u20837 ', '\u28857 \u20987 ']):\
            score += 5\
        else:\
            suggestions.append("\uc0\u55357 \u56481  \u24314 \u35758 \u28155 \u21152 \u34892 \u21160 \u21495 \u21484 ")\
        \
        return \{'score': score, 'suggestions': suggestions\}\
    \
    def analyze_keyword_density(self, title, description):\
        """\uc0\u20998 \u26512 \u20851 \u38190 \u35789 \u23494 \u24230 """\
        full_text = f"\{title\} \{description\}".lower()\
        words = re.findall(r'\\b\\w+\\b', full_text)\
        total_words = len(words)\
        \
        keyword_data = \{\}\
        for keyword in self.config['target_keywords']:\
            count = full_text.count(keyword.lower())\
            density = (count / total_words * 100) if total_words > 0 else 0\
            keyword_data[keyword] = \{\
                'count': count,\
                'density': round(density, 2),\
                'optimal': 1.5 <= density <= 5.0\
            \}\
        \
        return keyword_data\
    \
    def calculate_keyword_score(self, keyword_analysis):\
        """\uc0\u35745 \u31639 \u20851 \u38190 \u35789 \u24471 \u20998 """\
        optimal_count = sum(1 for data in keyword_analysis.values() if data['optimal'])\
        if optimal_count >= 2:\
            return 20\
        elif optimal_count == 1:\
            return 15\
        else:\
            return 10\
    \
    async def assess_channel_activity(self, channel):\
        """\uc0\u35780 \u20272 \u39057 \u36947 \u27963 \u36291 \u24230 """\
        try:\
            messages = await self.client(GetHistoryRequest(\
                peer=channel,\
                limit=10,\
                offset_date=None,\
                offset_id=0,\
                max_id=0,\
                min_id=0,\
                add_offset=0,\
                hash=0\
            ))\
            \
            if not messages.messages:\
                return 5\
            \
            total_views = 0\
            valid_messages = 0\
            \
            for msg in messages.messages:\
                if hasattr(msg, 'views') and msg.views:\
                    total_views += msg.views\
                    valid_messages += 1\
            \
            if valid_messages == 0:\
                return 5\
            \
            avg_views = total_views / valid_messages\
            \
            if avg_views > 10000:\
                return 20\
            elif avg_views > 5000:\
                return 18\
            elif avg_views > 1000:\
                return 15\
            elif avg_views > 500:\
                return 12\
            else:\
                return 10\
                \
        except:\
            return 10\
    \
    def format_audit_report(self, analysis, channel):\
        """\uc0\u26684 \u24335 \u21270 \u35786 \u26029 \u25253 \u21578 """\
        report = f"""\
\uc0\u55357 \u56522  **\{channel\} SEO\u35786 \u26029 \u25253 \u21578 **\
\uc0\u29983 \u25104 \u26102 \u38388 \u65306 \{datetime.now().strftime('%Y-%m-%d %H:%M')\}\
\
\uc0\u55356 \u57263  **\u32508 \u21512 \u35780 \u20998 \u65306 \{analysis['seo_score']\}/100**\
\
**\uc0\u35814 \u32454 \u35780 \u20998 \u65306 **\
"""\
        for check_name, score, total in analysis['checks']:\
            bar = '\uc0\u9608 ' * (score // 5) + '\u9617 ' * ((total - score) // 5)\
            report += f"\\n\{check_name\}: \{bar\} \{score\}/\{total\}"\
        \
        report += "\\n\\n\uc0\u55357 \u56523  **\u20248 \u21270 \u24314 \u35758 \u65306 **"\
        for suggestion in analysis['suggestions']:\
            report += f"\\n\{suggestion\}"\
        \
        report += "\\n\\n\uc0\u55357 \u56593  **\u20851 \u38190 \u35789 \u20998 \u26512 \u65306 **"\
        for kw, data in analysis['keyword_analysis'].items():\
            status = "\uc0\u9989 " if data['optimal'] else "\u9888 \u65039 "\
            report += f"\\n\{status\} \{kw\}: \{data['density']\}% (\uc0\u20986 \u29616 \{data['count']\}\u27425 )"\
        \
        score = analysis['seo_score']\
        if score >= 80:\
            level = "\uc0\u55356 \u57286  \u20248 \u31168 "\
        elif score >= 60:\
            level = "\uc0\u9989  \u33391 \u22909 "\
        elif score >= 40:\
            level = "\uc0\u9888 \u65039  \u19968 \u33324 "\
        else:\
            level = "\uc0\u10060  \u38656 \u25913 \u36827 "\
        \
        report += f"\\n\\n**\uc0\u35780 \u32423 \u65306 \{level\}**"\
        report += "\\n\\n\uc0\u55357 \u56481  \u20351 \u29992  /suggest \u33719 \u21462 \u20248 \u21270 \u20869 \u23481 \u27169 \u26495 "\
        \
        return report\
    \
    async def generate_optimized_content(self, topic):\
        """\uc0\u29983 \u25104 \u20248 \u21270 \u20869 \u23481 """\
        keywords = self.config['target_keywords']\
        primary_kw = keywords[0] if keywords else topic\
        \
        title_templates = [\
            f"\{primary_kw\} | \{topic\}\uc0\u20840 \u25915 \u30053 ",\
            f"\{primary_kw\} \'b7 \uc0\u27599 \u26085 \u31934 \u36873 \u65306 \{topic\}",\
            f"\uc0\u12304 \{primary_kw\}\u12305 \{topic\}\u23454 \u25112 \u25351 \u21335 "\
        ]\
        title = title_templates[0]\
        \
        hooks = [\
            f"\uc0\u55357 \u56613  \u20851 \u20110 \{topic\}\u65292 90%\u30340 \u20154 \u37117 \u24573 \u30053 \u20102 \u36825 3\u20010 \u20851 \u38190 \u28857 ",\
            f"\uc0\u55357 \u56520  \{topic\}\u26368 \u26032 \u36235 \u21183 \u65306 \u25484 \u25569 \u36825 5\u20010 \u25216 \u24039 \u25928 \u29575 \u32763 \u20493 ",\
            f"\uc0\u55357 \u56481  \u28145 \u32789 \{topic\}3\u24180 \u65292 \u24635 \u32467 \u20986 \u36825 \u22871 \u26680 \u24515 \u26041 \u27861 \u35770 "\
        ]\
        hook = hooks[datetime.now().day % len(hooks)]\
        \
        cta = f"""\
\uc0\u55357 \u56390  \u28857 \u20987 \u19978 \u26041 \u38142 \u25509 \u26597 \u30475 \u23436 \u25972 \u20869 \u23481 \
\uc0\u55357 \u56492  \u22312 \u35780 \u35770 \u21306 \u20998 \u20139 \u20320 \u30340 \{topic\}\u32463 \u39564 \
\uc0\u55357 \u56548  \u36716 \u21457 \u32473 \u38656 \u35201 \u30340 \u26379 \u21451 \
        """.strip()\
        \
        hashtags = [f"#\{kw.replace(' ', '')\}" for kw in keywords[:3]]\
        \
        keywords_in_title = "\uc0\u9989  \u24050 \u21253 \u21547 " if primary_kw in title[:15] else "\u10060  \u38656 \u35843 \u25972 "\
        \
        full_text = f"\{title\} \{hook\}"\
        word_count = len(re.findall(r'\\b\\w+\\b', full_text))\
        kw_count = sum(full_text.count(kw) for kw in keywords)\
        density = round((kw_count / word_count * 100) if word_count > 0 else 0, 2)\
        \
        return \{\
            'title': title,\
            'hook': hook,\
            'cta': cta,\
            'hashtags': hashtags,\
            'keywords_in_title': keywords_in_title,\
            'keyword_density': density\
        \}\
    \
    async def track_channel_metrics(self, channel_username):\
        """\uc0\u36861 \u36394 \u39057 \u36947 \u25351 \u26631 """\
        try:\
            channel = await self.client.get_entity(channel_username)\
            \
            messages = await self.client(GetHistoryRequest(\
                peer=channel,\
                limit=30,\
                offset_date=None,\
                offset_id=0,\
                max_id=0,\
                min_id=0,\
                add_offset=0,\
                hash=0\
            ))\
            \
            metrics = \{\
                'total_posts': len(messages.messages),\
                'avg_views': 0,\
                'avg_forwards': 0,\
                'engagement_rate': 0,\
                'best_posts': [],\
                'posting_frequency': 0\
            \}\
            \
            if messages.messages:\
                views = []\
                forwards = []\
                dates = []\
                \
                for msg in messages.messages:\
                    if hasattr(msg, 'views') and msg.views:\
                        views.append(msg.views)\
                    if hasattr(msg, 'forwards') and msg.forwards:\
                        forwards.append(msg.forwards)\
                    dates.append(msg.date)\
                    \
                    if msg.views and msg.views > 1000:\
                        metrics['best_posts'].append(\{\
                            'id': msg.id,\
                            'views': msg.views,\
                            'text': msg.message[:80] if msg.message else '[\uc0\u23186 \u20307 \u20869 \u23481 ]',\
                            'date': msg.date.strftime('%m-%d')\
                        \})\
                \
                if views:\
                    metrics['avg_views'] = int(sum(views) / len(views))\
                if forwards:\
                    metrics['avg_forwards'] = round(sum(forwards) / len(forwards), 1)\
                \
                if views and forwards:\
                    metrics['engagement_rate'] = round((sum(forwards) / sum(views)) * 100, 2)\
                \
                if len(dates) >= 2:\
                    date_range = (dates[0] - dates[-1]).days\
                    metrics['posting_frequency'] = round(len(messages.messages) / max(1, date_range), 1)\
            \
            self.save_metrics(channel_username, metrics)\
            return metrics\
            \
        except Exception as e:\
            return \{'error': str(e)\}\
    \
    def save_metrics(self, channel, metrics):\
        """\uc0\u20445 \u23384 \u25351 \u26631 """\
        file_path = f'\{DATA_DIR\}/metrics_\{channel.replace("@", "")\}.json'\
        try:\
            with open(file_path, 'r', encoding='utf-8') as f:\
                history = json.load(f)\
        except:\
            history = []\
        \
        history.append(\{\
            'date': datetime.now().isoformat(),\
            'metrics': metrics\
        \})\
        \
        history = history[-30:]\
        \
        with open(file_path, 'w', encoding='utf-8') as f:\
            json.dump(history, f, ensure_ascii=False, indent=2)\
    \
    def format_metrics_report(self, channel, metrics):\
        """\uc0\u26684 \u24335 \u21270 \u25351 \u26631 \u25253 \u21578 """\
        if 'error' in metrics:\
            return f"\uc0\u10060  \u33719 \u21462 \u25968 \u25454 \u22833 \u36133 \u65306 \{metrics['error']\}"\
        \
        report = f"""\
\uc0\u55357 \u56520  **\{channel\} \u25968 \u25454 \u25253 \u21578 **\
\uc0\u32479 \u35745 \u26102 \u38388 \u65306 \u26368 \u36817 30\u26465 \u20869 \u23481 \
\
**\uc0\u26680 \u24515 \u25351 \u26631 \u65306 **\
\'95 \uc0\u24179 \u22343 \u38405 \u35835 \u37327 \u65306 \{metrics['avg_views']:,\}\
\'95 \uc0\u24179 \u22343 \u36716 \u21457 \u37327 \u65306 \{metrics['avg_forwards']\}\
\'95 \uc0\u20114 \u21160 \u29575 \u65306 \{metrics['engagement_rate']\}%\
\'95 \uc0\u21457 \u24067 \u39057 \u29575 \u65306 \{metrics['posting_frequency']\}\u31687 /\u22825 \
\
**\uc0\u20869 \u23481 \u34920 \u29616 \u65306 **\
\'95 \uc0\u24635 \u20869 \u23481 \u25968 \u65306 \{metrics['total_posts']\}\u31687 \
\'95 \uc0\u29190 \u27454 \u20869 \u23481 \u25968 \u65306 \{len(metrics['best_posts'])\}\u31687 \u65288 >1000\u38405 \u35835 \u65289 \
\
**\uc0\u28909 \u38376 \u20869 \u23481 TOP3\u65306 **\
"""\
        for i, post in enumerate(metrics['best_posts'][:3], 1):\
            report += f"\\n\{i\}. \uc0\u55357 \u56385  \{post['views']\} | \{post['date']\} | \{post['text']\}"\
        \
        if metrics['avg_views'] > 5000:\
            level = "\uc0\u55356 \u57286  \u22836 \u37096 \u39057 \u36947 "\
        elif metrics['avg_views'] > 1000:\
            level = "\uc0\u9989  \u20248 \u36136 \u39057 \u36947 "\
        elif metrics['avg_views'] > 500:\
            level = "\uc0\u55357 \u56520  \u25104 \u38271 \u39057 \u36947 "\
        else:\
            level = "\uc0\u55356 \u57137  \u26032 \u39057 \u36947 "\
        \
        report += f"\\n\\n**\uc0\u35780 \u32423 \u65306 \{level\}**"\
        report += "\\n\\n\uc0\u55357 \u56481  \u24314 \u35758 \u65306 \u20445 \u25345 \u24403 \u21069 \u26356 \u26032 \u39057 \u29575 \u65292 \u20248 \u21270 \u26631 \u39064 \u20851 \u38190 \u35789 "\
        \
        return report\
    \
    def save_analysis(self, channel, analysis):\
        """\uc0\u20445 \u23384 \u20998 \u26512 \u32467 \u26524 """\
        file_path = f'\{DATA_DIR\}/analysis_\{channel.replace("@", "")\}.json'\
        with open(file_path, 'w', encoding='utf-8') as f:\
            json.dump(analysis, f, ensure_ascii=False, indent=2)\
\
\
async def main():\
    bot = TelegramSEOBot()\
    await bot.start()\
\
\
if __name__ == "__main__":\
    asyncio.run(main())\
}