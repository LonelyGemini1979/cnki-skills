#!/bin/bash
# CNKI Skills for Hermes - 一键安装脚本

set -e

echo "🚀 开始安装 CNKI Skills for Hermes..."
echo ""

# 检查Hermes是否安装
if [ ! -d "$HOME/.hermes" ]; then
    echo "❌ 错误: 未找到Hermes安装目录"
    echo "请先安装Hermes: https://github.com/NousResearch/hermes-agent"
    exit 1
fi

# 创建目标目录
TARGET_DIR="$HOME/.hermes/skills/research"
mkdir -p "$TARGET_DIR"

echo "📁 目标目录: $TARGET_DIR"
echo ""

# 安装所有技能
SKILLS=(
    "cnki-search"
    "cnki-advanced-search"
    "cnki-download"
    "cnki-export"
    "cnki-journal-index"
    "cnki-journal-search"
    "cnki-journal-toc"
    "cnki-navigate-pages"
    "cnki-paper-detail"
    "cnki-parse-results"
)

for skill in "${SKILLS[@]}"; do
    if [ -d "skills/$skill" ]; then
        echo "📦 安装 $skill..."
        cp -r "skills/$skill" "$TARGET_DIR/"
        echo "   ✅ 完成"
    else
        echo "   ⚠️  跳过 $skill (目录不存在)"
    fi
done

echo ""
echo "✅ 所有技能安装完成！"
echo ""
echo "📚 已安装的技能:"
ls -1 "$TARGET_DIR" | grep cnki | sed 's/^/   - /'
echo ""
echo "🎯 使用方法:"
echo "   直接对Hermes说:"
echo "   - '帮我搜索颈椎病相关论文'"
echo "   - '下载这篇论文的PDF'"
echo "   - '将这篇论文导出到Zotero'"
echo ""
echo "📖 查看文档:"
echo "   cat $TARGET_DIR/cnki-search/SKILL.md"
echo ""
echo "🔗 更多信息:"
echo "   https://github.com/LonelyGemini1979/cnki-skills"
