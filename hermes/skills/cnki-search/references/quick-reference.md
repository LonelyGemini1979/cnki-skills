# CNKI快速参考

## 常用操作命令

### 基础检索
```
用户: 搜索"颈椎病"相关论文
助手: [使用browser工具打开知网并搜索]
```

### 高级检索
```
用户: 搜索2020-2024年张三发表的颈椎病论文
助手: [使用高级检索，设置作者和时间范围]
```

### 获取详情
```
用户: 获取这篇论文的详细信息
助手: [点击论文标题，提取详情页信息]
```

### 下载全文
```
用户: 下载这篇论文的PDF
助手: [点击下载链接，保存PDF文件]
```

## 知网URL结构

### 检索页面
- 基础检索: https://kns.cnki.net/kns8s/defaultresult/index
- 高级检索: https://kns.cnki.net/kns8s/AdvSearch
- 专业检索: https://kns.cnki.net/kns8s/ProSearch

### 详情页面
- 论文详情: https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=XXX
- 期刊详情: https://navi.cnki.net/knavi/journals/XXX/detail

### 下载链接
- PDF下载: https://kns.cnki.net/kcms/detail/download.aspx?dbcode=CJFD&filename=XXX&dflag=pdfdown
- CAJ下载: https://kns.cnki.net/kcms/detail/download.aspx?dbcode=CJFD&filename=XXX&dflag=cajdown

## 常用选择器

### 搜索框
```css
input[placeholder*="检索"]
input.search-input
#searchInput
```

### 搜索按钮
```css
button.search-btn
input[type="submit"]
.search-button
```

### 结果列表
```css
.result-item
.paper-item
tr[bgcolor]
```

### 论文标题
```css
.paper-title
.fz14
a.title
```

### 作者信息
```css
.author
.author-name
td.author
```

### 下载按钮
```css
.download-btn
.btn-download
a[href*="download"]
```

## JavaScript代码片段

### 提取所有论文标题
```javascript
Array.from(document.querySelectorAll('.paper-title'))
  .map(el => el.innerText.trim())
```

### 提取论文链接
```javascript
Array.from(document.querySelectorAll('.paper-title a'))
  .map(el => el.href)
```

### 提取作者列表
```javascript
Array.from(document.querySelectorAll('.author-name'))
  .map(el => el.innerText.trim())
```

### 检查登录状态
```javascript
!!document.querySelector('.user-info')
```

### 检查验证码
```javascript
!!document.querySelector('.captcha')
```

## 错误代码

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| CAPTCHA_REQUIRED | 需要验证码 | 手动完成验证 |
| LOGIN_REQUIRED | 需要登录 | 登录知网账号 |
| PERMISSION_DENIED | 无下载权限 | 检查论文权限 |
| NETWORK_ERROR | 网络错误 | 重试或检查网络 |
| TIMEOUT | 请求超时 | 增加等待时间 |
| IP_BLOCKED | IP被封 | 更换IP或等待 |

## 实用技巧

1. **使用引号精确匹配**："颈椎病" 比 颈椎病 更精确
2. **使用OR扩大范围**：颈椎病 OR 颈椎退变
3. **使用AND缩小范围**：颈椎病 AND MRI
4. **使用NOT排除**：颈椎病 NOT 腰椎
5. **限定字段**：TI='颈椎病' 只搜索标题

## 相关资源

- 知网帮助: https://help.cnki.net
- 检索技巧: https://help.cnki.net/search
- 下载说明: https://help.cnki.net/download
- CAJViewer: https://cajviewer.cnki.net
