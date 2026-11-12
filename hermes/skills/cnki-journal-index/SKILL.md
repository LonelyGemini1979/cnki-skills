---
name: cnki-journal-index
description: |
  中国知网(CNKI)CNKI期刊收录查询技能。
  查询期刊被哪些数据库收录（北大核心、CSSCI、SCI等）
  触发词：期刊收录, 是否核心, 影响因子。
license: MIT
author: cookjohn (Hermes adaptation)
version: 2.0.0
metadata:
  hermes:
    tags: [cnki, 知网, 中文文献, 学术检索]
    homepage: https://github.com/cookjohn/cnki-skills
    original_skill: cnki-journal-index
    hermes_version: ">=1.0.0"
    required_tools: [browser_navigate, browser_console]
    estimated_duration: "30-60秒"
---

# CNKI期刊收录查询 (Hermes版)

## 功能

查询期刊被哪些数据库收录（北大核心、CSSCI、SCI等）

## 使用场景

**触发示例：**
```
用户: 《中华骨科杂志》是北大核心吗？
用户: 这个期刊的影响因子是多少？
用户: 查询期刊收录情况
```

**触发词：**
  - "期刊收录"
  - "是否核心"
  - "影响因子"
  - "期刊级别"

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

- 原始技能: https://github.com/cookjohn/cnki-skills/tree/main/skills/cnki-journal-index
- Hermes文档: https://hermes-agent.nousresearch.com/docs
