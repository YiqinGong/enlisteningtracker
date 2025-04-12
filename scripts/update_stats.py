#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
精听记录统计脚本

这个脚本自动解析logs目录下的精听记录，
更新stats目录下的统计文件。
"""

import os
import re
import datetime
from collections import defaultdict

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
STATS_DIR = os.path.join(ROOT_DIR, 'stats')

# 忽略的文件
IGNORE_FILES = ['example.md']

def parse_log_file(filepath):
    """解析单个日志文件，提取统计信息"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取日期
    date_match = re.search(r'# 日期: (\d{4}-\d{2}-\d{2})', content)
    date = date_match.group(1) if date_match else None
    
    # 提取标题
    title_match = re.search(r'- 标题: (.*)', content)
    title = title_match.group(1) if title_match else None
    
    # 提取链接
    link_match = re.search(r'- 链接: (.*)', content)
    link = link_match.group(1) if link_match else None
    
    # 提取时长
    duration_match = re.search(r'- 时长: (.*)', content)
    duration_str = duration_match.group(1) if duration_match else None
    
    # 转换时长为分钟
    duration_minutes = 0
    if duration_str:
        if ':' in duration_str:
            parts = duration_str.split(':')
            if len(parts) == 2:
                duration_minutes = int(parts[0]) * 1 + float(parts[1]) / 60
            elif len(parts) == 3:
                duration_minutes = int(parts[0]) * 60 + int(parts[1]) + float(parts[2]) / 60
        else:
            try:
                duration_minutes = float(duration_str)
            except:
                pass
    
    # 提取难度
    difficulty_match = re.search(r'- 难度: (.*)', content)
    difficulty = difficulty_match.group(1) if difficulty_match else None
    
    # 提取练习时间
    time_spent_match = re.search(r'- 总用时：(\d+)分钟', content)
    time_spent = int(time_spent_match.group(1)) if time_spent_match else 0
    
    # 提取重复次数
    repeats_match = re.search(r'- 重复次数：(\d+)', content)
    repeats = int(repeats_match.group(1)) if repeats_match else 0
    
    # 提取生词数量
    vocab_count = len(re.findall(r'\| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \|', content)) - 1  # 减去表头
    vocab_count = max(0, vocab_count)  # 确保不是负数
    
    return {
        'date': date,
        'title': title,
        'link': link,
        'duration': duration_minutes,
        'difficulty': difficulty,
        'time_spent': time_spent,
        'repeats': repeats,
        'vocab_count': vocab_count,
        'filename': os.path.basename(filepath)
    }

def update_daily_stats(logs_data):
    """更新每日统计数据"""
    daily_stats_path = os.path.join(STATS_DIR, 'daily.md')
    
    # 表头
    header = """# 每日精听统计

| 日期 | 视频标题 | 时长(分钟) | 精听用时(分钟) | 难度 | 生词数量 | 重复次数 | 链接 |
|-----|---------|-----------|--------------|-----|---------|---------|-----|"""
    
    # 按日期排序
    sorted_logs = sorted(logs_data, key=lambda x: x['date'] if x['date'] else '')
    
    # 生成行
    rows = []
    for log in sorted_logs:
        if not log['date']:
            continue
        
        row = f"| {log['date']} | {log['title'] or ''} | {log['duration']:.1f} | {log['time_spent']} | {log['difficulty'] or ''} | {log['vocab_count']} | {log['repeats']} | {log['link'] or ''} |"
        rows.append(row)
    
    # 写入文件
    with open(daily_stats_path, 'w', encoding='utf-8') as f:
        f.write(header + '\n')
        f.write('\n'.join(rows))

def update_weekly_stats(logs_data):
    """更新每周统计数据"""
    weekly_stats_path = os.path.join(STATS_DIR, 'weekly.md')
    
    # 按日期排序
    sorted_logs = sorted([log for log in logs_data if log['date']], 
                        key=lambda x: x['date'])
    
    if not sorted_logs:
        return
    
    # 计算周数据
    weeks = defaultdict(list)
    for log in sorted_logs:
        date = datetime.datetime.strptime(log['date'], '%Y-%m-%d')
        # 确定这一天是哪一周
        year, week_num, _ = date.isocalendar()
        week_key = f"{year}-W{week_num:02d}"
        weeks[week_key].append(log)
    
    # 计算每周的开始和结束日期
    week_dates = {}
    for week_key, logs in weeks.items():
        dates = [log['date'] for log in logs]
        week_dates[week_key] = (min(dates), max(dates))
    
    # 生成内容
    content = ["# 每周精听统计\n"]
    
    for i, (week_key, logs) in enumerate(sorted(weeks.items())):
        start_date, end_date = week_dates[week_key]
        
        # 计算统计
        completed = len(logs)
        total_time = sum(log['time_spent'] for log in logs)
        total_vocab = sum(log['vocab_count'] for log in logs)
        avg_daily = total_time / 7 if total_time else 0
        completion_rate = completed / 7 * 100  # 假设每周7天
        
        # 写入周信息
        content.append(f"## 第{i+1}周 ({start_date} 至 {end_date})\n")
        content.append(f"- 完成视频数: {completed}")
        content.append(f"- 总精听时长: {total_time}分钟")
        content.append(f"- 学习生词数: {total_vocab}")
        content.append(f"- 平均每日学习时间: {avg_daily:.1f}分钟")
        content.append(f"- 完成率: {completion_rate:.1f}%\n")
        
        # 本周视频列表
        content.append("### 本周视频列表\n")
        content.append("| 日期 | 视频标题 | 时长(分钟) |")
        content.append("|-----|---------|-----------|")
        
        for log in sorted(logs, key=lambda x: x['date']):
            content.append(f"| {log['date']} | {log['title'] or ''} | {log['duration']:.1f} |")
        
        content.append("\n---\n")
    
    # 写入文件
    with open(weekly_stats_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def update_summary_stats(logs_data):
    """更新总体统计数据"""
    summary_path = os.path.join(STATS_DIR, 'summary.md')
    
    # 过滤并按日期排序
    valid_logs = [log for log in logs_data if log['date']]
    sorted_logs = sorted(valid_logs, key=lambda x: x['date'])
    
    if not sorted_logs:
        return
    
    # 总体统计
    start_date = sorted_logs[0]['date']
    days_count = (datetime.datetime.strptime(sorted_logs[-1]['date'], '%Y-%m-%d') - 
                 datetime.datetime.strptime(start_date, '%Y-%m-%d')).days + 1
    total_videos = len(sorted_logs)
    total_hours = sum(log['time_spent'] for log in sorted_logs) / 60
    total_vocab = sum(log['vocab_count'] for log in sorted_logs)
    avg_daily = sum(log['time_spent'] for log in sorted_logs) / days_count if days_count else 0
    
    # 月度统计
    months = defaultdict(list)
    for log in sorted_logs:
        month = log['date'][:7]  # YYYY-MM
        months[month].append(log)
    
    # 难度分布
    difficulty_count = defaultdict(int)
    for log in sorted_logs:
        if log['difficulty']:
            difficulty_count[log['difficulty']] += 1
    
    # 生成内容
    content = [
        "# 精听累计统计\n",
        "## 总体进度\n",
        f"- 开始日期: {start_date}",
        f"- 已进行天数: {days_count}",
        f"- 累计精听视频: {total_videos}个",
        f"- 累计精听时长: {total_hours:.1f}小时",
        f"- 累计学习生词: {total_vocab}个",
        f"- 平均每日学习时间: {avg_daily:.1f}分钟\n",
        "## 月度统计\n",
        "| 月份 | 完成视频数 | 精听总时长(小时) | 学习生词数 | 完成率 |",
        "|-----|-----------|----------------|----------|-------|"
    ]
    
    for month, logs in sorted(months.items()):
        month_videos = len(logs)
        month_hours = sum(log['time_spent'] for log in logs) / 60
        month_vocab = sum(log['vocab_count'] for log in logs)
        
        # 计算当月天数
        year, month_num = map(int, month.split('-'))
        days_in_month = 30  # 简化处理
        completion_rate = month_videos / days_in_month * 100
        
        content.append(f"| {month} | {month_videos} | {month_hours:.1f} | {month_vocab} | {completion_rate:.1f}% |")
    
    # 进度图表
    content.append("\n## 进度图表\n")
    content.append("```")
    
    for i, (month, logs) in enumerate(sorted(months.items())):
        month_videos = len(logs)
        year, month_num = map(int, month.split('-'))
        days_in_month = 30  # 简化处理
        completion_rate = month_videos / days_in_month
        
        bar = '█' * int(completion_rate * 10)
        bar = bar.ljust(10, ' ')
        
        content.append(f"Month {i+1}: [{bar}] {completion_rate*100:.1f}%")
    
    content.append("```\n")
    
    # 难度分布
    total_with_difficulty = sum(difficulty_count.values())
    
    content.append("## 难度分布\n")
    for difficulty, count in difficulty_count.items():
        percentage = count / total_with_difficulty * 100 if total_with_difficulty else 0
        content.append(f"- {difficulty}: {count} ({percentage:.1f}%)")
    
    # 写入文件
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def main():
    """主函数"""
    # 确保目录存在
    os.makedirs(STATS_DIR, exist_ok=True)
    
    # 获取所有日志文件
    log_files = []
    for filename in os.listdir(LOGS_DIR):
        if filename.endswith('.md') and filename not in IGNORE_FILES:
            log_files.append(os.path.join(LOGS_DIR, filename))
    
    # 解析所有日志
    logs_data = []
    for filepath in log_files:
        log_data = parse_log_file(filepath)
        logs_data.append(log_data)
    
    # 更新各种统计
    update_daily_stats(logs_data)
    update_weekly_stats(logs_data)
    update_summary_stats(logs_data)
    
    print(f"已更新统计数据, 共处理 {len(logs_data)} 个精听记录")

if __name__ == "__main__":
    main() 