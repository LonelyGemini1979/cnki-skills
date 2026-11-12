# CNKI Skills for Hermes Agent

中国知网(CNKI)完整技能套件 - Hermes Agent适配版本

## 📦 包含技能 (10个)

| 技能 | 功能 | 说明 |
|------|------|------|
| cnki-search | 基础检索 | 关键词搜索论文 |
| cnki-advanced-search | 高级检索 | 多字段组合检索 |
| cnki-download | 文献下载 | PDF/CAJ下载 |
| cnki-export | 导出引用 | Zotero/RIS导出 |
| cnki-journal-index | 收录查询 | 期刊收录情况 |
| cnki-journal-search | 期刊检索 | 期刊搜索 |
| cnki-journal-toc | 目录浏览 | 期刊目录查看 |
| cnki-navigate-pages | 翻页排序 | 结果翻页和排序 |
| cnki-paper-detail | 详情提取 | 论文完整信息 |
| cnki-parse-results | 结果解析 | 搜索结果结构化 |

## 🚀 快速安装

```bash
# 一键安装所有技能
cd hermes
./install.sh
```

或手动安装：

```bash
# 复制所有技能到Hermes
cp -r hermes/skills/* ~/.hermes/skills/research/
```

## 📖 使用方法

### 基础检索
```
你: 帮我搜索"颈椎病"相关的中文论文
Hermes: [自动使用cnki-search技能]
```

### 高级检索
```
你: 搜索2020-2024年张三发表的颈椎病论文，限北大核心期刊
Hermes: [自动使用cnki-advanced-search技能]
```

### 下载文献
```
你: 下载这篇论文的PDF
Hermes: [自动使用cnki-download技能]
```

### 导出引用
```
你: 将这篇论文导出到Zotero
Hermes: [自动使用cnki-export技能]
```

### 期刊查询
```
你: 《中华骨科杂志》是北大核心吗？
Hermes: [自动使用cnki-journal-index技能]
```

## 🔧 技术架构

### 原版 (Claude Code)
- 使用 Chrome DevTools MCP
- 需要安装 MCP 服务器
- 通过 `claude mcp` 命令管理

### Hermes版
- 使用 Hermes browser 工具
- 无需额外依赖
- 自然语言直接调用

## 📁 目录结构

```
hermes/
├── README.md                 # 本文件
├── install.sh               # 一键安装脚本
├── skills/                  # 所有技能
│   ├── cnki-search/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   ├── cnki-advanced-search/
│   ├── cnki-download/
│   └── ...
└── docs/                    # 文档
    ├── installation.md      # 安装指南
    ├── usage.md            # 使用说明
    └── troubleshooting.md  # 故障排除
```

## ⚠️ 注意事项

1. **验证码**: 知网使用腾讯滑块，需手动完成
2. **登录**: 下载全文需要知网账号
3. **频率**: 建议操作间隔3-5秒
4. **权限**: 部分论文需要机构订阅

## 🔗 相关链接

- 原始项目: https://github.com/cookjohn/cnki-skills
- Hermes Agent: https://github.com/NousResearch/hermes-agent
- 知网官网: https://www.cnki.net

## 📝 更新日志

### v1.0.0 (2026-11-13)
- 完整适配所有10个技能
- 添加一键安装脚本
- 完善文档和示例
