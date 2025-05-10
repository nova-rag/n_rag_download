#!/bin/bash
# 资源清理脚本

# 基础配置
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DOWNLOAD_DIR="${ROOT_DIR}/data/downloads"          # 下载目录
CLEANED_DIR="${ROOT_DIR}/data/cleaned_data"        # 清理后文件存放目录
CLEAN_SCRIPT="${ROOT_DIR}/src/clean_data.py"       # 清理资源的Python脚本
JSON_SCRIPT="${ROOT_DIR}/src/generate_resource_json.py" # 生成JSON的Python脚本
VERBOSE=false                          # 是否显示详细输出
FORCE=false                            # 是否强制重新清理所有文件
GIT_MODE="copy"                        # Git仓库处理方式
GENERATE_JSON=true                     # 是否生成资源信息JSON文件

# 清理函数
cleanup() {
    echo -e "\n完成。清理后的数据位于: $CLEANED_DIR"
}

# 设置脚本终止时执行的命令
trap cleanup EXIT

# 显示帮助信息
show_help() {
    echo "资源清理脚本"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help            显示此帮助信息"
    echo "  -v, --verbose         显示详细输出"
    echo "  -i, --input <目录>     指定输入目录 (默认: ${DOWNLOAD_DIR})"
    echo "  -o, --output <目录>    指定输出目录 (默认: ${CLEANED_DIR})"
    echo "  -f, --force           强制重新清理所有文件"
    echo "  -g, --git <mode>      指定Git仓库处理方式 (默认: ${GIT_MODE})"
    echo "                        可选值: copy (复制整个仓库), skip (跳过Git仓库), readme_only (只提取README)"
    echo "  --no-json             不生成资源信息JSON文件"
    echo ""
    echo "示例:"
    echo "  $0 -v                 # 详细模式清理"
    echo "  $0 -f                 # 强制重新清理所有文件"
    echo "  $0 -g readme_only     # 只提取Git仓库中的README文件"
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
            -i|--input)
                DOWNLOAD_DIR="$2"
                shift 2
                ;;
            -o|--output)
                CLEANED_DIR="$2"
                shift 2
                ;;
            -f|--force)
                FORCE=true
                shift
                ;;
            -g|--git)
                GIT_MODE="$2"
                shift 2
                ;;
            --no-json)
                GENERATE_JSON=false
                shift
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
    if ! python3 -c "import bs4" &> /dev/null; then
        echo "错误: 缺少Python库 'beautifulsoup4'。请运行 'pip install beautifulsoup4' 安装。"
        exit 1
    fi
}

# 准备目录
prepare_directories() {
    # 检查下载目录是否存在
    if [ ! -d "$DOWNLOAD_DIR" ]; then
        echo "错误: 下载目录 $DOWNLOAD_DIR 不存在"
        exit 1
    fi

    # 创建清理后的数据目录
    mkdir -p "$CLEANED_DIR"
}

# 执行清理
execute_clean() {
    echo "正在清理数据..."
    
    # 更新命令参数，与src/clean_data.py脚本匹配
    local cmd_args=("$CLEAN_SCRIPT" "--clean-dir" "$(basename "$CLEANED_DIR")")
    
    if $VERBOSE; then
        cmd_args+=("--verbose")
    fi
    
    if $FORCE; then
        cmd_args+=("--force")
    fi
    
    cmd_args+=("--handle-git" "$GIT_MODE")
    
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
    python3 "$JSON_SCRIPT"
    return $?
}

# 主函数
main() {
    # 解析命令行参数
    parse_args "$@"
    
    # 检查依赖
    check_dependencies
    
    # 准备目录
    prepare_directories
    
    # 执行清理
    if execute_clean; then
        echo "清理完成!"
        
        # 生成资源信息JSON文件
        if $GENERATE_JSON; then
            generate_resource_json
        fi
    else
        echo "清理过程中发生错误。"
        exit 1
    fi
}

# 执行主函数
main "$@" 