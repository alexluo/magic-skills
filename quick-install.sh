#!/bin/bash
# Magic Skills 快速安装脚本
# 使用方式: curl -fsSL https://raw.githubusercontent.com/magicskills/magic-skills/main/quick-install.sh | bash

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔮 Magic Skills 快速安装${NC}"
echo ""

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    INSTALL_URL="https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    INSTALL_URL="https://raw.githubusercontent.com/magicskills/magic-skills/main/install.sh"
else
    echo -e "${RED}不支持的操作系统${NC}"
    echo "Windows 用户请使用 PowerShell 安装:"
    echo 'irm https://raw.githubusercontent.com/magicskills/magic-skills/main/install.ps1 | iex'
    exit 1
fi

# 创建临时目录
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

# 下载安装脚本
echo "📥 下载安装脚本..."
if command -v curl &> /dev/null; then
    curl -fsSL "$INSTALL_URL" -o install.sh
elif command -v wget &> /dev/null; then
    wget -q "$INSTALL_URL" -O install.sh
else
    echo -e "${RED}需要 curl 或 wget${NC}"
    exit 1
fi

# 执行安装
echo "🚀 开始安装..."
chmod +x install.sh
./install.sh

# 清理
rm -rf "$TMP_DIR"

echo ""
echo -e "${GREEN}✅ 安装完成!${NC}"
echo ""
echo "请运行: source ~/.zshrc (或 ~/.bashrc)"
echo "然后使用: magic-skill list"
