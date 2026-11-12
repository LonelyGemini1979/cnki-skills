#!/usr/bin/env python3
"""
将Claude Code的CNKI skills转换为Hermes格式
"""

import os
import re
from pathlib import Path

# 技能映射表
SKILLS_MAP = {
    'cnki-search': {
        'name': 'cnki-search',
        'description': '中国知网(CNKI)基础检索。使用关键词搜索学术论文，返回标题、作者、期刊、日期等结构化结果。',
        'tools': ['browser_navigate', 'browser_type', 'browser_click', 'browser_console'],
        'url': 'https://kns.cnki.net/kns8s/search'
    },
    'cnki-advanced-search': {
        'name': 'cnki-advanced-search',
        'description': '中国知网(CNKI)高级检索。支持多字段组合检索（作者、标题、期刊、日期范围、来源类别等），适用于精确筛选。',
        'tools': ['browser_navigate', 'browser_type', 'browser_click', 'browser_console'],
        'url': 'https://kns.cnki.net/kns8s/AdvSearch'
    },
    'cnki-download': {
        'name': 'cnki-download',
        'description': '中国知网(CNKI)文献下载。下载论文PDF或CAJ格式全文，需要知网账号登录。',
        'tools': ['browser_navigate', 'browser_click', 'browser_console'],
        'url': None
    },
    'cnki-export': {
        'name': 'cnki-export',
        'description': '中国知网(CNKI)导出引用。将论文导出到Zotero或保存为RIS/GB格式文件。',
        'tools': ['browser_navigate', 'browser_click', 'browser_console'],
        'url': None
    },
    'cnki-journal-index': {
        'name': 'cnki-journal-index',
        'description': '中国知网(CNKI)期刊收录查询。查询期刊被哪些数据库收录（北大核心、CSSCI、CSCD、SCI、EI等），获取影响因子。',
        'tools': ['browser_navigate', 'browser_console'],
        'url': None
    },
    'cnki-journal-search': {
        'name': 'cnki-journal-search',
        'description': '中国知网(CNKI)期刊检索。按期刊名称、ISSN、CN号或主办单位搜索期刊。',
        'tools': ['browser_navigate', 'browser_type', 'browser_click', 'browser_console'],
        'url': 'https://navi.cnki.net/knavi/journals/index'
    },
    'cnki-journal-toc': {
        'name': 'cnki-journal-toc',
        'description': '中国知网(CNKI)期刊目录浏览。浏览期刊各期目录，查看论文列表，下载原版目录PDF。',
        'tools': ['browser_navigate', 'browser_click', 'browser_console'],
        'url': None
    },
    'cnki-navigate-pages': {
        'name': 'cnki-navigate-pages',
        'description': '中国知网(CNKI)结果翻页和排序。导航搜索结果页面（下一页、上一页、指定页），更改排序方式。',
        'tools': ['browser_click', 'browser_console'],
        'url': None
    },
    'cnki-paper-detail': {
        'name': 'cnki-paper-detail',
        'description': '中国知网(CNKI)论文详情提取。提取论文完整信息，包括标题、作者、机构、摘要、关键词、基金、分类号等。',
        'tools': ['browser_navigate', 'browser_console'],
        'url': None
    },
    'cnki-parse-results': {
        'name': 'cnki-parse-results',
        'description': '中国知网(CNKI)搜索结果解析。将当前搜索结果页面解析为结构化数据（标题、作者、期刊、日期、引用等）。',
        'tools': ['browser_console'],
        'url': None
    }
}

def convert_skill(skill_name, skill_info):
    """转换单个skill为Hermes格式"""
    
    # 读取原始SKILL.md
    original_path = Path(f"../skills/{skill_name}/SKILL.md")
    if not original_path.exists():
        print(f"跳过 {skill_name}: 文件不存在")
        return
    
    original_content = original_path.read_text(encoding='utf-8')
    
    # 提取原始内容（去除frontmatter）
    content_match = re.search(r'---\n.*?\n---\n(.*)', original_content, re.DOTALL)
    if content_match:
        original_body = content_match.group(1)
    else:
        original_body = original_content
    
    # 转换工具调用
    converted_body = original_body
    converted_body = converted_body.replace('mcp__chrome-devtools__navigate_page', 'browser_navigate')
    converted_body = converted_body.replace('mcp__chrome-devtools__evaluate_script', 'browser_console')
    converted_body = converted_body.replace('mcp__chrome-devtools__click', 'browser_click')
    converted_body = converted_body.replace('mcp__chrome-devtools__fill', 'browser_type')
    converted_body = converted_body.replace('mcp__chrome-devtools__snapshot', 'browser_snapshot')
    
    # 创建Hermes格式的SKILL.md
    hermes_content = f"""---
name: {skill_info['name']}
description: {skill_info['description']}
license: MIT
author: cookjohn (Hermes adaptation)
version: 1.0.0
metadata:
  hermes:
    tags: [cnki, 知网, 中文文献, 学术检索, 浏览器自动化]
    homepage: https://github.com/cookjohn/cnki-skills
    original_skill: {skill_name}
---

# {skill_info['name']}

{skill_info['description']}

## 功能说明

本技能从Claude Code版本适配而来，使用Hermes的浏览器工具实现相同功能。

## 使用方法

直接对Hermes说出你的需求，例如：
- "帮我搜索'颈椎病'相关论文"
- "下载这篇论文的PDF"
- "将这篇论文导出到Zotero"

## 技术实现

**使用的Hermes工具：**
{chr(10).join(f'- `{tool}`' for tool in skill_info['tools'])}

**原始工具映射：**
- `mcp__chrome-devtools__navigate_page` → `browser_navigate`
- `mcp__chrome-devtools__evaluate_script` → `browser_console`
- `mcp__chrome-devtools__click` → `browser_click`
- `mcp__chrome-devtools__fill` → `browser_type`

## 原始文档

{converted_body}

## 注意事项

1. **验证码处理**: 知网使用腾讯滑块验证码，需要手动完成
2. **登录状态**: 某些功能需要知网账号登录
3. **访问频率**: 建议操作间隔3-5秒，避免触发反爬
4. **浏览器**: 确保Hermes浏览器工具已启动

## 参考链接

- 原始技能: https://github.com/cookjohn/cnki-skills/tree/main/skills/{skill_name}
- Hermes文档: https://hermes-agent.nousresearch.com/docs
"""
    
    # 写入Hermes版本
    output_path = Path(f'hermes/skills/{skill_name}/SKILL.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(hermes_content, encoding='utf-8')
    
    print(f"✅ 转换完成: {skill_name}")

def main():
    """主函数"""
    print("开始转换CNKI skills为Hermes格式...")
    print()
    
    for skill_name, skill_info in SKILLS_MAP.items():
        convert_skill(skill_name, skill_info)
    
    print()
    print("✅ 所有技能转换完成！")
    print(f"输出目录: hermes/skills/")

if __name__ == '__main__':
    main()
