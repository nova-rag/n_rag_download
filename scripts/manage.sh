#!/bin/bash
# 资源管理脚本 - 用于下载、清理资源和生成资源信息

# 项目根目录
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DOWNLOAD_SCRIPT="${ROOT_DIR}/scripts/download.sh"
CLEAN_SCRIPT="${ROOT_DIR}/scripts/clean.sh"
JSON_SCRIPT="${ROOT_DIR}/src/generate_resource_json.py"
FORMAT_SCRIPT="${ROOT_DIR}/src/generate_format_json.py"

# 显示帮助信息
show_help() {
    echo "资源管理脚本 - 用于下载、清理资源和生成资源信息"
    echo ""
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  download      下载资源"
    echo "  clean         清理数据"
    echo "  json          生成资源信息JSON文件"
    echo "  format        生成带清理路径的格式化JSON文件"
    echo "  all           执行所有操作 (下载 -> 清理 -> 生成JSON -> 格式化JSON)"
    echo "  help          显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 download -c \"公开芯片SDK\"    # 下载特定分类的资源"
    echo "  $0 clean                      # 清理下载的数据"
    echo "  $0 json                       # 生成资源信息JSON文件"
    echo "  $0 format                     # 生成带清理路径的格式化JSON文件"
    echo "  $0 all                        # 执行所有操作"
    echo ""
    echo "要查看每个命令的具体选项，请使用:"
    echo "  $0 [命令] --help"
}

# 检查脚本是否存在
check_scripts() {
    if [ ! -f "$DOWNLOAD_SCRIPT" ]; then
        echo "错误: 下载脚本不存在: $DOWNLOAD_SCRIPT"
        exit 1
    fi
    if [ ! -f "$CLEAN_SCRIPT" ]; then
        echo "错误: 清理脚本不存在: $CLEAN_SCRIPT"
        exit 1
    fi
    if [ ! -f "$JSON_SCRIPT" ]; then
        echo "错误: JSON生成脚本不存在: $JSON_SCRIPT"
        exit 1
    fi
    if [ ! -f "$FORMAT_SCRIPT" ]; then
        echo "警告: 格式化JSON生成脚本不存在: $FORMAT_SCRIPT"
    fi
}

# 确保脚本可执行
ensure_executable() {
    chmod +x "$DOWNLOAD_SCRIPT" 2>/dev/null || true
    chmod +x "$CLEAN_SCRIPT" 2>/dev/null || true
}

# 下载资源
download_resources() {
    echo "执行下载操作..."
    "$DOWNLOAD_SCRIPT" "$@"
    return $?
}

# 清理数据
clean_data() {
    echo "执行清理操作..."
    "$CLEAN_SCRIPT" "$@"
    return $?
}

# 生成JSON
generate_json() {
    echo "生成资源信息JSON文件..."
    python3 "$JSON_SCRIPT" "$@"
    return $?
}

# 生成格式化JSON
generate_format_json() {
    echo "生成带清理路径的格式化JSON文件..."
    if [ -f "$FORMAT_SCRIPT" ]; then
        python3 "$FORMAT_SCRIPT" "$@"
        return $?
    else
        echo "错误: 格式化JSON生成脚本不存在: $FORMAT_SCRIPT"
        return 1
    fi
}

# 执行所有操作
do_all() {
    echo "执行所有操作..."
    
    # 只将下载参数传递给下载脚本
    if download_resources "$@"; then
        echo "✓ 下载完成"
        
        # 清理和生成JSON不需要额外参数
        if clean_data; then
            echo "✓ 清理完成"
            
            if generate_json; then
                echo "✓ 生成资源信息JSON完成"
                
                if generate_format_json; then
                    echo "✓ 生成格式化JSON完成"
                    echo "✓✓ 全部操作已成功完成！"
                    return 0
                else
                    echo "✗ 生成格式化JSON失败"
                    return 1
                fi
            else
                echo "✗ 生成资源信息JSON失败"
                return 1
            fi
        else
            echo "✗ 清理操作失败"
            return 1
        fi
    else
        echo "✗ 下载操作失败"
        return 1
    fi
}

# 主函数
main() {
    # 检查脚本是否存在
    check_scripts
    
    # 确保脚本可执行
    ensure_executable
    
    # 解析命令
    case "$1" in
        download|d)
            shift
            download_resources "$@"
            ;;
        clean|c)
            shift
            clean_data "$@"
            ;;
        json|j)
            shift
            generate_json "$@"
            ;;
        format|f)
            shift
            generate_format_json "$@"
            ;;
        all|a)
            shift
            do_all "$@"
            ;;
        help|h|--help|-h)
            show_help
            ;;
        *)
            # 如果没有提供命令或提供的命令无效，显示帮助
            show_help
            exit 1
            ;;
    esac
    
    exit $?
}

# 执行主函数
main "$@" 