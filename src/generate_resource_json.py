#!/usr/bin/env python3
"""
生成下载资源的JSON信息文件
包含URL、文件名、类型、来源、分类和本地路径信息
"""

import os
import csv
import json
import re
import glob
import argparse
from collections import defaultdict

# 基础配置
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV_FILE = os.path.join(ROOT_DIR, "data/resources.csv")
OLD_CSV_FILE = os.path.join(ROOT_DIR, "data/resources_new.csv")
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "data/downloads")
OUTPUT_FILE = os.path.join(ROOT_DIR, "data/downloaded_resources_info.json")

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='生成下载资源的JSON信息文件')
    parser.add_argument('--csv', '-c', help='CSV资源文件路径', default=None)
    parser.add_argument('--output', '-o', help='输出JSON文件路径', default=None)
    args = parser.parse_args()
    
    # 处理CSV文件路径
    csv_file = args.csv
    if not csv_file:
        # 如果未指定，则首先尝试resources.csv，然后是resources_new.csv
        if os.path.exists(DEFAULT_CSV_FILE):
            csv_file = DEFAULT_CSV_FILE
        elif os.path.exists(OLD_CSV_FILE):
            csv_file = OLD_CSV_FILE
        else:
            raise FileNotFoundError("未找到默认的资源CSV文件")
    
    # 处理输出文件路径
    output_file = args.output or OUTPUT_FILE
    
    return csv_file, output_file

def get_repo_name_from_url(url):
    """从GitHub URL中提取仓库名称"""
    # 匹配GitHub仓库URL
    repo_match = re.search(r'github\.com/[^/]+/([^/]+)', url)
    if repo_match:
        return repo_match.group(1)
    return None

def get_all_files():
    """获取下载目录中的所有文件和目录"""
    all_files = []
    if not os.path.exists(DOWNLOAD_DIR):
        return all_files
    
    # 遍历下载目录中的所有文件和子目录
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        # 添加文件
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
        
        # 添加Git目录（直接子目录，不递归）
        if root == DOWNLOAD_DIR:
            for dir_name in dirs:
                if "_git" in dir_name or os.path.exists(os.path.join(root, dir_name, ".git")):
                    all_files.append(os.path.join(root, dir_name))
    
    print(f"发现下载目录中有 {len(all_files)} 个文件")
    return all_files

def find_file_by_prefix(index, files):
    """根据索引前缀查找文件"""
    prefix = f"{index}_"
    matches = [f for f in files if os.path.basename(f).startswith(prefix)]
    return matches

def find_file_by_name(filename, files):
    """根据文件名查找文件"""
    safe_name = filename.lower().replace(' ', '_')
    matches = []
    for file_path in files:
        basename = os.path.basename(file_path).lower()
        if safe_name in basename:
            matches.append(file_path)
    return matches

def find_git_repo(repo_name, files):
    """查找Git仓库目录"""
    # 直接匹配仓库名
    exact_match = os.path.join(DOWNLOAD_DIR, repo_name)
    if os.path.exists(exact_match) and os.path.isdir(exact_match):
        return exact_match
    
    # 匹配以索引开头、包含仓库名并以_git结尾的目录
    for file_path in files:
        basename = os.path.basename(file_path)
        if os.path.isdir(file_path) and ("_git" in basename or os.path.exists(os.path.join(file_path, ".git"))):
            if repo_name.lower() in basename.lower():
                return file_path
    
    return None

def process_resources(csv_file):
    """读取CSV资源并生成资源信息"""
    all_files = get_all_files()
    
    # 读取CSV文件
    resources = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # 跳过标题行
            headers = next(reader)
            
            # 处理每一行资源
            for i, row in enumerate(reader, 1):
                if not row or len(row) < 5:
                    continue
                    
                url, filename, resource_type, source, category = row
                
                # 准备资源信息
                resource_info = {
                    "url": url,
                    "filename": filename,
                    "resource_type": resource_type,
                    "source": source,
                    "category": category.strip(),  # 确保去除空格
                    "path": ""
                }
                
                # 查找下载文件路径
                if "github.com" in url.lower() and "github" in resource_type.lower():
                    # 针对GitHub仓库的处理
                    repo_name = get_repo_name_from_url(url)
                    if repo_name:
                        # 查找实际下载的Git仓库路径
                        git_path = find_git_repo(repo_name, all_files)
                        if git_path:
                            resource_info["path"] = git_path
                else:
                    # 针对非GitHub资源的处理
                    # 1. 首先按索引前缀查找
                    prefix_matches = find_file_by_prefix(i, all_files)
                    
                    # 2. 如果有多个匹配项，按文件名进一步过滤
                    if len(prefix_matches) > 1:
                        name_filtered = [f for f in prefix_matches if filename.lower() in os.path.basename(f).lower()]
                        if name_filtered:
                            prefix_matches = name_filtered
                    
                    # 3. 如果找到匹配项，取第一个
                    if prefix_matches:
                        resource_info["path"] = prefix_matches[0]
                    else:
                        # 4. 如果没有找到，尝试直接按文件名查找
                        name_matches = find_file_by_name(filename, all_files)
                        if name_matches:
                            resource_info["path"] = name_matches[0]
                
                # 确保路径是相对于工作目录的
                if resource_info["path"] and resource_info["path"].startswith(ROOT_DIR):
                    resource_info["path"] = os.path.relpath(resource_info["path"], ROOT_DIR)
                
                if not resource_info["path"]:
                    print(f"警告: 未找到资源 [{i}] {filename} 的下载路径")
                
                resources.append(resource_info)
        
        return resources
    
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return []

def save_to_json(resources, output_file):
    """将资源信息保存为JSON文件"""
    # 只保存成功下载的资源（有path的资源）
    successful_resources = [r for r in resources if r["path"]]
    total = len(resources)
    found_paths = len(successful_resources)
    
    # 按分类统计
    category_stats = defaultdict(lambda: {"found": 0, "total": 0})
    for r in resources:
        category = r["category"]
        category_stats[category]["total"] += 1
        if r["path"]:
            category_stats[category]["found"] += 1
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(successful_resources, f, ensure_ascii=False, indent=2)
        print(f"成功! 已将 {found_paths} 个成功下载的资源信息写入: {output_file}")
        print(f"共处理 {total} 个资源，其中 {found_paths}/{total} 个资源找到了下载路径\n")
        
        # 打印分类统计
        print("按分类统计:")
        for category, stats in category_stats.items():
            print(f"  {category}: {stats['found']}/{stats['total']} 个资源找到下载路径")
        
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")

def main():
    """主函数"""
    print("正在生成资源信息JSON文件...")
    
    # 解析命令行参数
    try:
        csv_file, output_file = parse_args()
        print(f"使用资源文件: {csv_file}")
        print(f"输出文件: {output_file}")
        
        # 处理资源并保存
        resources = process_resources(csv_file)
        save_to_json(resources, output_file)
    except Exception as e:
        print(f"程序执行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 