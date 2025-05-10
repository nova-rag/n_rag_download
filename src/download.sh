#!/bin/bash

# 设置脚本终止时执行的命令
trap "echo '已中断'; exit 1" INT TERM

# 默认参数
URL_FILE="resource_list.txt"
OUTPUT_DIR="downloads"
VERBOSE=""
SKIP_EXISTING="--skip-existing"
DELAY="1"
NO_GIT_CLONE=""
USE_CSV=""
CATEGORY=""
GENERATE_JSON=true

# 显示帮助信息
show_help() {
    echo "用法: ./download.sh [选项]"
    echo "选项:"
    echo "  -h, --help            显示帮助信息"
    echo "  -v, --verbose         显示详细输出"
    echo "  -f, --file <文件名>     指定资源文件 (默认: resource_list.txt)"
    echo "  -o, --output <目录>     指定下载目录 (默认: downloads)"
    echo "  -d, --delay <秒>       设置下载间隔 (默认: 1秒)"
    echo "  -r, --random-delay     使用随机延迟 (1-5秒)"
    echo "  --no-skip             不跳过已下载文件"
    echo "  --no-git-clone         不使用git clone下载GitHub仓库"
    echo "  --use-csv             强制使用CSV格式解析资源文件"
    echo "  -c, --category <分类>   只下载指定分类的资源"
    echo "  --no-json             不生成资源信息JSON文件"
    echo ""
    echo "可用的资源分类:"
    echo "  公开芯片SDK"
    echo "  FreeRTOS文档"
    echo "  RISC-V框架相关文档" 
    echo "  UWB的Rifa标准文档"
    echo "  其他行业相关文档"
    echo "  一些领域相关paper"
    echo ""
    echo "示例:"
    echo "  ./download.sh -v                  # 详细模式下载"
    echo "  ./download.sh -f resources.csv    # 使用CSV格式资源文件"
    echo "  ./download.sh -o custom_dir       # 下载到自定义目录"
    echo "  ./download.sh -d 2                # 设置下载间隔为2秒"
    echo "  ./download.sh -r                  # 使用随机延迟"
    echo "  ./download.sh -c '公开芯片SDK'     # 只下载公开芯片SDK分类的资源"
    exit 0
}

# 解析命令行参数
RANDOM_DELAY=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -f|--file)
            URL_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -d|--delay)
            DELAY="$2"
            shift 2
            ;;
        -r|--random-delay)
            RANDOM_DELAY="--random-delay"
            shift
            ;;
        --no-skip)
            SKIP_EXISTING=""
            shift
            ;;
        --no-git-clone)
            NO_GIT_CLONE="--no-git-clone"
            shift
            ;;
        --use-csv)
            USE_CSV="--use-csv"
            shift
            ;;
        --no-json)
            GENERATE_JSON=false
            shift
            ;;
        -c|--category)
            CATEGORY="--category"
            shift
            if [[ $# -eq 0 ]]; then
                echo "错误: --category 选项需要一个参数"
                exit 1
            fi
            CATEGORY_NAME="$1"
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

# 检查资源文件
if [ ! -f "data/$URL_FILE" ]; then
    echo "错误: 资源文件 'data/$URL_FILE' 不存在"
    exit 1
fi

# 如果使用CSV文件，确保设置--use-csv选项
if [[ "$URL_FILE" == *.csv ]]; then
    USE_CSV="--use-csv"
fi

# 确保下载目录存在
mkdir -p "data/$OUTPUT_DIR"

# 运行下载脚本
echo "开始下载资源..."
if [ -n "$CATEGORY" ]; then
    python3 src/download_resources.py \
        --url-file "$URL_FILE" \
        --output-dir "$OUTPUT_DIR" \
        --delay "$DELAY" \
        $RANDOM_DELAY \
        $SKIP_EXISTING \
        $VERBOSE \
        $NO_GIT_CLONE \
        $USE_CSV \
        --category "$CATEGORY_NAME"
else
    python3 src/download_resources.py \
        --url-file "$URL_FILE" \
        --output-dir "$OUTPUT_DIR" \
        --delay "$DELAY" \
        $RANDOM_DELAY \
        $SKIP_EXISTING \
        $VERBOSE \
        $NO_GIT_CLONE \
        $USE_CSV
fi

# 检查运行结果
DOWNLOAD_EXIT_CODE=$?
if [ $DOWNLOAD_EXIT_CODE -eq 0 ]; then
    echo "下载完成!"
    
    # 如果启用了JSON生成，生成资源信息JSON文件
    if [ "$GENERATE_JSON" = true ]; then
        echo ""
        echo "正在生成资源信息JSON文件..."
        python3 src/generate_resource_json.py
        
        if [ $? -eq 0 ]; then
            echo "资源信息JSON文件生成完成!"
        else
            echo "资源信息JSON文件生成失败!"
        fi
    fi
    
    exit 0
else
    echo "下载过程中发生错误，退出代码: $DOWNLOAD_EXIT_CODE"
    exit 1
fi 