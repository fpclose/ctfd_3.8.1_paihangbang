#!/bin/bash

###############################################################################
#
# CTFd-Paihangb Plugin 一键安装脚本
#
# 作者: fpclose
# 版本: 1.0.0
# 兼容: CTFd 3.8.1
# 依赖: ctfd-tuandui 插件
#
# 用法: sudo ./install.sh
#
###############################################################################

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

# 打印标题
echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        CTFd-Paihangb Plugin 一键安装脚本                          ║
║                                                                  ║
║        版本: 1.0.0                                               ║
║        作者: fpclose                                             ║
║        兼容: CTFd 3.8.1                                          ║
║        依赖: ctfd-tuandui 插件                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    print_error "请使用 root 权限运行此脚本"
    print_info "使用方法: sudo ./install.sh"
    exit 1
fi

# 设置 CTFd 路径
CTFD_PATH="/opt/CTFd"
PLUGIN_NAME="ctfd-paihangb"
PLUGIN_PATH="$CTFD_PATH/CTFd/plugins/$PLUGIN_NAME"
TUANDUI_PLUGIN_PATH="$CTFD_PATH/CTFd/plugins/ctfd-tuandui"

# 步骤 1: 检查 CTFd 是否存在
print_info "步骤 1/5: 检查 CTFd 安装..."
if [ ! -d "$CTFD_PATH" ]; then
    print_error "CTFd 未安装在 $CTFD_PATH"
    print_info "请修改脚本中的 CTFD_PATH 变量为您的 CTFd 安装路径"
    exit 1
fi
print_success "CTFd 路径: $CTFD_PATH"

# 检查 ctfd-tuandui 插件
print_info "步骤 2/5: 检查 ctfd-tuandui 插件..."
if [ ! -d "$TUANDUI_PLUGIN_PATH" ]; then
    print_error "未找到 ctfd-tuandui 插件！"
    print_info "ctfd-paihangb 插件依赖 ctfd-tuandui 插件提供的团队赛道信息"
    print_info "请先安装 ctfd-tuandui 插件："
    print_info "  https://github.com/fpclose/ctfd_3.8.1_tuandui"
    exit 1
fi
print_success "找到 ctfd-tuandui 插件"

# 检查 CTFd 版本
if [ -f "$CTFD_PATH/CTFd/__init__.py" ]; then
    VERSION=$(grep -oP "__version__\s*=\s*\"\K[^\"]+\" $CTFD_PATH/CTFd/__init__.py || echo "unknown")
    print_info "检测到 CTFd 版本: $VERSION"
fi

# 步骤 3: 安装插件文件
print_info "步骤 3/5: 安装插件文件..."

# 检查插件是否已存在
if [ -d "$PLUGIN_PATH" ]; then
    print_warning "插件目录已存在，将覆盖安装"
    rm -rf "$PLUGIN_PATH"
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 如果当前目录包含插件文件，直接复制
if [ -f "$SCRIPT_DIR/__init__.py" ] && [ -f "$SCRIPT_DIR/config.json" ]; then
    print_info "从当前目录复制插件文件..."
    mkdir -p "$PLUGIN_PATH"
    cp -r "$SCRIPT_DIR"/* "$PLUGIN_PATH/"
    print_success "插件文件已复制"
else
    # 否则尝试从 GitHub 下载
    print_info "从 GitHub 下载插件..."
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    if command -v git &> /dev/null; then
        git clone https://github.com/fpclose/ctfd_3.8.1_paihangb.git
        cp -r ctfd_3.8.1_paihangb "$PLUGIN_PATH"
        print_success "插件已从 GitHub 下载"
    else
        print_error "Git 未安装，无法下载插件"
        print_info "请手动下载插件到: $PLUGIN_PATH"
        exit 1
    fi
    
    cd - > /dev/null
    rm -rf "$TEMP_DIR"
fi

# 步骤 4: 设置权限
print_info "步骤 4/5: 设置文件权限..."
chown -R $(stat -c '%U:%G' "$CTFD_PATH") "$PLUGIN_PATH"
chmod -R 755 "$PLUGIN_PATH"
print_success "权限设置完成"

# 步骤 5: 重启 CTFd
print_info "步骤 5/5: 重启 CTFd 服务..."

# 检查是否使用 Docker
if [ -f "$CTFD_PATH/docker-compose.yml" ]; then
    print_info "检测到 Docker 环境，重启容器..."
    cd "$CTFD_PATH"
    docker compose restart ctfd
    print_success "CTFd 容器已重启"
elif systemctl is-active --quiet ctfd; then
    print_info "检测到 systemd 服务，重启服务..."
    systemctl restart ctfd
    print_success "CTFd 服务已重启"
else
    print_warning "无法自动重启 CTFd，请手动重启"
fi

# 等待服务启动
print_info "等待服务启动..."
sleep 6

# 安装完成
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                  安装完成！                                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

print_success "CTFd-Paihangb 插件安装成功！"
echo ""
print_info "插件安装位置: $PLUGIN_PATH"
echo ""
print_info "功能特性："
echo "  ✅ 四大榜单（总榜、新生榜、进阶榜、社会榜）"
echo "  ✅ 一键切换不同赛道"
echo "  ✅ 学校筛选功能"
echo "  ✅ 实时搜索队伍"
echo "  ✅ 自动刷新数据"
echo "  ✅ 美观的界面设计"
echo ""
print_info "访问排行榜："
echo "  http://your-ctfd-url/scoreboard/custom"
echo ""
print_info "请执行以下操作："
echo "  1. 清除浏览器缓存（Ctrl + F5）"
echo "  2. 访问自定义排行榜页面"
echo "  3. 测试榜单切换功能"
echo "  4. 测试筛选功能"
echo ""
print_info "查看插件日志："
if [ -f "$CTFD_PATH/docker-compose.yml" ]; then
    echo "  docker compose -f $CTFD_PATH/docker-compose.yml logs ctfd | grep 'ctfd-paihangb'"
else
    echo "  journalctl -u ctfd | grep 'ctfd-paihangb'"
fi
echo ""
print_info "如有问题，请查看 README.md 或访问："
echo "  https://github.com/fpclose/ctfd_3.8.1_paihangb"
echo ""

# 显示检查结果
print_info "正在检查插件加载状态..."

if [ -f "$CTFD_PATH/docker-compose.yml" ]; then
    LOGS=$(docker compose -f "$CTFD_PATH/docker-compose.yml" logs ctfd --tail=50 2>/dev/null | grep "ctfd-paihangb" || true)
else
    LOGS=$(journalctl -u ctfd --no-pager -n 50 2>/dev/null | grep "ctfd-paihangb" || true)
fi

if echo "$LOGS" | grep -q "插件加载成功"; then
    print_success "✅ 插件已成功加载！"
    echo "$LOGS" | grep "ctfd-paihangb"
else
    print_warning "⚠️  未检测到插件加载日志，请手动检查"
fi

echo ""
print_success "安装脚本执行完毕！"

exit 0

