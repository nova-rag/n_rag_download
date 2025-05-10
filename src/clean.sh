#!/bin/bash

# 设置脚本终止时执行的命令
trap "echo '已中断'; exit 1" INT TERM

# 默认参数
INPUT_DIR="downloads"
OUTPUT_DIR="cleaned_data"
VERBOSE=""
FORCE=""
GIT_MODE="copy"
GENERATE_JSON=true

# 显示帮助信息
show_help() {
    echo "用法: ./clean.sh [选项]"
    echo "选项:"
    echo "  -h, --help            显示帮助信息"
    echo "  -v, --verbose         显示详细输出"
    echo "  -i, --input <目录>     指定输入目录 (默认: downloads)"
    echo "  -o, --output <目录>    指定输出目录 (默认: cleaned_data)"
    echo "  -f, --force           强制重新清理所有文件"
    echo "  -g, --git <模式>       指定Git仓库处理方式 (默认: copy)"
    echo "                        可选值: copy, skip, readme_only"
    echo "  --no-json             不生成资源信息JSON文件"
    echo ""
    echo "示例:"
    echo "  ./clean.sh -v                   # 详细模式清理"
    echo "  ./clean.sh -f                   # 强制重新清理所有文件"
    echo "  ./clean.sh -i raw -o processed  # 指定输入和输出目录"
    echo "  ./clean.sh -g readme_only       # 只提取Git仓库中的README文件"
    exit 0
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -i|--input)
            INPUT_DIR="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -f|--force)
            FORCE="--force"
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
            echo "未知选项: $1"
            show_help
            ;;
    esac
done

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3。请安装Python3后再试。"
    exit 1
fi

# 检查必要的库
python3 -c "import bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装必要的Python库..."
    pip3 install beautifulsoup4 tqdm
fi

# 检查下载日志文件
if [ ! -f "data/download_log.json" ]; then
    echo "错误: 未找到下载日志文件。请先运行下载脚本。"
    exit 1
fi

# 确保清理目录存在
mkdir -p "data/$OUTPUT_DIR"

# 运行清理脚本
echo "开始清理数据..."
python3 src/clean_data.py \
    --input-dir "data/$INPUT_DIR" \
    --output-dir "data/$OUTPUT_DIR" \
    --git-mode "$GIT_MODE" \
    $VERBOSE \
    $FORCE

# 检查运行结果
CLEAN_EXIT_CODE=$?
if [ $CLEAN_EXIT_CODE -eq 0 ]; then
    echo "清理完成!"
    
    # 如果启用了JSON生成，更新资源信息JSON文件
    if [ "$GENERATE_JSON" = true ]; then
        echo ""
        echo "正在更新资源信息JSON文件..."
        python3 src/generate_resource_json.py
        
        if [ $? -eq 0 ]; then
            echo "资源信息JSON文件更新完成!"
        else
            echo "资源信息JSON文件更新失败!"
        fi
    fi
    
    exit 0
else
    echo "清理过程中发生错误，退出代码: $CLEAN_EXIT_CODE"
    exit 1
fi 