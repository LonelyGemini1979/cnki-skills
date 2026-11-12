---
name: cnki-journal-toc
description: |
  中国知网(CNKI)CNKI期刊目录浏览技能。
  浏览期刊各期目录，查看论文列表，下载原版目录PDF
  触发词：期刊目录, 浏览期刊, 查看目录。
license: MIT
author: cookjohn (Hermes adaptation)
version: 2.0.0
metadata:
  hermes:
    tags: [cnki, 知网, 中文文献, 学术检索]
    homepage: https://github.com/cookjohn/cnki-skills
    original_skill: cnki-journal-toc
    hermes_version: ">=1.0.0"
    required_tools: [browser_navigate, browser_click, browser_console]
    estimated_duration: "30-60秒"
---

# CNKI期刊目录浏览 (Hermes版)

## 功能

浏览期刊各期目录，查看论文列表，下载原版目录PDF

## 使用场景

**触发示例：**
```
用户: 查看《中华骨科杂志》2024年第1期目录
用户: 下载期刊原版目录
用户: 浏览最新一期论文
```

**触发词：**
  - "期刊目录"
  - "浏览期刊"
  - "查看目录"

## 工作流程

### 步骤1: 确保在正确页面

```
工具: browser_console
参数: code="return window.location.href"
说明: 检查当前页面URL
```

### 步骤2: 执行操作

```
工具: browser_console
参数: code=见下方JavaScript代码
```

## 技术实现

**使用的Hermes工具：**
- `browser_navigate`
- `browser_click`
- `browser_console`

## 注意事项

1. **验证码**: 知网使用腾讯滑块验证码，需要手动完成
2. **登录状态**: 某些功能需要知网账号登录
3. **访问频率**: 建议操作间隔3-5秒，避免触发反爬
4. **浏览器**: 确保Hermes浏览器工具已启动

## 相关技能

- `cnki-search`: 基础检索
- `cnki-advanced-search`: 高级检索
- `cnki-download`: 下载文献
- `cnki-export`: 导出引用

## 更新日志

### v2.0.0 (2026-11-13)
- 完全重写为Hermes风格
- 添加详细的触发示例
- 完善错误处理

## 参考

- 原始技能: https://github.com/cookjohn/cnki-skills/tree/main/skills/cnki-journal-toc
- Hermes文档: https://hermes-agent.nousresearch.com/docs
