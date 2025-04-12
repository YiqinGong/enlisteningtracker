#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建新的精听记录脚本

这个脚本会在logs目录下创建一个新的精听记录文件，文件名为当前日期。
"""

import os
import datetime
import shutil
import sys

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
TEMPLATE_PATH = os.path.join(ROOT_DIR, 'templates', 'daily_template.md')

def create_new_log():
    """创建新的精听记录文件"""
    # 确保目录存在
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # 获取当前日期
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 新文件路径
    new_file_path = os.path.join(LOGS_DIR, f'{today}.md')
    
    # 检查文件是否已存在
    if os.path.exists(new_file_path):
        print(f"今天的记录文件已存在: {new_file_path}")
        choice = input("要覆盖它吗? (y/n): ")
        if choice.lower() != 'y':
            print("操作取消")
            return
    
    # 从模板创建新文件
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # 替换模板中的日期
    content = template_content.replace('YYYY-MM-DD', today)
    
    # 写入新文件
    with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已创建今天的精听记录文件: {new_file_path}")
    print(f"填写完成后，请运行 python scripts/update_stats.py 更新统计数据")

if __name__ == "__main__":
    if not os.path.exists(TEMPLATE_PATH):
        print(f"错误: 模板文件不存在: {TEMPLATE_PATH}")
        sys.exit(1)
    
    create_new_log() 