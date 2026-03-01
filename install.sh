#!/bin/bash

# Magic Skills 一键安装脚本
# One-click installation script for Magic Skills
# 支援 macOS / Linux

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_banner() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║              🔮 Magic Skills 一键安装脚本                    ║"
    echo "║              One-Click Installation Script                   ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

# 检查系统
check_system() {
    print_info "检查系统环境..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_success "检测到 macOS 系统"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_success "检测到 Linux 系统"
    else
        print_error "不支持的操作系统: $OSTYPE"
        print_info "目前仅支持 macOS 和 Linux"
        exit 1
    fi
    
    # 检查架构
    ARCH=$(uname -m)
    print_info "系统架构: $ARCH"
}

# 检查依赖
check_dependencies() {
    print_info "检查依赖..."
    
    # 检查 Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python3 已安装: $PYTHON_VERSION"
        
        # 检查 Python 版本 >= 3.9
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
            print_error "Python 版本需要 >= 3.9"
            print_info "请升级 Python: https://www.python.org/downloads/"
            exit 1
        fi
    else
        print_error "未找到 Python3"
        print_info "请安装 Python 3.9+: https://www.python.org/downloads/"
        exit 1
    fi
    
    # 检查 pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 已安装"
    else
        print_warning "pip3 未安装，尝试安装..."
        python3 -m ensurepip --upgrade 2>/dev/null || {
            print_error "无法安装 pip"
            print_info "请手动安装 pip: https://pip.pypa.io/en/stable/installation/"
            exit 1
        }
    fi
    
    # 检查 Git
    if command -v git &> /dev/null; then
        print_success "Git 已安装"
    else
        print_warning "Git 未安装"
        if [ "$OS" == "macos" ]; then
            print_info "建议安装 Xcode Command Line Tools: xcode-select --install"
        else
            print_info "请安装 Git: sudo apt-get install git 或 sudo yum install git"
        fi
    fi
}

# 获取安装目录
get_install_dir() {
    print_info "选择安装方式..."
    echo ""
    echo "1) 安装到当前目录 ($(pwd))"
    echo "2) 安装到用户目录 (~/.magic-skills)"
    echo "3) 安装到系统目录 (/usr/local/share/magic-skills)"
    echo "4) 自定义目录"
    echo ""
    read -p "请选择 [1-4] (默认: 2): " choice
    
    case $choice in
        1)
            INSTALL_DIR="$(pwd)"
            ;;
        3)
            INSTALL_DIR="/usr/local/share/magic-skills"
            NEED_SUDO=true
            ;;
        4)
            read -p "请输入安装目录: " custom_dir
            INSTALL_DIR="$custom_dir"
            ;;
        *)
            INSTALL_DIR="$HOME/.magic-skills"
            ;;
    esac
    
    print_info "安装目录: $INSTALL_DIR"
}

# 克隆仓库
clone_repo() {
    if [ -d "$INSTALL_DIR" ] && [ "$(ls -A $INSTALL_DIR)" ]; then
        print_warning "目录 $INSTALL_DIR 已存在且不为空"
        read -p "是否覆盖? [y/N]: " overwrite
        if [[ $overwrite =~ ^[Yy]$ ]]; then
            rm -rf "$INSTALL_DIR"
        else
            print_info "使用现有目录"
            return
        fi
    fi
    
    print_info "克隆 Magic Skills 仓库..."
    
    # 检查是否是本地安装（脚本在仓库内）
    if [ -f "$(dirname "$0")/pyproject.toml" ]; then
        print_info "检测到本地仓库，直接复制..."
        mkdir -p "$INSTALL_DIR"
        cp -r "$(dirname "$0")"/* "$INSTALL_DIR/"
    else
        git clone https://github.com/magicskills/magic-skills.git "$INSTALL_DIR" 2>/dev/null || {
            print_warning "GitHub 克隆失败，尝试 Gitee..."
            git clone https://gitee.com/magicskills/magic-skills.git "$INSTALL_DIR" 2>/dev/null || {
                print_error "无法克隆仓库"
                print_info "请检查网络连接或手动下载"
                exit 1
            }
        }
    fi
    
    print_success "仓库已克隆到 $INSTALL_DIR"
}

# 创建虚拟环境
setup_venv() {
    print_info "创建 Python 虚拟环境..."
    
    cd "$INSTALL_DIR"
    
    if [ -d "venv" ]; then
        print_warning "虚拟环境已存在"
        read -p "是否重新创建? [y/N]: " recreate
        if [[ $recreate =~ ^[Yy]$ ]]; then
            rm -rf venv
            python3 -m venv venv
        fi
    else
        python3 -m venv venv
    fi
    
    print_success "虚拟环境创建完成"
}

# 安装依赖
install_dependencies() {
    print_info "安装依赖..."
    
    cd "$INSTALL_DIR"
    source venv/bin/activate
    
    # 升级 pip
    pip install --upgrade pip setuptools wheel
    
    # 安装项目
    pip install -e ".[dev]"
    
    print_success "依赖安装完成"
}

# 配置环境变量
setup_env() {
    print_info "配置环境变量..."
    
    # 创建 .env 文件
    if [ ! -f "$INSTALL_DIR/.env" ]; then
        cat > "$INSTALL_DIR/.env" << 'EOF'
# Magic Skills 环境变量配置
# 请填写你的 API 密钥

# OpenAI (默认)
OPENAI_API_KEY=your-openai-api-key-here

# 其他可选提供商
# ANTHROPIC_API_KEY=your-anthropic-key
# GOOGLE_API_KEY=your-google-key
# AZURE_OPENAI_API_KEY=your-azure-key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# 默认模型配置
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-4o

# 日志级别: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO
EOF
        print_success "已创建 .env 配置文件"
    fi
    
    # 询问是否配置 API 密钥
    echo ""
    read -p "是否现在配置 OpenAI API 密钥? [y/N]: " setup_key
    if [[ $setup_key =~ ^[Yy]$ ]]; then
        read -sp "请输入 OpenAI API 密钥: " api_key
        echo ""
        if [ -n "$api_key" ]; then
            sed -i.bak "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" "$INSTALL_DIR/.env"
            rm -f "$INSTALL_DIR/.env.bak"
            print_success "API 密钥已配置"
        fi
    fi
}

# 创建启动脚本
create_launcher() {
    print_info "创建启动脚本..."
    
    # 选择安装位置：优先使用 /usr/local/bin（系统级，已在PATH中）
    if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
        BIN_DIR="/usr/local/bin"
        print_info "使用系统目录: $BIN_DIR"
    elif [ -d "/usr/local/bin" ]; then
        # 需要sudo权限
        BIN_DIR="/usr/local/bin"
        USE_SUDO=true
        print_info "使用系统目录（需要管理员权限）: $BIN_DIR"
    else
        # 回退到用户目录
        BIN_DIR="$HOME/.local/bin"
        mkdir -p "$BIN_DIR"
        print_info "使用用户目录: $BIN_DIR"
        
        # 如果用户目录不在PATH中，需要添加到shell配置
        if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
            add_to_shell_rc "$BIN_DIR"
        fi
    fi
    
    # 创建启动器脚本 - 使用临时文件
    local tmp_dir=$(mktemp -d)
    
    # 创建 magic-skill 脚本 - 使用直接运行方式
    cat > "$tmp_dir/magic-skill" << 'LAUNCHER_EOF'
#!/bin/bash
# Magic Skills 启动脚本
# 安装目录: INSTALL_DIR_PLACEHOLDER

# 保存当前工作目录（用户执行命令的目录）
USER_CWD="$(pwd)"

# 激活虚拟环境
source "INSTALL_DIR_PLACEHOLDER/venv/bin/activate"

# 设置 PYTHONPATH（包含安装目录）
export PYTHONPATH="INSTALL_DIR_PLACEHOLDER:${PYTHONPATH:+:$PYTHONPATH}"

# 加载环境变量（优先从安装目录加载）
if [ -f "INSTALL_DIR_PLACEHOLDER/.env" ]; then
    set -a
    source "INSTALL_DIR_PLACEHOLDER/.env"
    set +a
fi

# 切换到用户当前工作目录执行命令
# 确保 Path.cwd() 返回正确的目录
cd "$USER_CWD" || exit 1
exec python -c "from cli.main import cli; cli()" "$@"
LAUNCHER_EOF

    # 创建 magic-skill-server 脚本
    cat > "$tmp_dir/magic-skill-server" << 'SERVER_EOF'
#!/bin/bash
# Magic Skills API Server 启动脚本
source "INSTALL_DIR_PLACEHOLDER/venv/bin/activate"
export PYTHONPATH="INSTALL_DIR_PLACEHOLDER:${PYTHONPATH:+:$PYTHONPATH}"

# 加载环境变量
if [ -f "INSTALL_DIR_PLACEHOLDER/.env" ]; then
    set -a
    source "INSTALL_DIR_PLACEHOLDER/.env"
    set +a
fi

# 使用 uvicorn 直接启动，传递所有参数
# 注意：服务器需要在安装目录运行以找到正确的模块路径
cd "INSTALL_DIR_PLACEHOLDER"
exec python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 "$@"
SERVER_EOF

    # 创建 magic-skill-mcp 脚本
    cat > "$tmp_dir/magic-skill-mcp" << 'MCP_EOF'
#!/bin/bash
# Magic Skills MCP Server 启动脚本
source "INSTALL_DIR_PLACEHOLDER/venv/bin/activate"
export PYTHONPATH="INSTALL_DIR_PLACEHOLDER:${PYTHONPATH:+:$PYTHONPATH}"

# 加载环境变量
if [ -f "INSTALL_DIR_PLACEHOLDER/.env" ]; then
    set -a
    source "INSTALL_DIR_PLACEHOLDER/.env"
    set +a
fi

# MCP 服务器需要在安装目录运行
cd "INSTALL_DIR_PLACEHOLDER"
python -c "from src.mcp.server import main; main()" "$@"
MCP_EOF

    # 替换占位符为实际路径
    for script in "$tmp_dir"/magic-skill*; do
        sed -i.bak "s|INSTALL_DIR_PLACEHOLDER|$INSTALL_DIR|g" "$script"
        rm -f "$script.bak"
    done

    # 写入脚本到目标目录
    if [ "$USE_SUDO" = true ]; then
        print_info "需要管理员权限安装到 $BIN_DIR"
        sudo cp "$tmp_dir/magic-skill" "$BIN_DIR/magic-skill"
        sudo cp "$tmp_dir/magic-skill-server" "$BIN_DIR/magic-skill-server"
        sudo cp "$tmp_dir/magic-skill-mcp" "$BIN_DIR/magic-skill-mcp"
        sudo chmod +x "$BIN_DIR/magic-skill" "$BIN_DIR/magic-skill-server" "$BIN_DIR/magic-skill-mcp"
    else
        cp "$tmp_dir/magic-skill" "$BIN_DIR/magic-skill"
        cp "$tmp_dir/magic-skill-server" "$BIN_DIR/magic-skill-server"
        cp "$tmp_dir/magic-skill-mcp" "$BIN_DIR/magic-skill-mcp"
        chmod +x "$BIN_DIR/magic-skill" "$BIN_DIR/magic-skill-server" "$BIN_DIR/magic-skill-mcp"
    fi
    
    # 清理临时文件
    rm -rf "$tmp_dir"
    
    print_success "启动脚本已安装到 $BIN_DIR"
}

# 添加到 shell 配置文件
add_to_shell_rc() {
    local bin_dir="$1"
    
    SHELL_RC=""
    # 检测当前使用的 shell
    if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = */zsh ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ] || [ "$SHELL" = */bash ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        # 默认尝试 .zshrc，如果不存在则尝试 .bashrc
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            SHELL_RC="$HOME/.bashrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            SHELL_RC="$HOME/.bash_profile"
        else
            # 创建 .zshrc（macOS 默认）
            SHELL_RC="$HOME/.zshrc"
            touch "$SHELL_RC"
            print_info "创建 $SHELL_RC"
        fi
    fi
    
    if [ -n "$SHELL_RC" ]; then
        # 检查是否已存在
        if ! grep -q "$bin_dir" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# Magic Skills" >> "$SHELL_RC"
            echo "export PATH=\"$bin_dir:\$PATH\"" >> "$SHELL_RC"
            print_success "已添加到 $SHELL_RC"
            print_warning "请运行: source $SHELL_RC"
        fi
    fi
}

# 配置 AI Tools
setup_ai_tools() {
    print_info "配置 AI Tools..."
    
    # Cursor
    if [ -d "$HOME/.cursor" ]; then
        print_info "检测到 Cursor，配置 MCP..."
        mkdir -p "$HOME/.cursor"
        cat > "$HOME/.cursor/mcp.json" << EOF
{
  "mcpServers": {
    "magic-skills": {
      "command": "$HOME/.local/bin/magic-skill-mcp",
      "env": {
        "PYTHONPATH": "$INSTALL_DIR"
      }
    }
  }
}
EOF
        print_success "Cursor MCP 配置完成"
    fi
    
    # Claude Desktop
    if [ -d "$HOME/Library/Application Support/Claude" ]; then
        print_info "检测到 Claude Desktop，配置 MCP..."
        CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
        mkdir -p "$(dirname "$CLAUDE_CONFIG")"
        cat > "$CLAUDE_CONFIG" << EOF
{
  "mcpServers": {
    "magic-skills": {
      "command": "$HOME/.local/bin/magic-skill-mcp",
      "env": {
        "PYTHONPATH": "$INSTALL_DIR"
      }
    }
  }
}
EOF
        print_success "Claude Desktop MCP 配置完成"
    fi
    
    print_info "Kiro IDE 配置已包含在项目 .kiro/ 目录中"
}

# 验证安装
verify_installation() {
    print_info "验证安装..."
    
    cd "$INSTALL_DIR"
    source venv/bin/activate
    
    # 检查 Python 模块能否正常导入
    if python -c "from cli.main import cli; print('CLI OK')" 2>/dev/null; then
        print_success "CLI 模块导入正常"
    else
        print_warning "CLI 模块导入失败"
    fi
    
    if python -c "from api.main import app; print('API OK')" 2>/dev/null; then
        print_success "API 模块导入正常"
    else
        print_warning "API 模块导入失败"
    fi
    
    if python -c "from src.mcp.server import main; print('MCP OK')" 2>/dev/null; then
        print_success "MCP 模块导入正常"
    else
        print_warning "MCP 模块导入失败"
    fi
    
    # 检查命令是否存在
    if [ -f "/usr/local/bin/magic-skill" ]; then
        print_success "magic-skill 已安装到 /usr/local/bin"
    elif [ -f "$HOME/.local/bin/magic-skill" ]; then
        print_success "magic-skill 已安装到 ~/.local/bin"
        # 检查是否在 PATH 中
        if command -v magic-skill &> /dev/null; then
            print_success "magic-skill 在 PATH 中"
        else
            print_warning "~/.local/bin 不在 PATH 中，安装完成后可能需要 source 配置文件"
        fi
    else
        print_warning "magic-skill 未找到"
    fi
    
    print_success "安装验证完成"
}

# 打印使用说明
print_usage() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🎉 安装完成!                              ║"
    echo "║                 Installation Complete!                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📁 安装目录: $INSTALL_DIR"
    echo ""
    
    # 检查命令安装位置
    if [ -f "/usr/local/bin/magic-skill" ]; then
        echo "✅ magic-skill 已安装到系统目录，立即可用"
        echo ""
        echo "🚀 立即尝试:"
        echo ""
        echo "  magic-skill list"
        echo ""
    elif command -v magic-skill &> /dev/null; then
        echo "✅ magic-skill 命令已就绪"
        echo ""
        echo "🚀 立即尝试:"
        echo ""
        echo "  magic-skill list"
        echo ""
    else
        echo "⚠️  ~/.local/bin 不在 PATH 中"
        echo ""
        echo "🔧 请执行以下命令之一:"
        echo ""
        # 检测应该 source 哪个文件
        if [ -f "$HOME/.zshrc" ]; then
            echo "  source ~/.zshrc"
        fi
        if [ -f "$HOME/.bashrc" ]; then
            echo "  source ~/.bashrc"
        fi
        if [ -f "$HOME/.bash_profile" ]; then
            echo "  source ~/.bash_profile"
        fi
        echo ""
        echo "或重新打开终端"
        echo ""
        echo "然后就可以使用:"
        echo ""
        echo "  magic-skill list"
        echo ""
    fi
    
    echo "📚 常用命令:"
    echo ""
    echo "  列出所有技能:"
    echo "     magic-skill list"
    echo ""
    echo "  执行技能:"
    echo "     magic-skill exec /mgc-java-backend-controller-gen -p '{\"endpoint\":\"/api/users\"}'"
    echo ""
    echo "  启动 API 服务器:"
    echo "     magic-skill-server"
    echo ""
    echo "  启动 MCP 服务器:"
    echo "     magic-skill-mcp"
    echo ""
    echo "📖 文档:"
    echo "  - 使用指南: $INSTALL_DIR/README.md"
    echo "  - 命令参考: $INSTALL_DIR/COMMANDS_REFERENCE.md"
    echo "  - AI Tools 集成: $INSTALL_DIR/AI_TOOLS_INTEGRATION.md"
    echo ""
    echo "⚙️  配置:"
    echo "  - 编辑配置文件: $INSTALL_DIR/.env"
    echo ""
    echo "💡 提示:"
    echo "  - 在 Kiro/Cursor/Claude Desktop 中输入 /mgc- 查看可用技能"
    echo "  - 使用 /mgc-list 列出所有技能"
    echo "  - 使用 /mgc-help 获取帮助"
    echo ""
}

# 主函数
main() {
    print_banner
    
    check_system
    check_dependencies
    get_install_dir
    clone_repo
    setup_venv
    install_dependencies
    setup_env
    create_launcher
    setup_ai_tools
    verify_installation
    print_usage
}

# 运行主函数
main
