# 安装指南

## 系统要求

- macOS / Linux / Windows (WSL)
- Hermes Agent 已安装
- Python 3.8+
- 网络连接

## 安装步骤

### 方法1: 一键安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/LonelyGemini1979/cnki-skills.git
cd cnki-skills/hermes

# 运行安装脚本
./install.sh
```

### 方法2: 手动安装

```bash
# 克隆仓库
git clone https://github.com/LonelyGemini1979/cnki-skills.git

# 复制技能到Hermes
cp -r cnki-skills/hermes/skills/* ~/.hermes/skills/research/
```

### 方法3: 从原仓库安装

```bash
# 添加远程仓库
git remote add upstream https://github.com/cookjohn/cnki-skills.git
git fetch upstream

# 复制技能
cp -r upstream/main/skills/* ~/.hermes/skills/research/
```

## 验证安装

```bash
# 查看已安装的技能
ls -la ~/.hermes/skills/research/ | grep cnki

# 应该看到:
# cnki-search
# cnki-advanced-search
# cnki-download
# cnki-export
# cnki-journal-index
# cnki-journal-search
# cnki-journal-toc
# cnki-navigate-pages
# cnki-paper-detail
# cnki-parse-results
```

## 配置

### 1. 启动浏览器

```bash
# 启动Hermes浏览器
hermes browser start
```

### 2. 登录知网（可选）

如需下载全文，请先在浏览器中登录知网：
1. 打开 https://www.cnki.net
2. 点击"登录"
3. 输入账号密码
4. 完成登录

## 故障排除

### 问题: 技能未找到

**解决方案:**
```bash
# 检查技能目录
ls -la ~/.hermes/skills/research/

# 重新安装
./install.sh
```

### 问题: 浏览器未启动

**解决方案:**
```bash
# 启动浏览器
hermes browser start

# 检查状态
hermes browser status
```

### 问题: 权限错误

**解决方案:**
```bash
# 修改权限
chmod -R 755 ~/.hermes/skills/research/cnki-*
```

## 卸载

```bash
# 删除所有CNKI技能
rm -rf ~/.hermes/skills/research/cnki-*
```

## 更新

```bash
# 进入仓库目录
cd cnki-skills

# 拉取最新代码
git pull origin master

# 重新安装
cd hermes
./install.sh
```
