# Magic Skills 一键安装脚本 (Windows PowerShell)
# One-click installation script for Magic Skills (Windows)

$ErrorActionPreference = "Stop"

# 颜色函数
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Blue }
function Write-Success { param($Message) Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

function Print-Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                              ║" -ForegroundColor Cyan
    Write-Host "║              🔮 Magic Skills 一键安装脚本                    ║" -ForegroundColor Cyan
    Write-Host "║              One-Click Installation Script                   ║" -ForegroundColor Cyan
    Write-Host "║                                                              ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Check-System {
    Write-Info "检查系统环境..."
    
    $os = [System.Environment]::OSVersion.Platform
    Write-Success "检测到 Windows 系统"
    
    $arch = [System.Environment]::Is64BitOperatingSystem
    if ($arch) {
        Write-Info "系统架构: x64"
    } else {
        Write-Info "系统架构: x86"
    }
}

function Check-Dependencies {
    Write-Info "检查依赖..."
    
    # 检查 Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Success "Python 已安装: $pythonVersion"
        
        # 检查版本 >= 3.9
        $version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        $major = [int]($version.Split('.')[0])
        $minor = [int]($version.Split('.')[1])
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
            Write-Error "Python 版本需要 >= 3.9"
            Write-Info "请从 https://www.python.org/downloads/ 下载并安装 Python 3.9+"
            exit 1
        }
    } catch {
        Write-Error "未找到 Python"
        Write-Info "请从 https://www.python.org/downloads/ 下载并安装 Python 3.9+"
        exit 1
    }
    
    # 检查 pip
    try {
        pip --version | Out-Null
        Write-Success "pip 已安装"
    } catch {
        Write-Warning "pip 未安装"
        Write-Info "请确保安装 Python 时勾选了 'Add Python to PATH' 和 'pip'"
    }
    
    # 检查 Git
    try {
        git --version | Out-Null
        Write-Success "Git 已安装"
    } catch {
        Write-Warning "Git 未安装"
        Write-Info "建议安装 Git: https://git-scm.com/download/win"
    }
}

function Get-InstallDir {
    Write-Info "选择安装方式..."
    Write-Host ""
    Write-Host "1) 安装到当前目录 ($(Get-Location))"
    Write-Host "2) 安装到用户目录 ($env:USERPROFILE\.magic-skills)"
    Write-Host "3) 自定义目录"
    Write-Host ""
    
    $choice = Read-Host "请选择 [1-3] (默认: 1)"
    
    switch ($choice) {
        "2" { $script:InstallDir = "$env:USERPROFILE\.magic-skills" }
        "3" { 
            $customDir = Read-Host "请输入安装目录"
            $script:InstallDir = $customDir
        }
        default { $script:InstallDir = Get-Location }
    }
    
    Write-Info "安装目录: $InstallDir"
}

function Clone-Repo {
    if (Test-Path "$InstallDir\pyproject.toml") {
        Write-Warning "目录 $InstallDir 已存在且不为空"
        $overwrite = Read-Host "是否覆盖? [y/N]"
        if ($overwrite -eq "y" -or $overwrite -eq "Y") {
            Remove-Item -Recurse -Force $InstallDir
        } else {
            Write-Info "使用现有目录"
            return
        }
    }
    
    Write-Info "克隆 Magic Skills 仓库..."
    
    # 检查是否是本地安装
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    if (Test-Path "$scriptDir\pyproject.toml") {
        Write-Info "检测到本地仓库，直接复制..."
        Copy-Item -Recurse $scriptDir $InstallDir
    } else {
        try {
            git clone https://github.com/magicskills/magic-skills.git $InstallDir
        } catch {
            Write-Warning "GitHub 克隆失败，尝试 Gitee..."
            try {
                git clone https://gitee.com/magicskills/magic-skills.git $InstallDir
            } catch {
                Write-Error "无法克隆仓库"
                Write-Info "请检查网络连接或手动下载"
                exit 1
            }
        }
    }
    
    Write-Success "仓库已克隆到 $InstallDir"
}

function Setup-Venv {
    Write-Info "创建 Python 虚拟环境..."
    
    Set-Location $InstallDir
    
    if (Test-Path "venv") {
        Write-Warning "虚拟环境已存在"
        $recreate = Read-Host "是否重新创建? [y/N]"
        if ($recreate -eq "y" -or $recreate -eq "Y") {
            Remove-Item -Recurse -Force venv
            python -m venv venv
        }
    } else {
        python -m venv venv
    }
    
    Write-Success "虚拟环境创建完成"
}

function Install-Dependencies {
    Write-Info "安装依赖..."
    
    Set-Location $InstallDir
    & .\venv\Scripts\Activate.ps1
    
    # 升级 pip
    python -m pip install --upgrade pip setuptools wheel
    
    # 安装项目
    pip install -e ".[dev]"
    
    Write-Success "依赖安装完成"
}

function Setup-Env {
    Write-Info "配置环境变量..."
    
    $envFile = "$InstallDir\.env"
    if (-not (Test-Path $envFile)) {
        @"
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
"@ | Out-File -FilePath $envFile -Encoding UTF8
        Write-Success "已创建 .env 配置文件"
    }
    
    $setupKey = Read-Host "是否现在配置 OpenAI API 密钥? [y/N]"
    if ($setupKey -eq "y" -or $setupKey -eq "Y") {
        $apiKey = Read-Host "请输入 OpenAI API 密钥" -AsSecureString
        $plainKey = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey))
        if ($plainKey) {
            (Get-Content $envFile) -replace "OPENAI_API_KEY=.*", "OPENAI_API_KEY=$plainKey" | Set-Content $envFile
            Write-Success "API 密钥已配置"
        }
    }
}

function Create-Launcher {
    Write-Info "创建启动脚本..."
    
    $binDir = "$env:USERPROFILE\.local\bin"
    New-Item -ItemType Directory -Force -Path $binDir | Out-Null
    
    # CLI 启动脚本
    @"
@echo off
REM Magic Skills 启动脚本
call "$InstallDir\venv\Scripts\activate.bat"
set PYTHONPATH=$InstallDir;%PYTHONPATH%

REM 加载环境变量
if exist "$InstallDir\.env" (
    for /f "tokens=*" %%a in ('type "$InstallDir\.env" ^| findstr /v "^#"') do set %%a
)

python -m src.cli.main %*
"@ | Out-File -FilePath "$binDir\magic-skill.bat" -Encoding UTF8
    
    # API 服务器启动脚本
    @"
@echo off
REM Magic Skills API Server 启动脚本
call "$InstallDir\venv\Scripts\activate.bat"
set PYTHONPATH=$InstallDir;%PYTHONPATH%

REM 加载环境变量
if exist "$InstallDir\.env" (
    for /f "tokens=*" %%a in ('type "$InstallDir\.env" ^| findstr /v "^#"') do set %%a
)

cd /d "$InstallDir"
python -m api.main %*
"@ | Out-File -FilePath "$binDir\magic-skill-server.bat" -Encoding UTF8
    
    # MCP 服务器启动脚本
    @"
@echo off
REM Magic Skills MCP Server 启动脚本
call "$InstallDir\venv\Scripts\activate.bat"
set PYTHONPATH=$InstallDir;%PYTHONPATH%

REM 加载环境变量
if exist "$InstallDir\.env" (
    for /f "tokens=*" %%a in ('type "$InstallDir\.env" ^| findstr /v "^#"') do set %%a
)

cd /d "$InstallDir"
python -m src.mcp.server %*
"@ | Out-File -FilePath "$binDir\magic-skill-mcp.bat" -Encoding UTF8
    
    Write-Success "启动脚本已创建"
    
    # 添加到 PATH（当前会话）
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$binDir*") {
        # 更新当前会话
        $env:Path = "$env:Path;$binDir"
        Write-Success "已添加到当前会话 PATH"
        
        # 同时更新用户环境变量
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$binDir", "User")
        Write-Success "已添加到用户 PATH"
    } else {
        # 确保当前会话也有
        if ($env:Path -notlike "*$binDir*") {
            $env:Path = "$env:Path;$binDir"
            Write-Success "已更新当前会话 PATH"
        }
    }
}

function Setup-AITools {
    Write-Info "配置 AI Tools..."
    
    # Cursor
    $cursorDir = "$env:USERPROFILE\.cursor"
    if (Test-Path $cursorDir) {
        Write-Info "检测到 Cursor，配置 MCP..."
        New-Item -ItemType Directory -Force -Path $cursorDir | Out-Null
        $mcpConfig = @{
            mcpServers = @{
                "magic-skills" = @{
                    command = "$env:USERPROFILE\.local\bin\magic-skill-mcp.bat"
                    env = @{
                        PYTHONPATH = $InstallDir
                    }
                }
            }
        } | ConvertTo-Json -Depth 3
        $mcpConfig | Out-File -FilePath "$cursorDir\mcp.json" -Encoding UTF8
        Write-Success "Cursor MCP 配置完成"
    }
    
    # Claude Desktop
    $claudeDir = "$env:APPDATA\Claude"
    if (Test-Path $claudeDir) {
        Write-Info "检测到 Claude Desktop，配置 MCP..."
        New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null
        $mcpConfig = @{
            mcpServers = @{
                "magic-skills" = @{
                    command = "$env:USERPROFILE\.local\bin\magic-skill-mcp.bat"
                    env = @{
                        PYTHONPATH = $InstallDir
                    }
                }
            }
        } | ConvertTo-Json -Depth 3
        $mcpConfig | Out-File -FilePath "$claudeDir\claude_desktop_config.json" -Encoding UTF8
        Write-Success "Claude Desktop MCP 配置完成"
    }
    
    Write-Info "Kiro IDE 配置已包含在项目 .kiro/ 目录中"
}

function Verify-Installation {
    Write-Info "验证安装..."
    
    Set-Location $InstallDir
    & .\venv\Scripts\Activate.ps1
    
    # 确保 binDir 在 PATH 中
    $binDir = "$env:USERPROFILE\.local\bin"
    if ($env:Path -notlike "*$binDir*") {
        $env:Path = "$env:Path;$binDir"
    }
    
    # 检查命令
    if (Test-Path "$binDir\magic-skill.bat") {
        Write-Success "magic-skill 命令已创建"
        # 测试运行
        try {
            & "$binDir\magic-skill.bat" --version 2>$null
            Write-Success "magic-skill 运行正常"
        } catch {
            Write-Warning "magic-skill 测试运行失败"
        }
    } else {
        Write-Warning "magic-skill 命令未找到"
    }
    
    # 运行快速验证
    if (Test-Path "verify_all.py") {
        python verify_all.py --quick 2>$null
    } else {
        Write-Warning "验证脚本未找到，跳过"
    }
    
    Write-Success "安装验证完成"
}

function Print-Usage {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                    🎉 安装完成!                              ║" -ForegroundColor Green
    Write-Host "║                 Installation Complete!                       ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 安装目录: $InstallDir"
    Write-Host ""
    
    # 检查命令是否可用
    $binDir = "$env:USERPROFILE\.local\bin"
    if (Get-Command magic-skill -ErrorAction SilentlyContinue) {
        Write-Host "✅ magic-skill 命令已就绪" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 立即尝试:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  magic-skill list" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host "⚠️  需要重新加载 PowerShell" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "🔧 请执行以下命令:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  `$env:Path = [Environment]::GetEnvironmentVariable('Path', 'User')" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "然后就可以使用:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  magic-skill list" -ForegroundColor Cyan
        Write-Host ""
    }
    
    Write-Host "📚 常用命令:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  列出所有技能:"
    Write-Host "     magic-skill list" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  执行技能:"
    Write-Host "     magic-skill exec /mgc-java-backend-controller-gen -p '{\"endpoint\":\"/api/users\"}'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  启动 API 服务器:"
    Write-Host "     magic-skill-server" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  启动 MCP 服务器:"
    Write-Host "     magic-skill-mcp" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📖 文档:" -ForegroundColor Yellow
    Write-Host "  - 使用指南: $InstallDir\README.md"
    Write-Host "  - 命令参考: $InstallDir\COMMANDS_REFERENCE.md"
    Write-Host "  - AI Tools 集成: $InstallDir\AI_TOOLS_INTEGRATION.md"
    Write-Host ""
    Write-Host "⚙️  配置:" -ForegroundColor Yellow
    Write-Host "  - 编辑配置文件: $InstallDir\.env"
    Write-Host ""
    Write-Host "💡 提示:" -ForegroundColor Yellow
    Write-Host "  - 在 Kiro/Cursor/Claude Desktop 中输入 /mgc- 查看可用技能"
    Write-Host "  - 使用 /mgc-list 列出所有技能"
    Write-Host "  - 使用 /mgc-help 获取帮助"
    Write-Host ""
}

# 主函数
function Main {
    Print-Banner
    
    Check-System
    Check-Dependencies
    Get-InstallDir
    Clone-Repo
    Setup-Venv
    Install-Dependencies
    Setup-Env
    Create-Launcher
    Setup-AITools
    Verify-Installation
    Print-Usage
}

# 运行主函数
Main
