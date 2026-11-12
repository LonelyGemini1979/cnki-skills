---
name: cnki-search
description: |
  中国知网(CNKI)基础检索技能。当用户需要搜索中文论文、中文学术文献时使用。
  触发词：知网、CNKI、中文论文、中文文献、搜索论文、查找文献。
  示例："帮我搜索颈椎病相关论文"、"在知网上查找MRI诊断的文献"。
license: MIT
author: cookjohn (Hermes adaptation)
version: 2.0.0
metadata:
  hermes:
    tags: [cnki, 知网, 中文文献, 学术检索, 浏览器自动化, 中文论文]
    homepage: https://github.com/cookjohn/cnki-skills
    original_skill: cnki-search
    hermes_version: ">=1.0.0"
    required_tools: [browser_navigate, browser_console, browser_click, browser_type]
    estimated_duration: "30-60秒"
    requires_login: false
    requires_captcha: true
---

# CNKI基础检索 (Hermes版)

## 功能

在中国知网(CNKI)上搜索学术论文，返回结构化的检索结果。

**支持：**
- ✅ 关键词检索（中文/英文）
- ✅ 结果解析（标题、作者、期刊、日期、引用、下载）
- ✅ 验证码检测
- ✅ 分页信息
- ⏳ 高级检索（使用 cnki-advanced-search）
- ⏳ 文献下载（使用 cnki-download）

## 使用场景

**触发示例：**
```
用户: 帮我搜索"颈椎病"相关的中文论文
用户: 在知网上查找"人工智能"的文献
用户: 搜索"机器学习"相关研究
用户: CNKI上有什么关于"深度学习"的论文
```

**不触发示例：**
```
用户: 搜索PubMed上的论文 → 使用 pubmed-search
用户: 下载这篇论文 → 使用 cnki-download
用户: 导出到Zotero → 使用 cnki-export
```

## 工作流程

### 步骤1: 打开知网检索页

```
工具: browser_navigate
参数: url="https://kns.cnki.net/kns8s/search"
说明: 打开知网基础检索页面
```

### 步骤2: 执行搜索并提取结果

```
工具: browser_console
参数: code=见下方JavaScript代码
说明: 填充关键词、提交搜索、等待结果、提取数据
```

**JavaScript代码：**
```javascript
async () => {
  const query = "YOUR_KEYWORDS"; // 替换为实际关键词
  
  // 1. 等待搜索框加载
  await new Promise((resolve, reject) => {
    let attempts = 0;
    const check = () => {
      if (document.querySelector('input.search-input')) {
        resolve();
      } else if (++attempts > 30) {
        reject(new Error('搜索框加载超时'));
      } else {
        setTimeout(check, 500);
      }
    };
    check();
  });
  
  // 2. 检查验证码
  const captcha = document.querySelector('#tcaptcha_transform_dy');
  if (captcha && captcha.getBoundingClientRect().top >= 0) {
    return { 
      error: 'captcha', 
      message: '检测到验证码，请手动完成验证后重试' 
    };
  }
  
  // 3. 填充搜索框并提交
  const input = document.querySelector('input.search-input');
  input.value = query;
  input.dispatchEvent(new Event('input', { bubbles: true }));
  
  const searchBtn = document.querySelector('input.search-btn');
  if (searchBtn) {
    searchBtn.click();
  } else {
    return { error: 'no_search_button', message: '找不到搜索按钮' };
  }
  
  // 4. 等待结果加载
  await new Promise((resolve, reject) => {
    let attempts = 0;
    const check = () => {
      if (document.body.innerText.includes('条结果')) {
        resolve();
      } else if (++attempts > 30) {
        reject(new Error('结果加载超时'));
      } else {
        setTimeout(check, 500);
      }
    };
    check();
  });
  
  // 5. 再次检查验证码
  const captcha2 = document.querySelector('#tcaptcha_transform_dy');
  if (captcha2 && captcha2.getBoundingClientRect().top >= 0) {
    return { 
      error: 'captcha', 
      message: '搜索后出现验证码，请手动完成验证' 
    };
  }
  
  // 6. 提取结果
  const rows = document.querySelectorAll('.result-table-list tbody tr');
  const checkboxes = document.querySelectorAll('.result-table-list tbody input.cbItem');
  
  const results = Array.from(rows).map((row, index) => {
    const titleLink = row.querySelector('td.name a.fz14');
    const authors = Array.from(
      row.querySelectorAll('td.author a.KnowledgeNetLink') || []
    ).map(a => a.innerText?.trim()).filter(Boolean);
    
    return {
      index: index + 1,
      title: titleLink?.innerText?.trim() || '',
      url: titleLink?.href || '',
      exportId: checkboxes[index]?.value || '',
      authors: authors.join('; '),
      journal: row.querySelector('td.source a')?.innerText?.trim() || '',
      date: row.querySelector('td.date')?.innerText?.trim() || '',
      citations: row.querySelector('td.quote')?.innerText?.trim() || '0',
      downloads: row.querySelector('td.download')?.innerText?.trim() || '0'
    };
  });
  
  // 7. 提取分页信息
  const totalText = document.querySelector('.pagerTitleCell')?.innerText || '';
  const totalMatch = totalText.match(/([\d,]+)/);
  const total = totalMatch ? totalMatch[1] : '0';
  
  const pageText = document.querySelector('.countPageMark')?.innerText || '1/1';
  
  return {
    success: true,
    query: query,
    total: total,
    page: pageText,
    count: results.length,
    results: results
  };
}
```

### 步骤3: 格式化输出

将结果格式化为易读的列表：

```
在知网搜索"颈椎病"，共找到 12,345 条结果（第 1/300 页）

1. 颈椎病MRI诊断的临床研究
   作者: 张三; 李四
   期刊: 中华骨科杂志 | 日期: 2024-01-15
   引用: 45 | 下载: 1,234

2. 脊髓型颈椎病的手术治疗进展
   作者: 王五; 赵六
   期刊: 中国脊柱脊髓杂志 | 日期: 2023-12-20
   引用: 32 | 下载: 987

...
```

## 错误处理

### 验证码

**检测：**
```javascript
const captcha = document.querySelector('#tcaptcha_transform_dy');
if (captcha && captcha.getBoundingClientRect().top >= 0) {
  // 验证码可见
}
```

**处理：**
```
返回: { error: 'captcha', message: '请手动完成验证' }
操作: 暂停执行，提示用户在浏览器中完成滑块验证
```

### 搜索超时

**处理：**
```
返回: { error: 'timeout', message: '搜索超时，请重试' }
建议: 检查网络连接，或稍后重试
```

### 无结果

**处理：**
```
返回: { success: true, total: '0', results: [] }
建议: 尝试更宽泛的关键词，或使用高级检索
```

## 后续操作

搜索完成后，用户可能需要：

1. **查看详情** → 使用 `cnki-paper-detail` 技能
2. **下载全文** → 使用 `cnki-download` 技能
3. **导出引用** → 使用 `cnki-export` 技能
4. **下一页** → 使用 `cnki-navigate-pages` 技能
5. **精确筛选** → 使用 `cnki-advanced-search` 技能

## 技术细节

### 选择器验证

| 元素 | CSS选择器 | 说明 |
|------|----------|------|
| 搜索框 | `input.search-input` | id=`txt_search` |
| 搜索按钮 | `input.search-btn` | type="button" |
| 结果行 | `.result-table-list tbody tr` | 每行一篇论文 |
| 标题链接 | `td.name a.fz14` | 包含论文URL |
| 作者 | `td.author a.KnowledgeNetLink` | 作者链接 |
| 期刊 | `td.source a` | 期刊名称 |
| 日期 | `td.date` | 发表日期 |
| 引用 | `td.quote` | 被引次数 |
| 下载 | `td.download` | 下载次数 |
| 总数 | `.pagerTitleCell` | "共找到 X 条结果" |
| 页码 | `.countPageMark` | "1/300" |

### 验证码检测原理

知网使用腾讯滑块验证码，SDK会预加载DOM但隐藏在屏幕外：
- 隐藏时: `top: -1000000px`
- 显示时: `top >= 0`

因此检测 `getBoundingClientRect().top >= 0` 可准确判断验证码是否真正显示。

## 注意事项

1. **访问频率**: 建议每次搜索间隔3-5秒，避免触发反爬
2. **验证码**: 频繁搜索会触发验证码，需手动完成
3. **登录状态**: 基础检索无需登录，下载需要登录
4. **结果数量**: 每页默认显示20条结果
5. **超时设置**: 搜索和结果加载超时时间为15秒

## 相关技能

- `cnki-advanced-search`: 高级检索（多字段筛选）
- `cnki-paper-detail`: 获取论文详细信息
- `cnki-download`: 下载论文PDF/CAJ
- `cnki-export`: 导出到Zotero/RIS
- `cnki-navigate-pages`: 翻页和排序

## 更新日志

### v2.0.0 (2026-11-13)
- 完全重写为Hermes风格
- 添加详细的触发示例
- 完善错误处理
- 添加技术细节说明
- 优化JavaScript代码

### v1.0.0 (2026-11-13)
- 初始Hermes适配版本
- 简单替换工具名称

## 参考

- 原始技能: https://github.com/cookjohn/cnki-skills
- 知网帮助: https://help.cnki.net
- Hermes文档: https://hermes-agent.nousresearch.com/docs
