# 故障排除

## 常见问题

### 1. 技能未找到

**症状**: Hermes提示找不到CNKI技能

**原因**: 技能未正确安装

**解决方案**:
```bash
# 检查技能目录
ls -la ~/.hermes/skills/research/ | grep cnki

# 如果没有输出，重新安装
cd ~/workspace/cnki-skills/hermes
./install.sh
```

### 2. 浏览器未启动

**症状**: 提示浏览器工具不可用

**解决方案**:
```bash
# 启动浏览器
hermes browser start

# 检查状态
hermes browser status

# 如果失败，重启Hermes
hermes restart
```

### 3. 验证码问题

**症状**: 频繁出现腾讯滑块验证码

**原因**: 访问频率过高触发反爬

**解决方案**:
- 降低访问频率（每次操作间隔5-10秒）
- 手动完成验证码
- 更换网络环境（如使用手机热点）
- 等待一段时间后重试

### 4. 登录状态丢失

**症状**: 下载时提示需要登录

**解决方案**:
1. 在浏览器中打开 https://www.cnki.net
2. 点击"登录"并输入账号密码
3. 保持浏览器会话，不要关闭
4. 重新尝试下载

### 5. 下载失败

**症状**: 点击下载无反应或失败

**可能原因**:
- 未登录知网账号
- 论文需要付费
- 网络连接问题
- 浏览器阻止下载

**解决方案**:
```bash
# 检查网络
ping kns.cnki.net

# 检查浏览器下载设置
# 确保允许知网下载文件

# 尝试手动下载
# 在浏览器中直接访问下载链接
```

### 6. 搜索结果为空

**症状**: 搜索返回0条结果

**可能原因**:
- 关键词过于精确
- 筛选条件过于严格
- 知网服务器问题

**解决方案**:
- 使用更宽泛的关键词
- 减少筛选条件
- 尝试同义词或相关词
- 稍后重试

### 7. 页面加载超时

**症状**: 页面长时间无法加载

**解决方案**:
```bash
# 检查网络速度
speedtest

# 清除浏览器缓存
# 在浏览器中清除知网的缓存和Cookie

# 更换DNS
# 尝试使用 8.8.8.8 或 114.114.114.114
```

### 8. Zotero导出失败

**症状**: 无法推送到Zotero

**解决方案**:
1. 确保Zotero已启动
2. 检查Zotero Connector是否安装
3. 验证Zotero API密钥（如需要）
4. 尝试手动导出RIS文件再导入

## 错误代码

| 错误代码 | 含义 | 解决方案 |
|---------|------|----------|
| CAPTCHA_REQUIRED | 需要验证码 | 手动完成验证 |
| LOGIN_REQUIRED | 需要登录 | 登录知网账号 |
| PERMISSION_DENIED | 无权限 | 检查论文权限 |
| NETWORK_ERROR | 网络错误 | 检查网络连接 |
| TIMEOUT | 请求超时 | 增加等待时间 |
| IP_BLOCKED | IP被封 | 更换IP或等待 |
| BROWSER_NOT_FOUND | 浏览器未启动 | 启动浏览器 |
| SKILL_NOT_FOUND | 技能未找到 | 重新安装技能 |

## 调试模式

### 启用详细日志

```bash
# 设置环境变量
export HERMES_DEBUG=1
export CNKI_DEBUG=1

# 运行Hermes
hermes chat
```

### 查看日志

```bash
# Hermes日志
tail -f ~/.hermes/logs/hermes.log

# 浏览器日志
tail -f ~/.hermes/logs/browser.log
```

### 手动测试

```bash
# 测试浏览器
hermes browser test

# 测试网络
curl -I https://kns.cnki.net

# 测试技能
python3 ~/.hermes/skills/research/cnki-search/scripts/cnki_search.py
```

## 性能优化

### 提高速度

1. **使用缓存**: 重复搜索时使用缓存结果
2. **减少请求**: 批量获取数据，减少页面跳转
3. **优化选择器**: 使用精确的CSS选择器
4. **并行处理**: 多个独立操作并行执行

### 减少验证码

1. **控制频率**: 每次操作间隔5-10秒
2. **模拟人工**: 添加随机延迟
3. **使用代理**: 轮换IP地址（如需要）
4. **保持会话**: 避免频繁重新登录

## 获取帮助

### 社区支持

- GitHub Issues: https://github.com/LonelyGemini1979/cnki-skills/issues
- Hermes Discord: https://discord.gg/hermes
- 知网帮助: https://help.cnki.net

### 报告Bug

提交Issue时请包含：
1. 操作系统和版本
2. Hermes版本
3. 错误信息完整截图
4. 复现步骤
5. 相关日志

### 贡献代码

欢迎提交Pull Request：
1. Fork仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request
