# CNKI Skills for Hermes Agent

这是cookjohn/cnki-skills的Hermes Agent适配版本。

## 安装方法

```bash
# 复制到Hermes skills目录
cp -r hermes/skills/cnki-search ~/.hermes/skills/research/
```

## 与Claude Code版本的区别

- 使用Hermes browser工具替代Chrome DevTools MCP
- 无需安装Chrome DevTools MCP服务器
- 直接使用Hermes的浏览器自动化功能
- 支持自然语言交互

## 使用方法

安装后，直接对Hermes说：
- "帮我搜索'颈椎病'相关的中文论文"
- "在知网上查找'MRI诊断'的文献"
- "下载这篇论文的PDF"

## 文件结构

```
hermes/
└── skills/
    └── cnki-search/
        ├── SKILL.md              # 技能定义
        ├── scripts/
        │   └── cnki_search.py    # 搜索解析脚本
        └── references/
            ├── usage-guide.md    # 使用指南
            └── quick-reference.md # 快速参考
```

## 原始项目

- 原始仓库: https://github.com/cookjohn/cnki-skills
- Hermes Agent: https://github.com/NousResearch/hermes-agent
