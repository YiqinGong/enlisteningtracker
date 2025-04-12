#!/bin/bash

# 这个脚本用来初始化GitHub仓库并推送代码

echo "初始化GitHub仓库..."

# 初始化git仓库
git init

# 添加所有文件
git add .

# 第一次提交
git commit -m "初始化精听记录项目"

echo "请输入您的GitHub用户名:"
read username

echo "请输入您想要创建的仓库名称 (默认: listeningtracker):"
read repo_name
repo_name=${repo_name:-listeningtracker}

echo "正在创建远程仓库链接..."
git remote add origin "https://github.com/$username/$repo_name.git"

echo "准备推送代码到GitHub..."
echo "请在GitHub上先创建一个名为 $repo_name 的空仓库，然后按任意键继续..."
read -n 1

echo "正在推送代码到GitHub..."
git push -u origin master || git push -u origin main

echo "完成!"
echo "您的精听记录仓库已创建并推送到 https://github.com/$username/$repo_name"
echo "现在您可以用以下命令来创建每日记录和更新统计数据:"
echo "- 创建今日记录: python scripts/new_log.py"
echo "- 更新统计数据: python scripts/update_stats.py" 