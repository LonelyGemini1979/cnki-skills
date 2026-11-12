---
name: cnki-parse-results
description: 中国知网(CNKI)搜索结果解析。将当前搜索结果页面解析为结构化数据（标题、作者、期刊、日期、引用等）。
license: MIT
author: cookjohn (Hermes adaptation)
version: 1.0.0
metadata:
  hermes:
    tags: [cnki, 知网, 中文文献, 学术检索, 浏览器自动化]
    homepage: https://github.com/cookjohn/cnki-skills
    original_skill: cnki-parse-results
---

# cnki-parse-results

中国知网(CNKI)搜索结果解析。将当前搜索结果页面解析为结构化数据（标题、作者、期刊、日期、引用等）。

## 功能说明

本技能从Claude Code版本适配而来，使用Hermes的浏览器工具实现相同功能。

## 使用方法

直接对Hermes说出你的需求，例如：
- "帮我搜索'颈椎病'相关论文"
- "下载这篇论文的PDF"
- "将这篇论文导出到Zotero"

## 技术实现

**使用的Hermes工具：**
- `browser_console`

**原始工具映射：**
- `mcp__chrome-devtools__navigate_page` → `browser_navigate`
- `mcp__chrome-devtools__evaluate_script` → `browser_console`
- `mcp__chrome-devtools__click` → `browser_click`
- `mcp__chrome-devtools__fill` → `browser_type`

## 原始文档


# CNKI Parse Search Results

Extract structured paper data from the current CNKI search results page.

## Prerequisites

The current Chrome page must be a CNKI search results page (URL contains `kns.cnki.net` and page shows "条结果").

## Steps

### 1. Verify we are on a results page

Use `mcp__chrome-devtools__take_snapshot`. Verify the page contains "条结果". If not, inform the user that no search results page is currently open.

Check for captcha ("拖动下方拼图完成验证") - if found, notify user to solve it manually.

### 2. Extract results via JavaScript

Use `browser_console` with this function:

```javascript
() => {
  const rows = document.querySelectorAll('.result-table-list tbody tr');
  const checkboxes = document.querySelectorAll('.result-table-list tbody input.cbItem');
  const results = Array.from(rows).map((row, index) => {
    const nameCell = row.querySelector('td.name');
    const titleLink = nameCell?.querySelector('a.fz14');
    const authorCell = row.querySelector('td.author');
    const sourceCell = row.querySelector('td.source');
    const dateCell = row.querySelector('td.date');
    const dataCell = row.querySelector('td.data');
    const quoteCell = row.querySelector('td.quote');
    const downloadCell = row.querySelector('td.download');
    const isOnlineFirst = !!nameCell?.querySelector('.marktip');

    return {
      number: index + 1,
      title: titleLink?.innerText?.trim() || '',
      url: titleLink?.href || '',
      exportId: checkboxes[index]?.value || '',
      authors: Array.from(authorCell?.querySelectorAll('a.KnowledgeNetLink') || []).map(a => a.innerText?.trim()),
      journal: sourceCell?.querySelector('a')?.innerText?.trim() || '',
      date: dateCell?.innerText?.trim() || '',
      database: dataCell?.innerText?.trim() || '',
      citations: quoteCell?.innerText?.trim() || '',
      downloads: downloadCell?.innerText?.trim() || '',
      isOnlineFirst: isOnlineFirst
    };
  });

  const totalText = document.querySelector('.pagerTitleCell')?.innerText || '';
  const totalMatch = totalText.match(/([\d,]+)/);
  const pageInfo = document.querySelector('.countPageMark')?.innerText || '';

  return {
    papers: results,
    totalCount: totalMatch ? totalMatch[1] : 'unknown',
    pageInfo: pageInfo
  };
}
```

### 3. Present results

Format as a numbered list:

```
CNKI search results ({totalCount} total, page {pageInfo}):

1. {title} {isOnlineFirst ? "[网络首发]" : ""}
   Authors: {authors joined by "; "}
   Journal: {journal} | Date: {date} | Type: {database}
   Citations: {citations} | Downloads: {downloads}
   URL: {url}

2. ...
```

### 4. Fallback: snapshot-based parsing

If JavaScript returns empty (DOM structure changed), use `mcp__chrome-devtools__take_snapshot` and parse the accessibility tree manually:

Look for the repeating pattern:
- `checkbox` → `StaticText` (number) → `link` with URL containing `kcms2/article/abstract` (title) → `link`s with URL containing `kcms2/author/detail` (authors) → `link` with URL containing `navi.cnki.net/knavi/detail` (journal) → `StaticText` (date) → `StaticText` (database type)

## Verified DOM Selectors (CNKI uses jQuery, stable semantic class names)

| Data       | Selector                         | Notes                      |
|------------|----------------------------------|----------------------------|
| Table      | `.result-table-list tbody tr`    | Each row = one paper       |
| Checkbox   | `input.cbItem`                   | value = export encrypted ID |
| Number     | `td.seq`                         | Row sequence number        |
| Title      | `td.name a.fz14`                 | Paper title link           |
| Authors    | `td.author a.KnowledgeNetLink`   | Author name links          |
| Journal    | `td.source a`                    | Journal/source link        |
| Date       | `td.date`                        | Publication date text      |
| DB Type    | `td.data`                        | Database type (期刊/学位论文) |
| Citations  | `td.quote`                       | Citation count             |
| Downloads  | `td.download`                    | Download count             |
| Online 1st | `td.name .marktip`               | "网络首发" label            |
| Total      | `.pagerTitleCell`                 | "共找到 X 条结果"           |
| Page       | `.countPageMark`                  | "1/300" format             |


## 注意事项

1. **验证码处理**: 知网使用腾讯滑块验证码，需要手动完成
2. **登录状态**: 某些功能需要知网账号登录
3. **访问频率**: 建议操作间隔3-5秒，避免触发反爬
4. **浏览器**: 确保Hermes浏览器工具已启动

## 参考链接

- 原始技能: https://github.com/cookjohn/cnki-skills/tree/main/skills/cnki-parse-results
- Hermes文档: https://hermes-agent.nousresearch.com/docs
