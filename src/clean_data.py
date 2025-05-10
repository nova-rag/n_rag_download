#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import shutil
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import traceback

# 解析命令行参数
parser = argparse.ArgumentParser(description='清理下载的资源文件，提取纯文本内容')
parser.add_argument('--clean-dir', default='cleaned_data', help='清理后的文件存放目录')
parser.add_argument('--verbose', action='store_true', help='显示详细输出')
parser.add_argument('--force', action='store_true', help='强制重新清理所有文件')
parser.add_argument('--handle-git', default='copy', choices=['copy', 'skip', 'readme_only'], 
                    help='处理Git仓库的方式: copy=复制整个仓库, skip=跳过, readme_only=只提取README')
args = parser.parse_args()

# 配置
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "data/downloads")
CLEAN_DIR = os.path.join(ROOT_DIR, "data", args.clean_dir)
LOG_FILE = os.path.join(ROOT_DIR, "data/download_log.json")
CLEAN_LOG_FILE = os.path.join(ROOT_DIR, "data/clean_log.json")

# 需要清理的文件类型
HTML_LIKE_EXTENSIONS = ['.html', '.htm', '.4', '.rst', '.4']

# 需要复制的文件类型
COPY_EXTENSIONS = ['.pdf', '.md', '.txt']

# Git仓库标记
GIT_REPO_SUFFIX = "_git"

# 确保清理目录存在
os.makedirs(CLEAN_DIR, exist_ok=True)

def load_log():
    """加载下载日志"""
    if not os.path.exists(LOG_FILE):
        print("错误: 下载日志文件不存在，请先运行下载程序")
        return None
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"无法读取日志文件: {e}")
        return None

def load_clean_log():
    """加载清理日志"""
    if not os.path.exists(CLEAN_LOG_FILE):
        return {"cleaned_files": []}
    
    try:
        with open(CLEAN_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"cleaned_files": []}

def save_clean_log(cleaned_files):
    """保存清理日志"""
    log_data = {
        "cleaned_files": cleaned_files
    }
    
    with open(CLEAN_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def clean_html(html_content):
    """清理HTML内容，只保留文本"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除所有脚本和样式
        for script in soup(["script", "style"]):
            script.extract()
        
        # 获取文本
        text = soup.get_text()
        
        # 处理多余的空白
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"清理HTML失败: {e}")
        return html_content

def clean_text_file(content):
    """清理文本文件，移除多余的空白"""
    try:
        # 处理多余的空白
        lines = (line.strip() for line in content.splitlines())
        text = '\n'.join(line for line in lines if line)
        return text
    except Exception as e:
        print(f"清理文本失败: {e}")
        return content

def is_git_repo(filename):
    """判断文件是否是Git仓库"""
    return filename.endswith(GIT_REPO_SUFFIX)

def extract_readme_from_repo(repo_path, target_path):
    """从Git仓库中提取README文件"""
    # 常见的README文件名格式
    readme_patterns = [
        "README.md", "README.txt", "README", "README.rst",
        "readme.md", "readme.txt", "readme", "readme.rst"
    ]
    
    for pattern in readme_patterns:
        readme_path = os.path.join(repo_path, pattern)
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
            except UnicodeDecodeError:
                try:
                    with open(readme_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                    
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    return True
                except:
                    pass
            except Exception as e:
                print(f"提取README失败: {e}")
    
    return False

def process_file(filename, cleaned_files):
    """处理单个文件"""
    source_path = os.path.join(DOWNLOAD_DIR, filename)
    target_path = os.path.join(CLEAN_DIR, filename)
    
    # 如果已经处理过且不是强制模式，则跳过
    if filename in cleaned_files and not args.force:
        if args.verbose:
            print(f"跳过 {filename}: 已清理")
        return True, "已跳过"
    
    try:
        # 检查文件是否存在
        if not os.path.exists(source_path):
            print(f"警告: 文件不存在 {source_path}")
            return False, "文件不存在"
        
        # 处理Git仓库
        if is_git_repo(filename):
            if args.handle_git == 'skip':
                if args.verbose:
                    print(f"跳过 {filename}: 是Git仓库")
                return True, "已跳过"
            elif args.handle_git == 'readme_only':
                if args.verbose:
                    print(f"提取 {filename} 中的README...")
                
                # 创建目标目录
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # 提取README文件
                if extract_readme_from_repo(source_path, target_path + ".md"):
                    return True, "已提取README"
                else:
                    # 如果没有找到README，则复制整个仓库
                    if args.verbose:
                        print(f"未找到README，复制整个仓库 {filename}")
                    shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                    return True, "已复制"
            else:  # copy
                if args.verbose:
                    print(f"复制Git仓库 {filename}")
                shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                return True, "已复制"
        
        # 获取文件扩展名
        ext = os.path.splitext(filename)[1].lower()
        
        # 处理HTML和类似HTML的文件
        if ext in HTML_LIKE_EXTENSIONS:
            try:
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # 尝试不同的编码
                try:
                    with open(source_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                except:
                    with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
            
            # 清理内容
            cleaned_content = clean_html(content)
            
            # 保存清理后的文件
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            if args.verbose:
                print(f"已清理 {filename}")
            
            return True, "已清理"
        
        # 对于PDF和Markdown文件，直接复制
        elif ext in COPY_EXTENSIONS:
            shutil.copy2(source_path, target_path)
            if args.verbose:
                print(f"已复制 {filename}")
            return True, "已复制"
        
        # 对于其他文件类型，尝试作为文本文件处理
        else:
            try:
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # 如果不是文本文件，直接复制
                shutil.copy2(source_path, target_path)
                if args.verbose:
                    print(f"已复制 {filename} (非文本文件)")
                return True, "已复制"
            
            # 清理文本内容
            cleaned_content = clean_text_file(content)
            
            # 保存清理后的文件
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            if args.verbose:
                print(f"已清理 {filename} (作为文本文件)")
            
            return True, "已清理"
    
    except Exception as e:
        print(f"处理 {filename} 失败: {e}")
        if args.verbose:
            traceback.print_exc()
        return False, str(e)

def main():
    # 加载日志
    log_data = load_log()
    if not log_data:
        return
    
    clean_log = load_clean_log()
    cleaned_files = clean_log.get("cleaned_files", [])
    
    downloaded_files = log_data.get("downloaded_files", [])
    
    if not downloaded_files:
        print("没有找到已下载的文件")
        return
    
    print(f"找到 {len(downloaded_files)} 个下载文件")
    
    # 统计变量
    clean_count = 0
    copy_count = 0
    readme_count = 0
    skip_count = 0
    error_count = 0
    git_count = 0
    
    # 处理每个文件
    for filename in tqdm(downloaded_files, desc="清理文件"):
        if is_git_repo(filename):
            git_count += 1
        
        success, status = process_file(filename, cleaned_files)
        
        if success:
            if status == "已清理":
                clean_count += 1
            elif status == "已复制":
                copy_count += 1
            elif status == "已跳过":
                skip_count += 1
            elif status == "已提取README":
                readme_count += 1
            
            if filename not in cleaned_files:
                cleaned_files.append(filename)
        else:
            error_count += 1
    
    # 保存清理日志
    save_clean_log(cleaned_files)
    
    # 输出统计信息
    print("\n清理统计:")
    print(f"已清理文件: {clean_count}")
    print(f"已复制文件: {copy_count}")
    if readme_count > 0:
        print(f"已提取README: {readme_count}")
    print(f"已跳过文件: {skip_count}")
    print(f"失败: {error_count}")
    if git_count > 0:
        print(f"其中Git仓库: {git_count} (处理方式: {args.handle_git})")
    print(f"总计: {clean_count + copy_count + readme_count + skip_count + error_count}/{len(downloaded_files)}")
    print(f"\n清理后的文件保存在: {CLEAN_DIR}")

if __name__ == "__main__":
    print("开始清理数据...")
    main()
    print("清理完成!") 