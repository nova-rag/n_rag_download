#!/bin/bash
# 资源自动下载脚本

# 基础配置
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RESOURCE_FILE="${ROOT_DIR}/data/resources.csv"  # 默认资源列表文件
DOWNLOAD_DIR="${ROOT_DIR}/data/downloads"          # 下载目录
DOWNLOAD_SCRIPT="${ROOT_DIR}/src/download_resources.py"  # 下载资源的Python脚本
VERBOSE=false                        # 是否显示详细输出
JSON_FILE="${ROOT_DIR}/data/downloaded_resources_info.json" # 资源信息JSON文件
SKIP_EXISTING="--skip-existing"      # 默认跳过已下载文件
DELAY="1"                           # 默认下载间隔（秒）
USE_GIT_CLONE=true                  # 是否使用Git克隆GitHub仓库
GENERATE_JSON=true                  # 是否生成资源信息JSON
CATEGORY=""                         # 资源分类筛选
RESOURCE_TYPE=""                    # 资源类型筛选
INDEX=""                            # 资源索引筛选

# 设置脚本终止时执行的命令
trap cleanup EXIT

# 清理函数
cleanup() {
    echo -e "\n完成。请检查下载目录: $DOWNLOAD_DIR"
}

# 显示帮助信息
show_help() {
    echo "资源自动下载脚本"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help             显示此帮助信息"
    echo "  -v, --verbose          显示详细输出"
    echo "  -f, --file <文件名>     指定资源文件 (默认: ${RESOURCE_FILE})"
    echo "  -o, --output <目录>     指定下载目录 (默认: ${DOWNLOAD_DIR})"
    echo "  -d, --delay <秒>        设置下载间隔 (默认: ${DELAY}秒)"
    echo "  -r, --random-delay      使用随机延迟 (1-5秒)"
    echo "  --no-skip               不跳过已下载文件"
    echo "  --no-json               不生成资源信息JSON文件"
    echo "  --no-git-clone          不使用git clone下载GitHub仓库"
    echo "  -c, --category <分类>    只下载指定分类的资源"
    echo "  -t, --type <类型>        按资源类型下载资源"
    echo "  -i, --index <索引>       按索引下载资源 (例如: \"1-5,10,15-20\")"
    echo ""
    echo "示例:"
    echo "  $0 -v                                 # 详细模式下载"
    echo "  $0 -d 2                               # 设置下载间隔为2秒"
    echo "  $0 -r                                 # 使用随机延迟"
    echo "  $0 -c \"公开芯片SDK\"                    # 只下载公开芯片SDK分类的资源"
    echo "  $0 -t \"PDF\" -c \"RISC-V框架相关文档\"    # 下载RISC-V分类的PDF文件"
    echo "  $0 -i \"1-5,10\"                       # 只下载索引为1到5和10的资源"
}

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -f|--file)
                RESOURCE_FILE="$2"
                shift 2
                ;;
            -o|--output)
                DOWNLOAD_DIR="$2"
                shift 2
                ;;
            -d|--delay)
                DELAY="$2"
                shift 2
                ;;
            -r|--random-delay)
                DELAY="random"
                shift
                ;;
            --no-skip)
                SKIP_EXISTING=""
                shift
                ;;
            --no-json)
                GENERATE_JSON=false
                shift
                ;;
            --no-git-clone)
                USE_GIT_CLONE=false
                shift
                ;;
            -c|--category)
                CATEGORY="$2"
                shift 2
                ;;
            -t|--type)
                RESOURCE_TYPE="$2"
                shift 2
                ;;
            -i|--index)
                INDEX="$2"
                shift 2
                ;;
            *)
                echo "错误: 未知选项 $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 检查依赖
check_dependencies() {
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "错误: 需要Python 3，但未找到。请安装Python 3后再试。"
        exit 1
    fi

    # 检查必要的Python库
    if ! python3 -c "import requests" &> /dev/null; then
        echo "错误: 缺少Python库 'requests'。请运行 'pip install requests' 安装。"
        exit 1
    fi

    # 检查Git（如果需要使用git clone）
    if $USE_GIT_CLONE && ! command -v git &> /dev/null; then
        echo "警告: 需要使用Git克隆GitHub仓库，但未找到Git。将只下载GitHub页面内容而不是克隆仓库。"
        USE_GIT_CLONE=false
    fi
}

# 准备下载目录
prepare_download_dir() {
    # 创建下载目录（如果不存在）
    if [ ! -d "$DOWNLOAD_DIR" ]; then
        mkdir -p "$DOWNLOAD_DIR"
        echo "创建下载目录: $DOWNLOAD_DIR"
    fi
}

# 执行下载
execute_download() {
    local cmd_args=()

    # 添加基本参数
    cmd_args+=("$DOWNLOAD_SCRIPT" "$RESOURCE_FILE" "$DOWNLOAD_DIR")

    # 添加可选参数
    if $VERBOSE; then
        cmd_args+=("--verbose")
    fi

    if [ -n "$SKIP_EXISTING" ]; then
        cmd_args+=("$SKIP_EXISTING")
    fi

    if [ "$DELAY" == "random" ]; then
        cmd_args+=("--random-delay")
    else
        cmd_args+=("--delay" "$DELAY")
    fi

    # 添加分类筛选
    if [ -n "$CATEGORY" ]; then
        cmd_args+=("--category" "$CATEGORY")
    fi

    # 添加类型筛选
    if [ -n "$RESOURCE_TYPE" ]; then
        cmd_args+=("--type" "$RESOURCE_TYPE")
    fi

    # 添加索引筛选
    if [ -n "$INDEX" ]; then
        cmd_args+=("--index" "$INDEX")
    fi

    # Git克隆选项
    if ! $USE_GIT_CLONE; then
        cmd_args+=("--no-git-clone")
    fi

    # 执行下载命令
    if $VERBOSE; then
        echo "执行命令: python3 ${cmd_args[*]}"
    fi

    python3 "${cmd_args[@]}"
    return $?
}

# 生成资源信息JSON文件
generate_resource_json() {
    if ! $GENERATE_JSON; then
        return 0
    fi

    echo "正在生成资源信息JSON文件..."
    python3 "${ROOT_DIR}/src/generate_resource_json.py"
    return $?
}

# 主函数
main() {
    # 解析命令行参数
    parse_args "$@"

    # 检查依赖
    check_dependencies

    # 准备下载目录
    prepare_download_dir

    # 执行下载
    echo "正在从 $RESOURCE_FILE 下载资源到 $DOWNLOAD_DIR..."
    if execute_download; then
        echo "下载完成!"
        
        # 生成资源信息JSON文件
        generate_resource_json
    else
        echo "下载过程中发生错误。"
        exit 1
    fi
}

# 执行主函数
main "$@" 