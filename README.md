# 资源自动下载和清理工具

这是一个用于自动下载和清理资源的工具集，支持从URL列表下载资源，清理HTML和其他文本文件，以及克隆GitHub仓库。

## 功能特点

- 从文本文件或CSV文件中读取资源列表并下载资源
- 支持在CSV中指定自定义文件名和资源类型
- 支持对资源进行分类，并可按分类筛选下载
- 自动生成下载资源信息的JSON文件，便于程序处理和查询
- 支持检测GitHub仓库链接并自动使用git clone下载
- 清理HTML文件，提取纯文本内容
- 处理目录中的PDF文件，生成带有清理路径的格式化JSON信息
- 支持处理多种文件类型（HTML、RST、PDF、Markdown等）
- 可自定义下载延迟，减轻对目标服务器的压力
- 显示下载进度和统计信息
- 支持多种模式处理Git仓库（完整复制、只提取README或跳过）
- 使用`--use-csv` 参数强制按CSV格式处理
- 使用`--no-json` 参数禁止生成JSON资源信息文件
- `--no-skip` - 不跳过已下载文件
- `--no-json` - 不生成资源信息JSON文件
- 可以使用 `-c, --category` 参数只下载特定分类的资源
- 下载完成后会自动生成 `data/downloaded_resources_info.json` 文件，仅包含成功下载的资源信息
- 支持生成 `data/format_data_info.json` 文件，包含清理路径和PDF文件信息

## 准备工作

1. 确保已安装Python 3.6+
2. 安装必要的Python库：
   ```bash
   pip install requests beautifulsoup4 tqdm
   ```
3. 如需使用Git克隆功能，请确保已安装Git：
   ```bash
   # Ubuntu/Debian
   sudo apt-get install git
   
   # CentOS/RHEL
   sudo yum install git
   
   # macOS (使用Homebrew)
   brew install git
   
   # Windows
   # 从 https://git-scm.com/download/win 下载安装程序
   ```

## 快速开始

1. 准备资源列表文件：
   - 在`data/resources.csv`中列出需要下载的资源，格式为 URL,文件名,资源类型,来源,分类
   
2. 使用管理脚本执行所有操作：
   ```bash
   ./scripts/manage.sh all
   ```
   
   或者逐步执行：
   ```bash
   # 下载资源
   ./scripts/manage.sh download
   
   # 清理数据
   ./scripts/manage.sh clean
   
   # 生成资源信息JSON
   ./scripts/manage.sh json
   
   # 生成格式化JSON（带清理路径）
   ./scripts/manage.sh format
   ```

## 详细使用说明

### 使用管理脚本

为了方便使用，我们提供了一个统一的管理脚本，可以执行所有操作：

```bash
./scripts/manage.sh [命令] [选项]
```

可用命令：
- `download` 或 `d`: 下载资源
- `clean` 或 `c`: 清理数据
- `json` 或 `j`: 生成资源信息JSON文件
- `format` 或 `f`: 生成带清理路径的格式化JSON文件
- `all` 或 `a`: 执行所有操作（下载 -> 清理 -> 生成JSON -> 格式化JSON）
- `help` 或 `h`: 显示帮助信息

例如：
```bash
# 下载特定分类的资源
./scripts/manage.sh download -c "公开芯片SDK"

# 执行所有操作
./scripts/manage.sh all

# 只生成JSON文件
./scripts/manage.sh json

# 生成带清理路径的格式化JSON文件
./scripts/manage.sh format
```

### 下载资源

资源列表文件存放在 `data/resources.csv`，包含URL、文件名、资源类型、来源和分类信息。运行以下命令下载所有资源：

```bash
./scripts/manage.sh download
```

您可以使用以下选项进行更精确的下载控制：

- `-c, --category <分类>`: 按分类下载资源，例如 "公开芯片SDK", "FreeRTOS文档", "RISC-V框架相关文档" 等
- `-t, --type <类型>`: 按资源类型下载资源，例如 "PDF", "HTML", "GitHub" 等
- `-i, --index <索引>`: 按索引下载资源，例如 "1-5", "10,15,20" 等
- `--no-git-clone`: 禁用GitHub仓库克隆功能，仅下载页面内容

例如，只下载与FreeRTOS相关的文档：

```bash
./scripts/manage.sh download -c "FreeRTOS文档"
```

### 清理数据

下载完成后，可以运行清理脚本处理下载的文件，提取纯文本内容：

```bash
./scripts/manage.sh clean
```

清理后的文件将存放在 `data/cleaned_data` 目录中，纯文本内容可以更方便地用于后续处理。

### 生成资源信息JSON文件

下载完成后，可以生成一个包含所有成功下载资源的路径信息的JSON文件，方便后续处理：

```bash
./scripts/manage.sh json
```

生成的JSON文件默认保存为 `data/downloaded_resources_info.json`，包含每个成功下载资源的URL、文件名、类型、来源、分类和本地下载路径信息。

支持的命令行选项：

- `--csv, -c <CSV文件路径>`: 指定资源列表CSV文件路径，默认使用 `data/resources.csv`
- `--output, -o <输出文件路径>`: 指定输出JSON文件路径，默认为 `data/downloaded_resources_info.json`

### 生成格式化JSON文件

在生成基础资源信息JSON文件后，可以进一步处理生成带有清理路径的格式化JSON文件：

```bash
./scripts/manage.sh format
```

这个命令会：
1. 读取 `data/downloaded_resources_info.json` 文件中的资源信息
2. 添加 `clean_path` 字段，指向 `data/cleaned_data` 目录下的文件
3. 对于目录类型的资源（如GitHub仓库），会:
   - 查找目录中的所有有价值的文件（PDF、JSON、CSV、MD等）
   - 复制这些文件到 `data/cleaned_data/{仓库名}/` 目录下
   - 为每个文件创建一个独立的资源条目，并添加`file_type`字段标识文件类型
4. 最终生成 `data/format_data_info.json` 文件

支持的命令行选项：
- `--input, -i <输入JSON文件路径>`: 指定输入JSON文件路径，默认为 `data/downloaded_resources_info.json`
- `--output, -o <输出JSON文件路径>`: 指定输出JSON文件路径，默认为 `data/format_data_info.json`
- `--verbose, -v`: 显示详细处理信息
- `--extensions, -e <扩展名列表>`: 指定要包含的文件扩展名，用逗号分隔，例如：`pdf,json,md`

支持的文件类型：
- PDF文档 (`.pdf`)
- JSON文件 (`.json`)
- CSV文件 (`.csv`)
- Markdown文件 (`.md`)
- 纯文本文件 (`.txt`)
- ReStructuredText文件 (`.rst`)
- YAML文件 (`.yaml`, `.yml`)
- XML文件 (`.xml`)
- HTML文件 (`.html`, `.htm`)
- Word文档 (`.doc`, `.docx`)
- Excel文件 (`.xls`, `.xlsx`)
- PowerPoint文件 (`.ppt`, `.pptx`)

示例：
```bash
# 只处理PDF和Markdown文件
./scripts/manage.sh format -e pdf,md

# 详细模式处理所有支持的文件类型
./scripts/manage.sh format -v

# 指定输入输出文件并只处理JSON和CSV文件
./scripts/manage.sh format -i data/custom_resources.json -o data/custom_format.json -e json,csv
```

### 统计信息

运行以下命令可以查看数据统计信息：

```bash
python3 src/stats.py
```

## 资源信息JSON文件

下载完成后会自动生成 `data/downloaded_resources_info.json` 文件，仅包含成功下载的资源信息：

```json
[
  {
    "url": "资源URL",
    "filename": "资源名称",
    "resource_type": "资源类型(HTML、PDF、GitHub等)",
    "source": "资源来源",
    "category": "资源分类",
    "path": "下载后的文件路径"
  },
  ...
]
```

这个JSON文件可以用于：
- 在其他程序中查询资源信息
- 追踪已下载的文件
- 按分类统计资源数量
- 生成资源索引等

## 格式化数据JSON文件

执行format命令后会生成 `data/format_data_info.json` 文件，它在基础的资源信息基础上增加了 `clean_path` 和 `file_type` 字段，并对GitHub仓库中的各类文件进行了处理：

```json
[
  {
    "url": "资源URL",
    "filename": "资源名称",
    "resource_type": "资源类型(HTML、PDF、GitHub等)",
    "source": "资源来源",
    "category": "资源分类",
    "path": "下载后的文件路径",
    "clean_path": "清理后的文件路径",
    "file_type": "文件类型描述"
  },
  ...
]
```

对于GitHub仓库中的文件，会为每个找到的文件创建一个独立的条目，例如：

```json
{
  "url": "https://github.com/user/repo",
  "filename": "repo名称 - example.pdf",
  "resource_type": "GitHub",
  "source": "GitHub",
  "category": "某分类",
  "path": "data/downloads/repo",
  "clean_path": "data/cleaned_data/repo/example.pdf",
  "file_type": "PDF文档"
}
```

这个格式化的JSON文件特别适合以下场景：
- 需要处理GitHub仓库中的多种文件格式
- 需要知道每个资源的清理后路径和文件类型
- 需要将文档进行标准化处理供后续程序使用

## 贡献

欢迎提交 Pull Request 或 Issue 来改进本项目。

## 注意事项

- 请确保遵守网站的使用条款和robots.txt规则
- 适当设置下载延迟，避免对目标服务器造成过大压力
- 对于GitHub仓库，使用`--depth 1`参数只克隆最新版本，减少下载量
- 清理后的HTML文件可能不包含原始格式和图像等多媒体内容

## 许可证

[MIT](LICENSE) 