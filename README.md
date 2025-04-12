# 精听练习记录

这个仓库用于记录我的英语精听练习。我会每天精听一个YouTube视频，记录视频信息、字幕内容以及我的学习笔记。

## 项目结构

- `logs/`: 按日期组织的精听记录
- `stats/`: 统计数据和汇总表格
- `templates/`: 记录模板
- `website/`: 网页界面

## 统计数据

- [每日记录统计](stats/daily.md)
- [每周记录统计](stats/weekly.md)
- [累计统计](stats/summary.md)

## 如何使用

### 在GitHub网页上操作（推荐）

本项目支持完全在网页上操作，无需下载任何文件到本地：

1. 访问项目的GitHub Pages页面：`https://用户名.github.io/enlisteningtracker/`
   - 例如：https://yiqingong.github.io/enlisteningtracker/
   - 注意：请确保使用正确的格式，用户名和仓库名之间是斜杠(/)而不是点(.)
2. 在"创建记录"选项卡中填写精听内容
3. 点击"预览"按钮查看Markdown格式
4. 点击"提交到GitHub"按钮（需要GitHub授权）

### 自动化功能

本项目配置了多个GitHub Actions工作流，实现以下自动化功能：

1. **自动创建每日记录**：每天自动创建当日的精听记录模板
2. **自动更新统计**：当添加新的记录时，自动更新统计数据
3. **自动部署网页**：当代码变更时，自动部署GitHub Pages

### 在本地操作（可选）

1. **创建每日精听记录**：
   ```
   python scripts/new_log.py
   ```
   这将在logs目录下创建一个以当前日期命名的记录文件

2. **更新统计数据**：
   ```
   python scripts/update_stats.py
   ```

## 目标

通过持续精听练习提高英语听力能力，积累地道表达和词汇。

## 获取YouTube字幕

由于技术限制，在GitHub网页上不能直接获取YouTube字幕，以下是几种获取字幕的方法：

1. 使用[DownSub](https://downsub.com/)等第三方网站下载字幕
2. 在YouTube视频下方找到"显示文字记录"按钮，复制字幕
3. 使用浏览器扩展程序获取字幕

## 常见问题

### 网页访问404错误

如果访问GitHub Pages时出现404错误，请检查：

1. 确保URL格式正确：`https://用户名.github.io/enlisteningtracker/`
2. 确保仓库设置中已启用GitHub Pages功能（设置->Pages）
3. 确保工作流有权限部署Pages（设置->Actions->General->Workflow permissions）
4. 查看Actions标签页中部署工作流是否成功运行 