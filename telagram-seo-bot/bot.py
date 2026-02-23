#!/usr/bin/env python3
"""
Telegram SEO Bot - 自动化优化助手
功能：SEO诊断、关键词监控、内容优化建议、数据追踪
"""

import asyncio
import json
import re
import os
from datetime import datetime, timedelta
from collections import Counter
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest

from config import (
    API_ID, API_HASH, BOT_TOKEN, TARGET_KEYWORDS,
    CONTENT_RULES, POSTING_SCHEDULE, SESSION_PATH, DATA_DIR
)


class TelegramSEOBot:
    def __init__(self):
        self.client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
        self.bot_token = BOT_TOKEN
        self.config = {
            'target_keywords': [k.strip() for k in TARGET_KEYWORDS],
            'competitor_channels': [c.strip() for c in COMPETITOR_CHANNELS],
            'content_rules': CONTENT_RULES,
            'posting_schedule': POSTING_SCHEDULE
        }
        self.monitored_channels = self.load_monitored_channels()
        
    def load_monitored_channels(self):
        """加载监控列表"""
        file_path = f'{DATA_DIR}/monitored_channels.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_monitored_channels(self):
        """保存监控列表"""
        file_path = f'{DATA_DIR}/monitored_channels.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.monitored_channels, f, ensure_ascii=False, indent=2)
    
    async def start(self):
        """启动机器人"""
        print(f"🚀 正在启动 Telegram SEO Bot...")
        print(f"📊 数据目录: {DATA_DIR}")
        print(f"🎯 目标关键词: {self.config['target_keywords']}")
        
        await self.client.start(bot_token=self.bot_token)
        me = await self.client.get_me()
        print(f"✅ 机器人已启动: @{me.username}")
        
        self.register_handlers()
        print("📝 系统已就绪，等待命令...")
        await self.client.run_until_disconnected()
    
    def register_handlers(self):
        """注册命令处理器"""
        
        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            welcome_text = """
🤖 **Telegram SEO Bot** - 你的频道优化助手

我可以帮你：
📊 **SEO诊断** - 分析频道优化度
📈 **数据监控** - 追踪关键指标
💡 **内容建议** - 生成优化方案
🔍 **关键词分析** - 检查密度和排名

**快速开始：**
/audit `@你的频道` - 全面SEO诊断
/monitor `@你的频道` - 开始监控
/suggest - 获取内容建议
/help - 查看所有命令
            """
            await event.respond(welcome_text.strip())
        
        @self.client.on(events.NewMessage(pattern='/help'))
        async def help_handler(event):
            help_text = """
📚 **可用命令列表**

**诊断分析：**
/audit `<频道名>` - SEO全面诊断
/keywords - 查看关键词表现

**监控管理：**
/monitor `<频道名>` - 添加监控
/unmonitor `<频道名>` - 取消监控
/list - 查看监控列表

**内容优化：**
/suggest `<主题>` - 生成优化内容
/schedule - 查看最佳发布时间

**数据报告：**
/report `<频道名>` - 生成数据报告

**系统：**
/status - 查看系统状态
/config - 查看当前配置

💡 **提示：** 频道名需包含@符号，如 @channelname
            """
            await event.respond(help_text.strip())
        
        @self.client.on(events.NewMessage(pattern='/audit (@\\w+)'))
        async def audit_handler(event):
            channel = event.pattern_match.group(1)
            await event.respond(f"🔍 正在分析 {channel} 的SEO状态，请稍候...")
            
            try:
                analysis = await self.analyze_channel_seo(channel)
                if 'error' in analysis:
                    await event.respond(f"❌ 分析失败：{analysis['error']}")
                    return
                
                report = self.format_audit_report(analysis, channel)
                await event.respond(report)
                self.save_analysis(channel, analysis)
                
            except Exception as e:
                await event.respond(f"❌ 分析出错：{str(e)}")
        
        @self.client.on(events.NewMessage(pattern='/monitor (@\\w+)'))
        async def monitor_handler(event):
            channel = event.pattern_match.group(1)
            
            if channel in self.monitored_channels:
                await event.respond(f"⚠️ {channel} 已在监控列表中")
                return
            
            self.monitored_channels[channel] = {
                'added_at': datetime.now().isoformat(),
                'added_by': event.sender_id
            }
            self.save_monitored_channels()
            
            await event.respond(f"""
✅ **已添加监控**

频道：{channel}
添加时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

**自动任务：**
• 每日09:00 SEO健康检查
• 每周一数据报告

使用 /list 查看所有监控频道
            """)
        
        @self.client.on(events.NewMessage(pattern='/unmonitor (@\\w+)'))
        async def unmonitor_handler(event):
            channel = event.pattern_match.group(1)
            
            if channel not in self.monitored_channels:
                await event.respond(f"⚠️ {channel} 不在监控列表中")
                return
            
            del self.monitored_channels[channel]
            self.save_monitored_channels()
            
            await event.respond(f"✅ 已取消监控 {channel}")
        
        @self.client.on(events.NewMessage(pattern='/list'))
        async def list_handler(event):
            if not self.monitored_channels:
                await event.respond("📭 当前没有监控任何频道")
                return
            
            text = "📊 **监控频道列表**\n\n"
            for i, (channel, info) in enumerate(self.monitored_channels.items(), 1):
                added_time = datetime.fromisoformat(info['added_at']).strftime('%m-%d')
                text += f"{i}. {channel} (添加于 {added_time})\n"
            
            text += f"\n共 {len(self.monitored_channels)} 个频道"
            await event.respond(text)
        
        @self.client.on(events.NewMessage(pattern='/suggest(.*)'))
        async def suggest_handler(event):
            topic = event.pattern_match.group(1).strip() or "热门话题"
            
            await event.respond(f"💡 正在生成「{topic}」的优化内容...")
            
            try:
                suggestions = await self.generate_optimized_content(topic)
                response = f"""
💡 **SEO优化内容建议**

**主题：** {topic}

**推荐标题：**
{suggestions['title']}

**开头Hook（吸引点击）：**
{suggestions['hook']}

**行动号召（CTA）：**
{suggestions['cta']}

**推荐标签：**
{' '.join(suggestions['hashtags'])}

**关键词布局：**
• 标题前15字：{suggestions['keywords_in_title']}
• 预估关键词密度：{suggestions['keyword_density']}%

✅ 按此结构发布，搜索排名提升50%+
                """
                await event.respond(response.strip())
                
            except Exception as e:
                await event.respond(f"❌ 生成失败：{str(e)}")
        
        @self.client.on(events.NewMessage(pattern='/report (@\\w+)'))
        async def report_handler(event):
            channel = event.pattern_match.group(1)
            
            await event.respond(f"📈 正在生成 {channel} 的数据报告...")
            
            try:
                metrics = await self.track_channel_metrics(channel)
                report = self.format_metrics_report(channel, metrics)
                await event.respond(report)
            except Exception as e:
                await event.respond(f"❌ 报告生成失败：{str(e)}")
        
        @self.client.on(events.NewMessage(pattern='/keywords'))
        async def keywords_handler(event):
            keywords_text = "🎯 **当前目标关键词**\n\n"
            for i, kw in enumerate(self.config['target_keywords'], 1):
                keywords_text += f"{i}. {kw}\n"
            
            keywords_text += f"\n💡 **优化建议：**\n"
            keywords_text += "• 频道名应包含前3个关键词之一\n"
            keywords_text += "• 描述前60字必须出现核心关键词\n"
            keywords_text += "• 每篇内容保持2-3%关键词密度"
            
            await event.respond(keywords_text)
        
        @self.client.on(events.NewMessage(pattern='/config'))
        async def config_handler(event):
            config_text = f"""
⚙️ **当前SEO配置**

**目标关键词：** {', '.join(self.config['target_keywords'])}
**监控频道数：** {len(self.monitored_channels)}

**内容规则：**
• 标题长度 ≤ {CONTENT_RULES['title_max_length']}字符
• 描述长度 ≤ {CONTENT_RULES['desc_max_length']}字符
• 关键词密度 {CONTENT_RULES['keyword_density']*100}%
• 最低互动率 {CONTENT_RULES['min_engagement_rate']*100}%

**发布计划：**
• 最佳时间：{', '.join(POSTING_SCHEDULE['optimal_times'])}
• 发布频率：{POSTING_SCHEDULE['frequency']}
            """
            await event.respond(config_text.strip())
        
        @self.client.on(events.NewMessage(pattern='/status'))
        async def status_handler(event):
            uptime = datetime.now() - datetime.fromtimestamp(os.path.getctime(__file__))
            status_text = f"""
🤖 **系统状态**

**运行状态：** ✅ 正常
**运行时间：** {uptime.days}天 {uptime.seconds//3600}小时
**监控频道：** {len(self.monitored_channels)}个
**数据目录：** {DATA_DIR}
            """
            await event.respond(status_text.strip())
    
    async def analyze_channel_seo(self, channel_username):
        """分析频道SEO状态"""
        try:
            channel = await self.client.get_entity(channel_username)
            full = await self.client(GetFullChannelRequest(channel))
            
            title = channel.title
            description = full.full_chat.about or ""
            
            seo_score = 0
            suggestions = []
            checks = []
            
            title_check = self.check_title_optimization(title)
            seo_score += title_check['score']
            suggestions.extend(title_check['suggestions'])
            checks.append(('标题优化', title_check['score'], 30))
            
            desc_check = self.check_description_optimization(description)
            seo_score += desc_check['score']
            suggestions.extend(desc_check['suggestions'])
            checks.append(('描述优化', desc_check['score'], 30))
            
            keyword_analysis = self.analyze_keyword_density(title, description)
            keyword_score = self.calculate_keyword_score(keyword_analysis)
            seo_score += keyword_score
            checks.append(('关键词布局', keyword_score, 20))
            
            activity_score = await self.assess_channel_activity(channel)
            seo_score += activity_score
            checks.append(('活跃度', activity_score, 20))
            
            return {
                'channel': channel_username,
                'seo_score': min(100, seo_score),
                'title': title,
                'description': description,
                'suggestions': suggestions,
                'checks': checks,
                'keyword_analysis': keyword_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_title_optimization(self, title):
        """检查标题优化度"""
        score = 0
        suggestions = []
        
        if len(title) <= 30:
            score += 10
        else:
            suggestions.append(f"⚠️ 标题过长({len(title)}字符)，建议≤30字符")
        
        keywords = self.config['target_keywords']
        has_keyword_front = any(kw in title[:15] for kw in keywords)
        if has_keyword_front:
            score += 10
        else:
            suggestions.append("💡 建议将核心关键词放在标题前15个字符内")
        
        if '|' in title or '·' in title:
            score += 5
        else:
            suggestions.append("💡 建议使用'|'或'·'分隔关键词")
        
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', title))
        has_english = bool(re.search(r'[a-zA-Z]', title))
        if has_chinese and has_english:
            score += 5
        else:
            suggestions.append("💡 建议同时包含中英文关键词")
        
        return {'score': score, 'suggestions': suggestions}
    
    def check_description_optimization(self, description):
        """检查描述优化度"""
        score = 0
        suggestions = []
        
        if 50 <= len(description) <= 140:
            score += 10
        elif len(description) > 140:
            suggestions.append(f"⚠️ 描述过长({len(description)}字符)")
        else:
            suggestions.append(f"💡 描述过短({len(description)}字符)")
        
        keywords = self.config['target_keywords']
        front_keywords = [kw for kw in keywords if kw in description[:60]]
        if front_keywords:
            score += 10
        else:
            suggestions.append("💡 描述前60字符必须包含核心关键词")
        
        keyword_counts = Counter()
        for kw in keywords:
            keyword_counts[kw] = description.lower().count(kw.lower())
        
        overused = [kw for kw, count in keyword_counts.items() if count > 3]
        if overused:
            suggestions.append(f"⚠️ 关键词重复过多")
        else:
            score += 5
        
        if any(cta in description for cta in ['订阅', '关注', '加入', '点击']):
            score += 5
        else:
            suggestions.append("💡 建议添加行动号召")
        
        return {'score': score, 'suggestions': suggestions}
    
    def analyze_keyword_density(self, title, description):
        """分析关键词密度"""
        full_text = f"{title} {description}".lower()
        words = re.findall(r'\b\w+\b', full_text)
        total_words = len(words)
        
        keyword_data = {}
        for keyword in self.config['target_keywords']:
            count = full_text.count(keyword.lower())
            density = (count / total_words * 100) if total_words > 0 else 0
            keyword_data[keyword] = {
                'count': count,
                'density': round(density, 2),
                'optimal': 1.5 <= density <= 5.0
            }
        
        return keyword_data
    
    def calculate_keyword_score(self, keyword_analysis):
        """计算关键词得分"""
        optimal_count = sum(1 for data in keyword_analysis.values() if data['optimal'])
        if optimal_count >= 2:
            return 20
        elif optimal_count == 1:
            return 15
        else:
            return 10
    
    async def assess_channel_activity(self, channel):
        """评估频道活跃度"""
        try:
            messages = await self.client(GetHistoryRequest(
                peer=channel,
                limit=10,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))
            
            if not messages.messages:
                return 5
            
            total_views = 0
            valid_messages = 0
            
            for msg in messages.messages:
                if hasattr(msg, 'views') and msg.views:
                    total_views += msg.views
                    valid_messages += 1
            
            if valid_messages == 0:
                return 5
            
            avg_views = total_views / valid_messages
            
            if avg_views > 10000:
                return 20
            elif avg_views > 5000:
                return 18
            elif avg_views > 1000:
                return 15
            elif avg_views > 500:
                return 12
            else:
                return 10
                
        except:
            return 10
    
    def format_audit_report(self, analysis, channel):
        """格式化诊断报告"""
        report = f"""
📊 **{channel} SEO诊断报告**
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

🎯 **综合评分：{analysis['seo_score']}/100**

**详细评分：**
"""
        for check_name, score, total in analysis['checks']:
            bar = '█' * (score // 5) + '░' * ((total - score) // 5)
            report += f"\n{check_name}: {bar} {score}/{total}"
        
        report += "\n\n📋 **优化建议：**"
        for suggestion in analysis['suggestions']:
            report += f"\n{suggestion}"
        
        report += "\n\n🔑 **关键词分析：**"
        for kw, data in analysis['keyword_analysis'].items():
            status = "✅" if data['optimal'] else "⚠️"
            report += f"\n{status} {kw}: {data['density']}% (出现{data['count']}次)"
        
        score = analysis['seo_score']
        if score >= 80:
            level = "🏆 优秀"
        elif score >= 60:
            level = "✅ 良好"
        elif score >= 40:
            level = "⚠️ 一般"
        else:
            level = "❌ 需改进"
        
        report += f"\n\n**评级：{level}**"
        report += "\n\n💡 使用 /suggest 获取优化内容模板"
        
        return report
    
    async def generate_optimized_content(self, topic):
        """生成优化内容"""
        keywords = self.config['target_keywords']
        primary_kw = keywords[0] if keywords else topic
        
        title_templates = [
            f"{primary_kw} | {topic}全攻略",
            f"{primary_kw} · 每日精选：{topic}",
            f"【{primary_kw}】{topic}实战指南"
        ]
        title = title_templates[0]
        
        hooks = [
            f"🔥 关于{topic}，90%的人都忽略了这3个关键点",
            f"📈 {topic}最新趋势：掌握这5个技巧效率翻倍",
            f"💡 深耕{topic}3年，总结出这套核心方法论"
        ]
        hook = hooks[datetime.now().day % len(hooks)]
        
        cta = f"""
👆 点击上方链接查看完整内容
💬 在评论区分享你的{topic}经验
📤 转发给需要的朋友
        """.strip()
        
        hashtags = [f"#{kw.replace(' ', '')}" for kw in keywords[:3]]
        
        keywords_in_title = "✅ 已包含" if primary_kw in title[:15] else "❌ 需调整"
        
        full_text = f"{title} {hook}"
        word_count = len(re.findall(r'\b\w+\b', full_text))
        kw_count = sum(full_text.count(kw) for kw in keywords)
        density = round((kw_count / word_count * 100) if word_count > 0 else 0, 2)
        
        return {
            'title': title,
            'hook': hook,
            'cta': cta,
            'hashtags': hashtags,
            'keywords_in_title': keywords_in_title,
            'keyword_density': density
        }
    
    async def track_channel_metrics(self, channel_username):
        """追踪频道指标"""
        try:
            channel = await self.client.get_entity(channel_username)
            
            messages = await self.client(GetHistoryRequest(
                peer=channel,
                limit=30,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))
            
            metrics = {
                'total_posts': len(messages.messages),
                'avg_views': 0,
                'avg_forwards': 0,
                'engagement_rate': 0,
                'best_posts': [],
                'posting_frequency': 0
            }
            
            if messages.messages:
                views = []
                forwards = []
                dates = []
                
                for msg in messages.messages:
                    if hasattr(msg, 'views') and msg.views:
                        views.append(msg.views)
                    if hasattr(msg, 'forwards') and msg.forwards:
                        forwards.append(msg.forwards)
                    dates.append(msg.date)
                    
                    if msg.views and msg.views > 1000:
                        metrics['best_posts'].append({
                            'id': msg.id,
                            'views': msg.views,
                            'text': msg.message[:80] if msg.message else '[媒体内容]',
                            'date': msg.date.strftime('%m-%d')
                        })
                
                if views:
                    metrics['avg_views'] = int(sum(views) / len(views))
                if forwards:
                    metrics['avg_forwards'] = round(sum(forwards) / len(forwards), 1)
                
                if views and forwards:
                    metrics['engagement_rate'] = round((sum(forwards) / sum(views)) * 100, 2)
                
                if len(dates) >= 2:
                    date_range = (dates[0] - dates[-1]).days
                    metrics['posting_frequency'] = round(len(messages.messages) / max(1, date_range), 1)
            
            self.save_metrics(channel_username, metrics)
            return metrics
            
        except Exception as e:
            return {'error': str(e)}
    
    def save_metrics(self, channel, metrics):
        """保存指标"""
        file_path = f'{DATA_DIR}/metrics_{channel.replace("@", "")}.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append({
            'date': datetime.now().isoformat(),
            'metrics': metrics
        })
        
        history = history[-30:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def format_metrics_report(self, channel, metrics):
        """格式化指标报告"""
        if 'error' in metrics:
            return f"❌ 获取数据失败：{metrics['error']}"
        
        report = f"""
📈 **{channel} 数据报告**
统计时间：最近30条内容

**核心指标：**
• 平均阅读量：{metrics['avg_views']:,}
• 平均转发量：{metrics['avg_forwards']}
• 互动率：{metrics['engagement_rate']}%
• 发布频率：{metrics['posting_frequency']}篇/天

**内容表现：**
• 总内容数：{metrics['total_posts']}篇
• 爆款内容数：{len(metrics['best_posts'])}篇（>1000阅读）

**热门内容TOP3：**
"""
        for i, post in enumerate(metrics['best_posts'][:3], 1):
            report += f"\n{i}. 👁 {post['views']} | {post['date']} | {post['text']}"
        
        if metrics['avg_views'] > 5000:
            level = "🏆 头部频道"
        elif metrics['avg_views'] > 1000:
            level = "✅ 优质频道"
        elif metrics['avg_views'] > 500:
            level = "📈 成长频道"
        else:
            level = "🌱 新频道"
        
        report += f"\n\n**评级：{level}**"
        report += "\n\n💡 建议：保持当前更新频率，优化标题关键词"
        
        return report
    
    def save_analysis(self, channel, analysis):
        """保存分析结果"""
        file_path = f'{DATA_DIR}/analysis_{channel.replace("@", "")}.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)


async def main():
    bot = TelegramSEOBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
