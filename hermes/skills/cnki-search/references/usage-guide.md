# CNKI检索使用指南

## 快速开始

### 1. 基础检索

**用户提问示例：**
- "帮我搜索'颈椎病'相关的中文论文"
- "在知网上查找'脊髓型颈椎病'的文献"
- "搜索'MRI诊断'相关的中文研究"

**助手操作流程：**
1. 使用 `browser_navigate` 打开知网检索页面
2. 使用 `browser_type` 在搜索框输入关键词
3. 使用 `browser_click` 点击搜索按钮
4. 使用 `browser_snapshot` 获取结果页面
5. 使用 `browser_console` 执行JavaScript提取数据
6. 使用脚本解析并格式化结果

### 2. 高级检索

**支持字段：**
- 主题：SU='关键词'
- 作者：AU='作者名'
- 期刊：LY='期刊名'
- 年份：YE BETWEEN ('2020','2024')
- 文献类型：期刊、博硕、会议

**示例查询：**
```
SU='颈椎病' AND AU='张三' AND YE BETWEEN ('2020','2024')
```

### 3. 获取论文详情

**操作步骤：**
1. 点击论文标题链接
2. 等待详情页加载
3. 提取标题、作者、摘要、关键词
4. 获取PDF/CAJ下载链接

### 4. 下载全文

**前提条件：**
- 已登录知网账号（个人或机构）
- 论文有下载权限

**操作流程：**
1. 在详情页找到下载链接
2. 点击PDF或CAJ下载
3. 处理可能的验证码
4. 保存文件到本地

## 浏览器命令参考

### 打开知网
```javascript
browser_navigate(url="https://kns.cnki.net/kns8s/defaultresult/index")
```

### 输入关键词
```javascript
browser_type(ref="@search_input", text="颈椎病")
```

### 点击搜索
```javascript
browser_click(ref="@search_button")
```

### 提取结果
```javascript
browser_console(code="""
  const results = [];
  document.querySelectorAll('.result-item').forEach(item => {
    results.push({
      title: item.querySelector('.title').innerText,
      authors: item.querySelector('.authors').innerText,
      journal: item.querySelector('.journal').innerText,
      url: item.querySelector('a').href
    });
  });
  return results;
""")
```

## 常见问题处理

### 1. 遇到验证码

**现象：** 页面显示腾讯滑块验证码

**处理方法：**
1. 暂停自动化操作
2. 提示用户手动完成验证
3. 等待验证完成后继续

**代码示例：**
```javascript
// 检测验证码
const captcha = document.querySelector('.captcha');
if (captcha) {
  console.log('检测到验证码，请手动完成验证');
  // 暂停执行，等待用户操作
}
```

### 2. 登录状态检查

**检查是否已登录：**
```javascript
const loginStatus = document.querySelector('.user-info');
if (!loginStatus) {
  console.log('未登录，请先登录知网账号');
}
```

### 3. 下载权限检查

**检查下载权限：**
```javascript
const downloadBtn = document.querySelector('.download-btn');
if (downloadBtn.disabled) {
  console.log('无下载权限，需要登录或购买');
}
```

## 数据解析技巧

### 提取论文标题
```javascript
const titles = Array.from(document.querySelectorAll('.paper-title'))
  .map(el => el.innerText.trim());
```

### 提取作者信息
```javascript
const authors = Array.from(document.querySelectorAll('.author-name'))
  .map(el => el.innerText.trim());
```

### 提取摘要
```javascript
const abstract = document.querySelector('.abstract-content')?.innerText.trim();
```

### 提取下载链接
```javascript
const pdfLink = document.querySelector('a[href*=".pdf"]')?.href;
const cajLink = document.querySelector('a[href*=".caj"]')?.href;
```

## 结果格式化

### 文本格式
```
1. 颈椎病MRI诊断研究
   作者: 张三, 李四
   期刊: 中华骨科杂志
   年份: 2024
   下载: PDF | CAJ
```

### JSON格式
```json
{
  "title": "颈椎病MRI诊断研究",
  "authors": ["张三", "李四"],
  "journal": "中华骨科杂志",
  "year": "2024",
  "downloads": {
    "pdf": "https://...",
    "caj": "https://..."
  }
}
```

### CSV格式
```csv
标题,作者,期刊,年份,PDF链接,CAJ链接
颈椎病MRI诊断研究,"张三,李四",中华骨科杂志,2024,https://...,https://...
```

## 最佳实践

1. **控制访问频率**：每次操作间隔2-3秒，避免触发反爬
2. **使用高级检索**：精确检索减少结果数量
3. **批量处理**：一次检索多篇论文，减少请求次数
4. **错误重试**：网络错误时自动重试，验证码时人工介入
5. **结果缓存**：保存检索结果，避免重复请求

## 限制与注意事项

- **验证码**：知网使用腾讯滑块，无法自动绕过
- **付费墙**：部分论文需要付费或机构权限
- **IP限制**：频繁访问可能导致IP被封
- **格式限制**：部分论文仅提供CAJ格式
- **下载速度**：受知网服务器限制，大文件下载较慢

## 故障排除

### 问题：搜索无结果
**可能原因：**
- 关键词过于精确
- 网络连接问题
- 知网服务器繁忙

**解决方案：**
- 尝试更宽泛的关键词
- 检查网络连接
- 稍后重试

### 问题：下载失败
**可能原因：**
- 未登录账号
- 无下载权限
- 网络中断

**解决方案：**
- 登录知网账号
- 检查论文权限
- 重新下载

### 问题：页面加载慢
**可能原因：**
- 网络速度慢
- 知网服务器负载高
- 浏览器缓存问题

**解决方案：**
- 等待页面完全加载
- 清除浏览器缓存
- 更换网络环境
