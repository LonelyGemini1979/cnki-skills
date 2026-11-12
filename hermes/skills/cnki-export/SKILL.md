---
name: cnki-export
description: 中国知网(CNKI)导出引用。将论文导出到Zotero或保存为RIS/GB格式文件。
license: MIT
author: cookjohn (Hermes adaptation)
version: 1.0.0
metadata:
  hermes:
    tags: [cnki, 知网, 中文文献, 学术检索, 浏览器自动化]
    homepage: https://github.com/cookjohn/cnki-skills
    original_skill: cnki-export
---

# cnki-export

中国知网(CNKI)导出引用。将论文导出到Zotero或保存为RIS/GB格式文件。

## 功能说明

本技能从Claude Code版本适配而来，使用Hermes的浏览器工具实现相同功能。

## 使用方法

直接对Hermes说出你的需求，例如：
- "帮我搜索'颈椎病'相关论文"
- "下载这篇论文的PDF"
- "将这篇论文导出到Zotero"

## 技术实现

**使用的Hermes工具：**
- `browser_navigate`
- `browser_click`
- `browser_console`

**原始工具映射：**
- `mcp__chrome-devtools__navigate_page` → `browser_navigate`
- `mcp__chrome-devtools__evaluate_script` → `browser_console`
- `mcp__chrome-devtools__click` → `browser_click`
- `mcp__chrome-devtools__fill` → `browser_type`

## 原始文档


# CNKI Export & Zotero Integration

Export paper citation data from CNKI and push directly to Zotero, or save as RIS file.

## Arguments

- `zotero` (default) — push to Zotero desktop via local API
- `ris` — save as .ris file
- `gb` — output GB/T 7714 citation text
- Optionally include a paper URL

## Mode Selection

Choose the right mode based on context:

| Context | Mode | Tool calls |
|---------|------|-----------|
| On a paper detail page | Single export (Step 1A) | 1 evaluate + 1 bash = **2** |
| On a search results page, save all/selected | **Batch export (Step 1B)** | 1 evaluate + 1 bash = **2** |
| Need to search then save | Use cnki-search first, then batch export | **4 total** |

**Always prefer batch export (1B) when multiple papers need saving.** It avoids navigating to each detail page (saves ~3 calls per paper).

## Steps

### 1A. Single export: from paper detail page

Use `browser_console`:

```javascript
async () => {
  const url = document.querySelector('#export-url')?.value;
  const params = document.querySelector('#export-id')?.value;
  const uniplatform = new URLSearchParams(window.location.search).get('uniplatform') || 'NZKPT';
  if (!url || !params) return { error: 'Not on a paper detail page' };

  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ filename: params, displaymode: 'GBTREFER,elearning,EndNote', uniplatform })
  });
  const data = await resp.json();
  if (data.code !== 1) return { error: data.msg };

  const result = {};
  for (const item of data.data) {
    result[item.mode] = item.value[0];
  }

  const body = document.body.innerText;
  result.pageUrl = window.location.href;
  result.issn = body.match(/ISSN[：:]\s*(\S+)/)?.[1] || '';
  result.dbcode = document.querySelector('#paramdbcode')?.value || '';
  result.dbname = document.querySelector('#paramdbname')?.value || '';
  result.filename = document.querySelector('#paramfilename')?.value || '';

  return result;
}
```

### 1B. Batch export: from search results page (PREFERRED for multiple papers)

On any CNKI search results page, extract checkbox values and call the export API directly — **no need to navigate to detail pages**.

Key discovery: `input.cbItem` checkbox `value` === detail page `#export-id` (same encrypted ID).

Use `browser_console`:

```javascript
async () => {
  const API_URL = 'https://kns.cnki.net/dm8/API/GetExport';

  // Get all checkbox values (= export encrypted IDs)
  const checkboxes = document.querySelectorAll('.result-table-list tbody input.cbItem');
  const rows = document.querySelectorAll('.result-table-list tbody tr');

  if (checkboxes.length === 0) return { error: 'No results on page' };

  const allPapers = [];
  for (let i = 0; i < checkboxes.length; i++) {
    const exportId = checkboxes[i].value;
    const paperUrl = rows[i]?.querySelector('td.name a.fz14')?.href || '';

    const resp = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ filename: exportId, displaymode: 'GBTREFER,elearning,EndNote', uniplatform: 'NZKPT' })
    });
    const data = await resp.json();
    if (data.code === 1) {
      const result = {};
      for (const item of data.data) { result[item.mode] = item.value[0]; }
      result.pageUrl = paperUrl;
      // Extract ISSN from ENDNOTE %@ field
      const issnMatch = result.ENDNOTE?.match(/%@\s*([^\s<]+)/);
      result.issn = issnMatch ? issnMatch[1] : '';
      result.dbcode = 'CJFQ';
      result.dbname = '';
      result.filename = '';
      allPapers.push(result);
    }
  }

  return allPapers; // JSON array, directly writable to file for Python script
}
```

**To export only specific papers** (e.g. #1, #3, #5), filter by index:

```javascript
// Replace the for loop condition:
const indices = [0, 2, 4]; // 0-indexed: papers #1, #3, #5
for (let i = 0; i < checkboxes.length; i++) {
  if (!indices.includes(i)) continue;
  // ... rest same
}
```

### 2. Push to Zotero

Save the export data (single object or JSON array) to a temp file, then run the Python script:

```bash
python "e:/cnki/.claude/skills/cnki-export/scripts/push_to_zotero.py" /tmp/papers.json
```

The Python script handles both single paper `{}` and batch `[{}, {}, ...]` JSON input.

- UTF-8 encoding (avoids Windows encoding issues)
- Parsing ELEARNING format into Zotero item fields
- Calling `POST http://127.0.0.1:23119/connector/saveItems`
- Returns: 201 = success, 500 = error, 0 = Zotero not running

### 3. Report result

Single:
```
已将论文添加到 Zotero:
  标题: {title}
  作者: {authors}
  期刊: {journal}

GB/T 7714 引用: {gbt_citation}
```

Batch:
```
已批量添加 {count} 篇论文到 Zotero:
  1. {title1} ({journal1})
  2. {title2} ({journal2})
  ...
```

## Export API Reference

| Parameter | Value | Source |
|-----------|-------|--------|
| API URL | `https://kns.cnki.net/dm8/API/GetExport` | Fixed, works from any page |
| filename | Encrypted ID | Detail page: `#export-id`; Results page: `input.cbItem` value |
| displaymode | `GBTREFER,elearning,EndNote` | Comma-separated modes |
| uniplatform | `NZKPT` | Required |

## Verified selectors

| Element | Selector | Page |
|---------|----------|------|
| Export URL | `#export-url` | Detail page only |
| Export ID | `#export-id` | Detail page only |
| Checkbox (= export ID) | `input.cbItem` | Search results page |
| Result rows | `.result-table-list tbody tr` | Search results page |
| Title link | `td.name a.fz14` | Search results page |

## Zotero API Reference

```
POST http://127.0.0.1:23119/connector/saveItems
Content-Type: application/json
X-Zotero-Connector-API-Version: 3
```

**Response:** 201 = created, 500 = error
**Collection:** Saves to Zotero's currently selected collection.

Query collections:
```bash
python "e:/cnki/.claude/skills/cnki-export/scripts/push_to_zotero.py" --list
```

## Important Notes

- **Windows encoding:** Must use Python script, cannot pass Chinese JSON via bash/curl directly
- **Zotero must be running:** `localhost:23119` requires Zotero desktop in background
- **Chinese authors:** Use `name` field (single field, not split), `creatorType: "author"`
- **Batch export saves ~90% tool calls:** 9 papers: 33 calls → 3 calls
- **CNKI Export API:** `filename` must be encrypted ID (`#export-id` or `input.cbItem` value), NOT `#paramfilename`


## 注意事项

1. **验证码处理**: 知网使用腾讯滑块验证码，需要手动完成
2. **登录状态**: 某些功能需要知网账号登录
3. **访问频率**: 建议操作间隔3-5秒，避免触发反爬
4. **浏览器**: 确保Hermes浏览器工具已启动

## 参考链接

- 原始技能: https://github.com/cookjohn/cnki-skills/tree/main/skills/cnki-export
- Hermes文档: https://hermes-agent.nousresearch.com/docs
