#!/bin/bash
# 推送项目到GitHub仓库

# 检查是否已安装git
if ! command -v git &> /dev/null; then
    echo "错误: 未安装git，请先安装git工具"
    exit 1
fi

# 指定GitHub仓库URL
REPO_URL="https://github.com/joytianya/n_rag_download.git"

# 初始化git仓库
echo "初始化git仓库..."
git init

# 添加所有文件到git仓库
echo "添加文件到git仓库..."
git add .

# 排除不需要提交的文件
echo "创建.gitignore文件..."
cat > .gitignore << EOL
.DS_Store
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.env
.venv
env/
venv/
ENV/
.idea/
.vscode/
data/downloads/*
data/cleaned_data/*
!data/downloads/.gitkeep
!data/cleaned_data/.gitkeep
EOL

# 确保数据目录存在并添加.gitkeep文件
mkdir -p data/downloads data/cleaned_data
touch data/downloads/.gitkeep data/cleaned_data/.gitkeep

# 再次添加文件（包括新创建的.gitignore）
git add .

# 提交更改
echo "提交更改..."
git commit -m "初始提交：资源下载与清理系统"

# 添加远程仓库
echo "添加远程仓库..."
git remote add origin $REPO_URL

# 推送到GitHub
echo "推送到GitHub..."
echo "正在推送代码到 $REPO_URL..."
git push -u origin master

# 检查结果
if [ $? -eq 0 ]; then
    echo "✅ 成功推送项目到GitHub仓库：$REPO_URL"
    echo "可以通过以下网址访问：${REPO_URL%.git}"
else
    echo "❌ 推送失败，请检查以下问题："
    echo "1. 是否有权限访问该仓库"
    echo "2. 仓库URL是否正确"
    echo "3. 是否已设置好GitHub身份验证"
    echo ""
    echo "如果是身份验证问题，请尝试："
    echo "git config --global user.name \"你的GitHub用户名\""
    echo "git config --global user.email \"你的邮箱\""
    echo "然后再次运行此脚本，或使用以下命令手动推送："
    echo "git push -u origin master"
fi 