---
name: cnki-navigate-pages
description: 中国知网(CNKI)结果翻页和排序。导航搜索结果页面（下一页、上一页、指定页），更改排序方式。
license: MIT
author: cookjohn (Hermes adaptation)
version: 1.0.0
metadata:
  hermes:
    tags: [cnki, 知网, 中文文献, 学术检索, 浏览器自动化]
    homepage: https://github.com/cookjohn/cnki-skills
    original_skill: cnki-navigate-pages
---

# cnki-navigate-pages

中国知网(CNKI)结果翻页和排序。导航搜索结果页面（下一页、上一页、指定页），更改排序方式。

## 功能说明

本技能从Claude Code版本适配而来，使用Hermes的浏览器工具实现相同功能。

## 使用方法

直接对Hermes说出你的需求，例如：
- "帮我搜索'颈椎病'相关论文"
- "下载这篇论文的PDF"
- "将这篇论文导出到Zotero"

## 技术实现

**使用的Hermes工具：**
- `browser_click`
- `browser_console`

**原始工具映射：**
- `mcp__chrome-devtools__navigate_page` → `browser_navigate`
- `mcp__chrome-devtools__evaluate_script` → `browser_console`
- `mcp__chrome-devtools__click` → `browser_click`
- `mcp__chrome-devtools__fill` → `browser_type`

## 原始文档


# CNKI Results Pagination and Sorting

All operations use a single async `evaluate_script` — no snapshot or wait_for needed.

## Arguments

`$ARGUMENTS` should be one of:
- `next` / `previous` / `page N` — pagination
- `sort by date` / `sort by citations` / `sort by downloads` / `sort by relevance` / `sort by comprehensive` — sorting

## Pagination (single evaluate_script)

Replace `ACTION_HERE` with `"next"`, `"previous"`, or `"page 3"`:

```javascript
async () => {
  const cap = document.querySelector('#tcaptcha_transform_dy');
  if (cap && cap.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  const action = "ACTION_HERE";
  const pageLinks = document.querySelectorAll('.pages a');
  const prevMark = document.querySelector('.countPageMark')?.innerText;

  if (action === 'next') {
    const next = Array.from(pageLinks).find(a => a.innerText.trim() === '下一页');
    if (!next) return { error: 'no_next_page' };
    next.click();
  } else if (action === 'previous') {
    const prev = Array.from(pageLinks).find(a => a.innerText.trim() === '上一页');
    if (!prev) return { error: 'no_previous_page' };
    prev.click();
  } else {
    const num = action.replace(/\D/g, '');
    const target = Array.from(pageLinks).find(a => a.innerText.trim() === num);
    if (!target) return { error: 'page_not_found', available: Array.from(pageLinks).map(a => a.innerText.trim()) };
    target.click();
  }

  // Wait for page change
  await new Promise((r, j) => {
    let n = 0;
    const c = () => {
      const mark = document.querySelector('.countPageMark')?.innerText;
      if (mark && mark !== prevMark) r();
      else if (++n > 30) j('timeout');
      else setTimeout(c, 500);
    };
    setTimeout(c, 1000);
  });

  const cap2 = document.querySelector('#tcaptcha_transform_dy');
  if (cap2 && cap2.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  return {
    action,
    total: document.querySelector('.pagerTitleCell')?.innerText?.match(/([\d,]+)/)?.[1] || '0',
    page: document.querySelector('.countPageMark')?.innerText || '?',
    url: location.href
  };
}
```

## Sorting (single evaluate_script)

Replace `SORT_HERE` with `"relevance"`, `"date"`, `"citations"`, `"downloads"`, or `"comprehensive"`:

```javascript
async () => {
  const cap = document.querySelector('#tcaptcha_transform_dy');
  if (cap && cap.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  const sortBy = "SORT_HERE";
  const idMap = {
    'relevance': 'FFD', 'date': 'PT',
    'citations': 'CF', 'downloads': 'DFR', 'comprehensive': 'ZH'
  };

  const liId = idMap[sortBy];
  if (!liId) return { error: 'invalid_sort', valid: Object.keys(idMap) };

  const li = document.querySelector('#orderList li#' + liId);
  if (!li) return { error: 'sort_option_not_found' };

  const prevMark = document.querySelector('.countPageMark')?.innerText;
  li.click();

  // Wait for results to refresh (page resets to 1)
  await new Promise((r, j) => {
    let n = 0;
    const c = () => {
      const mark = document.querySelector('.countPageMark')?.innerText;
      if (mark && mark !== prevMark) r();
      else if (++n > 30) j('timeout');
      else setTimeout(c, 500);
    };
    setTimeout(c, 1000);
  });

  return {
    sortBy,
    total: document.querySelector('.pagerTitleCell')?.innerText?.match(/([\d,]+)/)?.[1] || '0',
    page: document.querySelector('.countPageMark')?.innerText || '?',
    activeLi: document.querySelector('#orderList li.cur')?.innerText?.trim(),
    url: location.href
  };
}
```

## Output

> Navigated to page {page}. Total {total} results.
> Results now sorted by {sortBy}.

## Tool calls: 1 (evaluate_script only)

## Verified selectors

| Element | Selector | Notes |
|---------|----------|-------|
| Page links | `.pages a` | numbers + 上一页/下一页 |
| Current page | `.pages a.cur` | |
| Next page | text `下一页`, class `pagesnums` | |
| Page counter | `.countPageMark` | text "1/300" |
| Sort container | `#sortList` (`.order-group`) | |
| Sort options | `#orderList li` | click to sort |
| 相关度 | `li#FFD` | data-sort="FFD" |
| 发表时间 | `li#PT` | data-sort="PT" |
| 被引 | `li#CF` | data-sort="CF" |
| 下载 | `li#DFR` | data-sort="DFR" |
| 综合 | `li#ZH` | data-sort="ZH" |
| Active sort | `#orderList li.cur` | has class `cur` |

## Captcha detection

Check `#tcaptcha_transform_dy` element's `getBoundingClientRect().top >= 0`.
Only active when `top >= 0` (visible). Pre-loaded SDK sits at `top: -1000000px`.


## 注意事项

1. **验证码处理**: 知网使用腾讯滑块验证码，需要手动完成
2. **登录状态**: 某些功能需要知网账号登录
3. **访问频率**: 建议操作间隔3-5秒，避免触发反爬
4. **浏览器**: 确保Hermes浏览器工具已启动

## 参考链接

- 原始技能: https://github.com/cookjohn/cnki-skills/tree/main/skills/cnki-navigate-pages
- Hermes文档: https://hermes-agent.nousresearch.com/docs
